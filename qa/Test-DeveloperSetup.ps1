$ErrorActionPreference = 'Stop'
$setupPath = Join-Path (Split-Path -Parent $PSScriptRoot) 'scripts\Test-DeveloperSetup.ps1'
$tokens = $null
$parseErrors = $null
$ast = [Management.Automation.Language.Parser]::ParseFile($setupPath, [ref] $tokens, [ref] $parseErrors)
if ($parseErrors.Count -gt 0) {
    throw 'Setup script has PowerShell syntax errors.'
}
$functionNames = @(
    'Invoke-M365SetupCommand', 'Get-M365Status', 'Test-OnboardingLogin', 'Connect-OnboardingTarget',
    'Get-M365AccessToken', 'Get-SharePointRestTestDocument', 'Get-GraphTestDocument',
    'Test-OnboardingSharePointConnection', 'Invoke-OnboardingSharePointTests'
)
foreach ($name in $functionNames) {
    $functionAst = $ast.Find({
        param($node)
        $node -is [Management.Automation.Language.FunctionDefinitionAst] -and $node.Name -eq $name
    }, $false)
    if ($null -eq $functionAst) { throw "Setup script is missing function $name." }
    . ([scriptblock]::Create($functionAst.Extent.Text))
}
$constantAssignments = $ast.FindAll({
    param($node)
    $node -is [Management.Automation.Language.AssignmentStatementAst] -and
        $node.Left.Extent.Text -match '^\$script:(DefaultTestFolderUrl|Onboarding\w+)$'
}, $false)
foreach ($assignment in $constantAssignments) {
    . ([scriptblock]::Create($assignment.Extent.Text))
}
$ce = $script:OnboardingTargets | Where-Object { $_.Api -eq 'SharePoint' }
$mgp = $script:OnboardingTargets | Where-Object { $_.Api -eq 'Graph' }

function Assert-True {
    param([bool] $Condition, [string] $Message)
    if (-not $Condition) { throw $Message }
}

Assert-True (@($script:OnboardingTargets).Count -eq 2 -and $ce.AppId -ne $mgp.AppId -and $ce.ConnectionName -ne $mgp.ConnectionName) 'Both tenants must be configured with separate apps and connections.'

function New-TestDocument {
    param([string] $Xml)
    Add-Type -AssemblyName System.IO.Compression
    $stream = [IO.MemoryStream]::new()
    $archive = [IO.Compression.ZipArchive]::new($stream, [IO.Compression.ZipArchiveMode]::Create, $true)
    $writer = [IO.StreamWriter]::new($archive.CreateEntry('word/document.xml').Open())
    $writer.Write($Xml)
    $writer.Dispose()
    $archive.Dispose()
    $bytes = $stream.ToArray()
    $stream.Dispose()
    return ,$bytes
}

function Set-ActiveConnection {
    param([string] $Name)
    $script:Active = $Name
    $script:SignedOut = $false
}

