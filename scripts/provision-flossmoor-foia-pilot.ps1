param(
    [string]$SiteUrl = "https://communityessentials.sharepoint.com/sites/Administration",
    [string]$ResourceHost = "https://communityessentials.sharepoint.com"
)

$ErrorActionPreference = "Stop"

function Get-SpoToken {
    $token = m365 util accesstoken get --resource $ResourceHost --new --output text
    if (-not $token) {
        throw "Microsoft 365 CLI did not return a SharePoint access token. Run m365 login with the approved provisioning application."
    }

    return $token
}

function Invoke-Spo {
    param(
        [Parameter(Mandatory = $true)]
        [ValidateSet("GET", "POST")]
        [string]$Method,

        [Parameter(Mandatory = $true)]
        [string]$RelativeUri,

        [object]$Body
    )

    $headers = @{
        Authorization = "Bearer $script:SpoToken"
        Accept = "application/json;odata=verbose"
    }

    $arguments = @{
        Method = $Method
        Uri = "$SiteUrl$RelativeUri"
        Headers = $headers
    }

    if ($null -ne $Body) {
        $headers["Content-Type"] = "application/json;odata=verbose"
        $arguments["Body"] = $Body | ConvertTo-Json -Depth 20 -Compress
    }

    try {
        return Invoke-RestMethod @arguments
    }
    catch {
        $response = $_.Exception.Response
        if ($response) {
            $reader = New-Object System.IO.StreamReader($response.GetResponseStream())
            $details = $reader.ReadToEnd()
            throw "SharePoint request failed: $Method $RelativeUri`nHTTP $([int]$response.StatusCode): $details"
        }

        throw
    }
}

function Get-SpoLists {
    $response = Invoke-Spo -Method GET -RelativeUri "/_api/web/lists?`$select=Id,Title,Description,BaseTemplate,ListItemEntityTypeFullName,RootFolder/ServerRelativeUrl&`$expand=RootFolder"
    return @($response.d.results)
}

function Ensure-SpoList {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Title,

        [Parameter(Mandatory = $true)]
        [ValidateSet(100, 101)]
        [int]$BaseTemplate,

        [Parameter(Mandatory = $true)]
        [string]$Description
    )

    $existing = Get-SpoLists | Where-Object { $_.Title -eq $Title } | Select-Object -First 1
    if ($existing) {
        Write-Host "Existing resource: $Title"
        return $existing
    }

    $body = @{
        __metadata = @{
            type = "SP.List"
        }
        Title = $Title
        BaseTemplate = $BaseTemplate
        Description = $Description
        EnableVersioning = $true
    }

    Invoke-Spo -Method POST -RelativeUri "/_api/web/lists" -Body $body | Out-Null
    $created = Get-SpoLists | Where-Object { $_.Title -eq $Title } | Select-Object -First 1
    if (-not $created) {
        throw "SharePoint did not return the newly created resource: $Title"
    }

    Write-Host "Created resource: $Title"
    return $created
}

function Get-SpoFields {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ListId
    )

    $response = Invoke-Spo -Method GET -RelativeUri "/_api/web/lists(guid'$ListId')/fields?`$select=Id,InternalName,Title"
    return @($response.d.results)
}

function Ensure-SpoField {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ListId,

        [Parameter(Mandatory = $true)]
        [string]$InternalName,

        [Parameter(Mandatory = $true)]
        [string]$SchemaXml
    )

    $existing = Get-SpoFields -ListId $ListId |
        Where-Object { $_.InternalName -eq $InternalName } |
        Select-Object -First 1

    if ($existing) {
        Write-Host "  Existing column: $($existing.Title)"
        return
    }

    $body = @{
        parameters = @{
            __metadata = @{
                type = "SP.XmlSchemaFieldCreationInformation"
            }
            SchemaXml = $SchemaXml
            Options = 8
        }
    }

    Invoke-Spo -Method POST -RelativeUri "/_api/web/lists(guid'$ListId')/fields/createfieldasxml" -Body $body | Out-Null
    Write-Host "  Created column: $InternalName"
}

function ConvertTo-XmlValue {
    param([string]$Value)

    return [System.Security.SecurityElement]::Escape($Value)
}