function Test-CommandAvailable { return $script:CliAvailable }
function Write-Host {}
function Read-Host { throw 'The check must not prompt in the terminal.' }
function Write-Check {
    param([string] $Status, [string] $Message)
    $script:Checks += [pscustomobject]@{ Status = $Status; Message = $Message }
}
function m365 {
    $global:LASTEXITCODE = $script:CliExitCode
    if ($args[0] -eq 'status') {
        if ($script:SignedOut) { return '"Logged out"' }
        $c = $script:Connections[$script:Active]
        return (@{ connectionName = $script:Active; connectedAs = 'tester@example.invalid'; authType = 'browser'; appId = $c.AppId; appTenant = $c.TenantId } | ConvertTo-Json)
    }
    if ($args[0] -eq 'connection' -and $args[1] -eq 'use') {
        $script:ConnectionUses += $args[3]
        if ($script:Connections.ContainsKey($args[3])) { Set-ActiveConnection $args[3] } else { $global:LASTEXITCODE = 1 }
        return
    }
    if ($args[0] -eq 'login') {
        Assert-True ($args[1] -eq '--authType' -and $args[2] -eq 'browser') 'Sign-in must use the browser, not passwords or secrets.'
        $loginArgs = $args
        $target = $script:OnboardingTargets | Where-Object { $_.AppId -eq $loginArgs[4] -and $_.TenantId -eq $loginArgs[6] -and $_.ConnectionName -eq $loginArgs[8] }
        Assert-True ($null -ne $target) 'Login must use an approved onboarding app, its tenant, and its own connection name.'
        $script:LoginCalls += 1
        $global:LASTEXITCODE = $script:LoginExitCode
        Write-Error 'Synthetic CLI progress or error must not reach the user.' -ErrorAction Continue
        if ($script:LoginExitCode -eq 0) {
            $script:Connections[$args[8]] = @{ AppId = $args[4]; TenantId = $args[6] }
            Set-ActiveConnection $args[8]
        }
        return
    }
    Assert-True ($args[0] -eq 'util' -and $args[1] -eq 'accesstoken' -and $args[2] -eq 'get') 'Unexpected CLI operation.'
    $script:TokenResources += $args[4]
    if ($script:TokenFailure) { $global:LASTEXITCODE = 1 }
    return 'synthetic-token'
}
function Invoke-RestMethod {
    param($Method, $Uri, $Headers, $TimeoutSec, $MaximumRedirection)
    Assert-True ($Method -eq 'GET' -and $MaximumRedirection -eq 0) 'Only non-redirecting GET requests are allowed.'
    $script:Requests += 1
    if ($script:DenyAccess) { throw 'Synthetic HTTP 403.' }
    $decoded = [uri]::UnescapeDataString($Uri)
    if ($Uri.StartsWith('https://graph.microsoft.com/v1.0/')) {
        $siteUri = [uri] $mgp.SiteUrl
        if ($decoded -like "*/sites/$($siteUri.Host):$($siteUri.AbsolutePath)?*") { return @{ id = 'site-id' } }
        if ($decoded -like '*/sites/site-id/drive?*') { return @{ id = 'drive-id' } }
        if ($decoded -like "*/drives/drive-id/root:/$($mgp.FolderPath):/children?*") { return @{ value = @(@{ name = $script:FileName }) } }
        Assert-True ($decoded -like "*/drives/drive-id/root:/$($mgp.FolderPath)/Connection Test.docx") 'Graph request escaped the test folder.'
        return @{ '@microsoft.graph.downloadUrl' = $script:DownloadUrl }
    }
    Assert-True ($Uri.StartsWith("$($ce.SiteUrl)/_api/web/GetFolderByServerRelativeUrl(")) 'Unexpected folder endpoint.'
    Assert-True ($decoded.Contains("('$($ce.FolderPath)')/Files?")) 'Request escaped the test library.'
    return @{ value = @(@{ Name = $script:FileName }) }
}
function Invoke-WebRequest {
    param([switch] $UseBasicParsing, $Method, $Uri, $Headers, $TimeoutSec, $MaximumRedirection)
    Assert-True ($Method -eq 'GET' -and $MaximumRedirection -eq 0) 'Only non-redirecting GET requests are allowed.'
    if ($Uri -eq $script:DownloadUrl) {
        Assert-True ($null -eq $Headers) 'The bearer token must not be sent to the pre-authenticated download URL.'
    }
    else {
        Assert-True ([uri]::UnescapeDataString($Uri).EndsWith("$($ce.FolderPath)/Connection Test.docx')/`$value")) 'Download escaped the test document.'
    }
    $script:Requests += 1
    return @{ Content = $script:DocumentBytes }
}

$xmlPrefix = '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p>'
$xmlSuffix = '</w:p></w:body></w:document>'
$validDocument = New-TestDocument ($xmlPrefix + '<w:r><w:t>MGP connection </w:t></w:r><w:r><w:t>test successful.</w:t></w:r>' + $xmlSuffix)

function Reset-State {
    $script:CliAvailable = $true
    $script:CliExitCode = 0
    $script:FileName = 'Connection Test.docx'
    $script:DownloadUrl = 'https://mgpinc.sharepoint.com/sites/Spark/_layouts/15/download.aspx?tempauth=synthetic'
    $script:DenyAccess = $false
    $script:TokenFailure = $false
    $script:Connections = @{ 'user-existing' = @{ AppId = $ce.AppId; TenantId = $ce.TenantId } }
    Set-ActiveConnection 'user-existing'
    $script:LoginCalls = 0
    $script:LoginExitCode = 0
    $script:ConnectionUses = @()
    $script:TokenResources = @()
    $script:Requests = 0
    $script:Checks = @()
    $script:DocumentBytes = $validDocument
}

Reset-State
Test-OnboardingSharePointConnection $ce
Assert-True ($script:Requests -eq 2 -and $script:LoginCalls -eq 0) 'An existing onboarding login must be reused without signing in again.'

Reset-State
$script:SignedOut = $true
Test-OnboardingSharePointConnection $ce
Assert-True ($script:LoginCalls -eq 1 -and $script:Requests -eq 2) 'Signed-out users must sign in once and continue automatically.'

Reset-State
$script:Connections['provisioning'] = @{ AppId = 'provisioning-app'; TenantId = $ce.TenantId }
Set-ActiveConnection 'provisioning'
Test-OnboardingSharePointConnection $ce
Assert-True ($script:LoginCalls -eq 1 -and $script:Requests -eq 2) 'A different active app must never be used for the read-only test.'