function New-TextFieldXml {
    param(
        [string]$Name,
        [string]$DisplayName,
        [bool]$Required = $false
    )

    $requiredValue = if ($Required) { "TRUE" } else { "FALSE" }
    return "<Field Type=`"Text`" DisplayName=`"$(ConvertTo-XmlValue $DisplayName)`" Name=`"$Name`" StaticName=`"$Name`" Required=`"$requiredValue`" Group=`"FOIA Pilot`" />"
}

function New-NoteFieldXml {
    param(
        [string]$Name,
        [string]$DisplayName,
        [bool]$Required = $false
    )

    $requiredValue = if ($Required) { "TRUE" } else { "FALSE" }
    return "<Field Type=`"Note`" DisplayName=`"$(ConvertTo-XmlValue $DisplayName)`" Name=`"$Name`" StaticName=`"$Name`" Required=`"$requiredValue`" NumLines=`"6`" RichText=`"FALSE`" Group=`"FOIA Pilot`" />"
}

function New-ChoiceFieldXml {
    param(
        [string]$Name,
        [string]$DisplayName,
        [string[]]$Choices,
        [bool]$Required = $false,
        [string]$DefaultValue
    )

    $requiredValue = if ($Required) { "TRUE" } else { "FALSE" }
    $choiceXml = ($Choices | ForEach-Object { "<CHOICE>$(ConvertTo-XmlValue $_)</CHOICE>" }) -join ""
    $defaultXml = if ($DefaultValue) { "<Default>$(ConvertTo-XmlValue $DefaultValue)</Default>" } else { "" }
    return "<Field Type=`"Choice`" DisplayName=`"$(ConvertTo-XmlValue $DisplayName)`" Name=`"$Name`" StaticName=`"$Name`" Required=`"$requiredValue`" Format=`"Dropdown`" FillInChoice=`"FALSE`" Group=`"FOIA Pilot`"><CHOICES>$choiceXml</CHOICES>$defaultXml</Field>"
}

function New-DateFieldXml {
    param(
        [string]$Name,
        [string]$DisplayName,
        [bool]$Required = $false
    )

    $requiredValue = if ($Required) { "TRUE" } else { "FALSE" }
    return "<Field Type=`"DateTime`" DisplayName=`"$(ConvertTo-XmlValue $DisplayName)`" Name=`"$Name`" StaticName=`"$Name`" Required=`"$requiredValue`" Format=`"DateOnly`" FriendlyDisplayFormat=`"Disabled`" Group=`"FOIA Pilot`" />"
}

function New-BooleanFieldXml {
    param(
        [string]$Name,
        [string]$DisplayName
    )

    return "<Field Type=`"Boolean`" DisplayName=`"$(ConvertTo-XmlValue $DisplayName)`" Name=`"$Name`" StaticName=`"$Name`" Group=`"FOIA Pilot`"><Default>0</Default></Field>"
}

function New-NumberFieldXml {
    param(
        [string]$Name,
        [string]$DisplayName
    )

    return "<Field Type=`"Number`" DisplayName=`"$(ConvertTo-XmlValue $DisplayName)`" Name=`"$Name`" StaticName=`"$Name`" Decimals=`"0`" Group=`"FOIA Pilot`" />"
}

function New-PersonFieldXml {
    param(
        [string]$Name,
        [string]$DisplayName
    )

    return "<Field Type=`"User`" DisplayName=`"$(ConvertTo-XmlValue $DisplayName)`" Name=`"$Name`" StaticName=`"$Name`" List=`"UserInfo`" ShowField=`"ImnName`" UserSelectionMode=`"PeopleOnly`" UserSelectionScope=`"0`" Group=`"FOIA Pilot`" />"
}

function New-LookupFieldXml {
    param(
        [string]$Name,
        [string]$DisplayName,
        [string]$LookupListId
    )

    return "<Field Type=`"Lookup`" DisplayName=`"$(ConvertTo-XmlValue $DisplayName)`" Name=`"$Name`" StaticName=`"$Name`" List=`"{$LookupListId}`" ShowField=`"Title`" Group=`"FOIA Pilot`" />"
}

function Ensure-SpoFields {
    param(
        [string]$ListId,
        [object[]]$Definitions
    )

    foreach ($definition in $Definitions) {
        Ensure-SpoField -ListId $ListId -InternalName $definition.Name -SchemaXml $definition.Xml
    }
}

function Get-SpoItems {
    param(
        [string]$ListId
    )

    $response = Invoke-Spo -Method GET -RelativeUri "/_api/web/lists(guid'$ListId')/items?`$select=Id,Title"
    return @($response.d.results)
}

function Ensure-DepartmentItems {
    param(
        [object]$List
    )

    $existing = @(Get-SpoItems -ListId $List.Id | ForEach-Object { $_.Title })
    $departments = @(
        @{ Title = "Administration"; DepartmentCode = "ADMIN"; Active = $true; SortOrder = 10; IsPolice = $false },
        @{ Title = "Police Department"; DepartmentCode = "POLICE"; Active = $true; SortOrder = 20; IsPolice = $true },
        @{ Title = "Finance"; DepartmentCode = "FIN"; Active = $true; SortOrder = 30; IsPolice = $false },
        @{ Title = "Planning and Zoning"; DepartmentCode = "PZ"; Active = $true; SortOrder = 40; IsPolice = $false },
        @{ Title = "Fire Department"; DepartmentCode = "FIRE"; Active = $true; SortOrder = 50; IsPolice = $false },
        @{ Title = "Building Department"; DepartmentCode = "BLDG"; Active = $true; SortOrder = 60; IsPolice = $false },
        @{ Title = "Public Works Department"; DepartmentCode = "PW"; Active = $true; SortOrder = 70; IsPolice = $false }
    )

    foreach ($department in $departments) {
        if ($existing -contains $department.Title) {
            Write-Host "  Existing department: $($department.Title)"
            continue
        }

        $body = @{
            __metadata = @{
                type = $List.ListItemEntityTypeFullName
            }
            Title = $department.Title
            DepartmentCode = $department.DepartmentCode
            Active = $department.Active
            SortOrder = $department.SortOrder
            IsPolice = $department.IsPolice
        }

        Invoke-Spo -Method POST -RelativeUri "/_api/web/lists(guid'$($List.Id)')/items" -Body $body | Out-Null
        Write-Host "  Created department: $($department.Title)"
    }
}

$script:SpoToken = Get-SpoToken
$web = Invoke-Spo -Method GET -RelativeUri "/_api/web?`$select=Title,Url"
Write-Host "Provisioning Flossmoor FOIA pilot in $($web.d.Url)"

$departments = Ensure-SpoList `
    -Title "FOIA Pilot Departments" `
    -BaseTemplate 100 `
    -Description "Synthetic pilot routing reference for the Flossmoor FOIA delivery standard."

Ensure-SpoFields -ListId $departments.Id -Definitions @(
    @{ Name = "DepartmentCode"; Xml = (New-TextFieldXml -Name "DepartmentCode" -DisplayName "Department Code" -Required $true) },
    @{ Name = "Active"; Xml = (New-BooleanFieldXml -Name "Active" -DisplayName "Active") },
    @{ Name = "SortOrder"; Xml = (New-NumberFieldXml -Name "SortOrder" -DisplayName "Sort Order") },
    @{ Name = "IsPolice"; Xml = (New-BooleanFieldXml -Name "IsPolice" -DisplayName "Is Police") }
)

$requests = Ensure-SpoList `
    -Title "FOIA Pilot Requests" `
    -BaseTemplate 100 `
    -Description "Synthetic pilot master request tracking for the Flossmoor FOIA delivery standard."