Reset-State
$script:Connections[$mgp.ConnectionName] = @{ AppId = $mgp.AppId; TenantId = $mgp.TenantId }
Test-OnboardingSharePointConnection $mgp
Assert-True ($script:LoginCalls -eq 0 -and $script:Active -eq $mgp.ConnectionName) 'A saved MGP connection must be reused without signing in again.'
Assert-True ($script:Requests -eq 5 -and $script:TokenResources -contains 'https://graph.microsoft.com') 'The MGP test must list and read through Microsoft Graph.'

Reset-State
$script:Connections['wrong-tenant'] = @{ AppId = $mgp.AppId; TenantId = $ce.TenantId }
Set-ActiveConnection 'wrong-tenant'
Test-OnboardingSharePointConnection $mgp
Assert-True ($script:LoginCalls -eq 1) 'The right app in the wrong tenant must not be used.'

Reset-State
Invoke-OnboardingSharePointTests
Assert-True ((@($script:Checks | Where-Object Status -eq 'PASS').Count) -eq 2 -and -not ($script:Checks | Where-Object Status -ne 'PASS')) 'Both tenants must pass in one run.'
Assert-True ($script:LoginCalls -eq 1) 'Only the tenant without a usable login may open a browser sign-in.'
Assert-True ($script:Active -eq 'user-existing') 'The previously active CLI login must be restored afterwards.'

Reset-State
$script:DenyAccess = $true
Invoke-OnboardingSharePointTests
Assert-True ((@($script:Checks | Where-Object Status -eq 'FAIL').Count) -eq 2 -and $script:Active -eq 'user-existing') 'Each tenant must report its own blocker, and the previous login must still be restored.'

$cases = @('missing-cli', 'browser-login-failed', 'failed-status', 'failed-token', 'denied', 'missing-file', 'wrong-phrase', 'invalid-docx')
foreach ($target in @($ce, $mgp)) {
    $targetCases = $cases
    if ($target -eq $mgp) { $targetCases += 'foreign-download-url' }
    foreach ($case in $targetCases) {
        Reset-State
        $script:Connections[$mgp.ConnectionName] = @{ AppId = $mgp.AppId; TenantId = $mgp.TenantId }
        $script:CliAvailable = $case -ne 'missing-cli'
        $script:CliExitCode = if ($case -eq 'failed-status') { 1 } else { 0 }
        $script:DenyAccess = $case -eq 'denied'
        $script:TokenFailure = $case -eq 'failed-token'
        if ($case -eq 'browser-login-failed') {
            $script:Connections.Remove($mgp.ConnectionName)
            $script:SignedOut = $true
            $script:LoginExitCode = 1
        }
        if ($case -eq 'missing-file') { $script:FileName = 'Other.docx' }
        if ($case -eq 'foreign-download-url') { $script:DownloadUrl = 'https://attacker.example.invalid/file.docx' }
        $script:DocumentBytes = if ($case -eq 'invalid-docx') {
            [Text.Encoding]::UTF8.GetBytes('not a zip archive')
        }
        elseif ($case -eq 'wrong-phrase') {
            New-TestDocument ($xmlPrefix + '<w:r><w:t>Not the expected verification phrase.</w:t></w:r>' + $xmlSuffix)
        }
        else { $validDocument }
        $failure = $null
        try { Test-OnboardingSharePointConnection $target }
        catch { $failure = $_ }
        Assert-True ($null -ne $failure) "$($target.Name) $case must fail explicitly."
        if ($case -eq 'browser-login-failed') {
            Assert-True ($failure.Exception.Message.Contains('Browser sign-in')) 'Failed browser sign-in must give the specific blocker.'
            Assert-True ($script:LoginCalls -eq 1) 'A failed login must not loop or retry automatically.'
        }
        if ($case -in @('missing-cli', 'browser-login-failed', 'failed-status', 'failed-token')) {
            Assert-True ($script:Requests -eq 0) "$($target.Name) $case must not access SharePoint."
        }
        if ($case -eq 'denied') {
            Assert-True ($script:Requests -eq 1) "$($target.Name) $case must stop at the first request."
        }
        if ($case -in @('missing-file', 'foreign-download-url')) {
            $expectedRequests = if ($target -eq $ce) { 1 } elseif ($case -eq 'missing-file') { 3 } else { 4 }
            Assert-True ($script:Requests -eq $expectedRequests) "$($target.Name) $case must stop before downloading."
        }
    }
}
Write-Output 'PASS: both tenants sign in, reuse saved logins, read the test document, and restore the previous login; blocker cases fail safely for each tenant.'