Ensure-SpoFields -ListId $requests.Id -Definitions @(
    @{ Name = "ReceivedDate"; Xml = (New-DateFieldXml -Name "ReceivedDate" -DisplayName "Received Date" -Required $true) },
    @{ Name = "IntakeMethod"; Xml = (New-ChoiceFieldXml -Name "IntakeMethod" -DisplayName "Intake Method" -Required $true -Choices @("Online Form", "Email", "Written", "In Person", "Other")) },
    @{ Name = "RequestRoute"; Xml = (New-ChoiceFieldXml -Name "RequestRoute" -DisplayName "Request Route" -Required $true -Choices @("Police", "Non-Police", "Multi-Department", "Unassigned")) },
    @{ Name = "CommercialPurpose"; Xml = (New-ChoiceFieldXml -Name "CommercialPurpose" -DisplayName "Commercial Purpose" -Choices @("Unknown", "Yes", "No") -DefaultValue "Unknown") },
    @{ Name = "RequesterFirstName"; Xml = (New-TextFieldXml -Name "RequesterFirstName" -DisplayName "Requester First Name") },
    @{ Name = "RequesterLastName"; Xml = (New-TextFieldXml -Name "RequesterLastName" -DisplayName "Requester Last Name") },
    @{ Name = "RequesterStreetAddress"; Xml = (New-TextFieldXml -Name "RequesterStreetAddress" -DisplayName "Requester Street Address") },
    @{ Name = "RequesterCity"; Xml = (New-TextFieldXml -Name "RequesterCity" -DisplayName "Requester City") },
    @{ Name = "RequesterState"; Xml = (New-TextFieldXml -Name "RequesterState" -DisplayName "Requester State") },
    @{ Name = "RequesterZip"; Xml = (New-TextFieldXml -Name "RequesterZip" -DisplayName "Requester ZIP") },
    @{ Name = "RequesterEmail"; Xml = (New-TextFieldXml -Name "RequesterEmail" -DisplayName "Requester Email") },
    @{ Name = "RequesterPhone"; Xml = (New-TextFieldXml -Name "RequesterPhone" -DisplayName "Requester Phone") },
    @{ Name = "RequestDescription"; Xml = (New-NoteFieldXml -Name "RequestDescription" -DisplayName "Request Description" -Required $true) },
    @{ Name = "DeliveryFormat"; Xml = (New-ChoiceFieldXml -Name "DeliveryFormat" -DisplayName "Delivery Format" -Choices @("Unspecified", "Electronic", "Paper") -DefaultValue "Unspecified") },
    @{ Name = "CertifiedCopies"; Xml = (New-ChoiceFieldXml -Name "CertifiedCopies" -DisplayName "Certified Copies" -Choices @("Unknown", "Yes", "No") -DefaultValue "Unknown") },
    @{ Name = "FeeWaiverRequested"; Xml = (New-ChoiceFieldXml -Name "FeeWaiverRequested" -DisplayName "Fee Waiver Requested" -Choices @("Unknown", "Yes", "No") -DefaultValue "Unknown") },
    @{ Name = "OverallStatus"; Xml = (New-ChoiceFieldXml -Name "OverallStatus" -DisplayName "Overall Status" -Required $true -Choices @("New", "Triage", "Assigned", "In Progress", "Awaiting Department", "Awaiting Clarification", "Extension Pending", "Ready for Response", "Completed", "Closed", "Denied") -DefaultValue "New") },
    @{ Name = "DueDate"; Xml = (New-DateFieldXml -Name "DueDate" -DisplayName "Due Date") },
    @{ Name = "DueDateConfirmed"; Xml = (New-BooleanFieldXml -Name "DueDateConfirmed" -DisplayName "Due Date Confirmed") },
    @{ Name = "PrimaryDepartment"; Xml = (New-LookupFieldXml -Name "PrimaryDepartment" -DisplayName "Primary Department" -LookupListId $departments.Id) },
    @{ Name = "AssignedOfficer"; Xml = (New-PersonFieldXml -Name "AssignedOfficer" -DisplayName "Assigned Officer") },
    @{ Name = "ExtensionType"; Xml = (New-ChoiceFieldXml -Name "ExtensionType" -DisplayName "Extension Type" -Choices @("None", "Statutory", "Agreed") -DefaultValue "None") },
    @{ Name = "ExtensionDays"; Xml = (New-NumberFieldXml -Name "ExtensionDays" -DisplayName "Extension Days") },
    @{ Name = "ExtensionStatus"; Xml = (New-ChoiceFieldXml -Name "ExtensionStatus" -DisplayName "Extension Status" -Choices @("Not Applicable", "Requested", "Agreed", "Declined", "No Response") -DefaultValue "Not Applicable") },
    @{ Name = "FinalResponseDate"; Xml = (New-DateFieldXml -Name "FinalResponseDate" -DisplayName "Final Response Date") },
    @{ Name = "CloseoutNotes"; Xml = (New-NoteFieldXml -Name "CloseoutNotes" -DisplayName "Closeout Notes") },
    @{ Name = "SourceSubmissionId"; Xml = (New-TextFieldXml -Name "SourceSubmissionId" -DisplayName "Source Submission ID") },
    @{ Name = "CurrentStageNotes"; Xml = (New-NoteFieldXml -Name "CurrentStageNotes" -DisplayName "Current Stage Notes") }
)

$assignments = Ensure-SpoList `
    -Title "FOIA Pilot Assignments" `
    -BaseTemplate 100 `
    -Description "Synthetic pilot department assignments for FOIA requests."

Ensure-SpoFields -ListId $assignments.Id -Definitions @(
    @{ Name = "Request"; Xml = (New-LookupFieldXml -Name "Request" -DisplayName "Request" -LookupListId $requests.Id) },
    @{ Name = "Department"; Xml = (New-LookupFieldXml -Name "Department" -DisplayName "Department" -LookupListId $departments.Id) },
    @{ Name = "AssignedTo"; Xml = (New-PersonFieldXml -Name "AssignedTo" -DisplayName "Assigned To") },
    @{ Name = "AssignmentStatus"; Xml = (New-ChoiceFieldXml -Name "AssignmentStatus" -DisplayName "Assignment Status" -Required $true -Choices @("New", "Accepted", "In Progress", "Awaiting Clarification", "Redaction", "Complete", "Cancelled") -DefaultValue "New") },
    @{ Name = "AssignmentDueDate"; Xml = (New-DateFieldXml -Name "AssignmentDueDate" -DisplayName "Assignment Due Date") },
    @{ Name = "RedactionRequired"; Xml = (New-ChoiceFieldXml -Name "RedactionRequired" -DisplayName "Redaction Required" -Choices @("Unknown", "Yes", "No") -DefaultValue "Unknown") },
    @{ Name = "DepartmentCompleteDate"; Xml = (New-DateFieldXml -Name "DepartmentCompleteDate" -DisplayName "Department Complete Date") },
    @{ Name = "ResponseNotes"; Xml = (New-NoteFieldXml -Name "ResponseNotes" -DisplayName "Response Notes") },
    @{ Name = "Active"; Xml = (New-BooleanFieldXml -Name "Active" -DisplayName "Active") }
)

$records = Ensure-SpoList `
    -Title "FOIA Pilot Records" `
    -BaseTemplate 101 `
    -Description "Synthetic pilot record artifacts for FOIA requests."

Ensure-SpoFields -ListId $records.Id -Definitions @(
    @{ Name = "Request"; Xml = (New-LookupFieldXml -Name "Request" -DisplayName "Request" -LookupListId $requests.Id) },
    @{ Name = "Department"; Xml = (New-LookupFieldXml -Name "Department" -DisplayName "Department" -LookupListId $departments.Id) },
    @{ Name = "DocumentType"; Xml = (New-ChoiceFieldXml -Name "DocumentType" -DisplayName "Document Type" -Required $true -Choices @("Request", "Responsive Record", "Redacted Record", "Extension Letter", "Correspondence", "Final Response", "Other")) },
    @{ Name = "RedactionStatus"; Xml = (New-ChoiceFieldXml -Name "RedactionStatus" -DisplayName "Redaction Status" -Choices @("Not Reviewed", "Not Required", "In Progress", "Complete") -DefaultValue "Not Reviewed") },
    @{ Name = "IsFinalResponse"; Xml = (New-BooleanFieldXml -Name "IsFinalResponse" -DisplayName "Is Final Response") },
    @{ Name = "Sensitivity"; Xml = (New-ChoiceFieldXml -Name "Sensitivity" -DisplayName "Sensitivity" -Choices @("Internal", "Public Response", "Restricted") -DefaultValue "Internal") },
    @{ Name = "Notes"; Xml = (New-NoteFieldXml -Name "Notes" -DisplayName "Notes") }
)

Ensure-DepartmentItems -List $departments

Write-Host ""
Write-Host "Provisioning complete."
Write-Host "Departments: $ResourceHost$($departments.RootFolder.ServerRelativeUrl)"
Write-Host "Requests: $ResourceHost$($requests.RootFolder.ServerRelativeUrl)"
Write-Host "Assignments: $ResourceHost$($assignments.RootFolder.ServerRelativeUrl)"
Write-Host "Records: $ResourceHost$($records.RootFolder.ServerRelativeUrl)"
