[CmdletBinding()]
param(
    [string] $SharePointFolderUrl
)

$ErrorActionPreference = 'Stop'
$script:Failed = $false
$script:Warnings = 0
# Read-only onboarding app (delegated AllSites.Read) in the Spark by MGP tenant; not the provisioning app.
$script:OnboardingAppId = 'c894f981-7ffe-4aeb-aa2b-c71f179f35c8'
$script:OnboardingTenantId = 'ce08ca1a-3a87-472b-affa-217b4d4793ce'
$script:OnboardingSiteUrl = 'https://communityessentials.sharepoint.com/sites/TreyResearchlegaldocuments'
$script:OnboardingFolderPath = '/sites/TreyResearchlegaldocuments/Shared Documents/Documents'
$script:DefaultTestFolderUrl = 'https://communityessentials.sharepoint.com/sites/TreyResearchlegaldocuments/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FTreyResearchlegaldocuments%2FShared%20Documents%2FDocuments'
if (-not $PSBoundParameters.ContainsKey('SharePointFolderUrl')) {
    $SharePointFolderUrl = $script:DefaultTestFolderUrl
}

function Assert-SharePointFolderUrl {
    param(
        [string] $Value
    )

    $folderUri = $null
    if (
        -not [uri]::TryCreate($Value.Trim(), [UriKind]::Absolute, [ref] $folderUri) -or
        $folderUri.Scheme -ne 'https' -or
        -not $folderUri.Host.EndsWith('.sharepoint.com', [StringComparison]::OrdinalIgnoreCase)
    ) {
        throw 'Paste only the approved HTTPS SharePoint folder URL, not the PowerShell command, then retry. The hostname must end in .sharepoint.com.'
    }
}

if (-not [string]::IsNullOrWhiteSpace($SharePointFolderUrl) -or $PSBoundParameters.ContainsKey('SharePointFolderUrl')) {
    Assert-SharePointFolderUrl $SharePointFolderUrl
}

function Write-Check {
    param(
        [Parameter(Mandatory)]
        [ValidateSet('PASS', 'WARN', 'FAIL', 'INFO')]
        [string] $Status,

        [Parameter(Mandatory)]
        [string] $Message
    )

    $color = switch ($Status) {
        'PASS' { 'Green' }
        'WARN' { 'Yellow' }
        'FAIL' { 'Red' }
        default { 'Cyan' }
    }

    Write-Host "[$Status] $Message" -ForegroundColor $color

    if ($Status -eq 'FAIL') {
        $script:Failed = $true
    }

    if ($Status -eq 'WARN') {
        $script:Warnings += 1
    }
}

function Test-CommandAvailable {
    param(
        [Parameter(Mandatory)]
        [string] $Name
    )

    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Invoke-M365SetupCommand {
    param(
        [string[]] $Arguments,
        [string] $FailureMessage
    )

    $previousErrorAction = $ErrorActionPreference
    try {
        $ErrorActionPreference = 'Continue'
        $output = @(& m365 @Arguments 2>&1)
        $exitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $previousErrorAction
    }
    if ($exitCode -ne 0) {
        throw $FailureMessage
    }
    return (($output | Where-Object { $_ -isnot [Management.Automation.ErrorRecord] }) -join "`n").Trim()
}

function Test-OnboardingSharePointConnection {
    if (-not (Test-CommandAvailable 'm365')) {
        throw 'Microsoft 365 CLI (m365) is missing. Ask IT to install it and configure the approved login.'
    }

    $statusOutput = Invoke-M365SetupCommand -Arguments @('status', '--output', 'json') -FailureMessage 'Could not check the Microsoft 365 CLI login.'
    if (-not $statusOutput) {
        throw 'Microsoft 365 CLI has no usable login. Ask IT to configure the approved user login.'
    }
    $status = ($statusOutput -join "`n") | ConvertFrom-Json
    $usingOnboardingApp = $status -isnot [string] -and $status.appId -eq $script:OnboardingAppId -and $status.authType -in @('DeviceCode', 'Browser')
    if (-not $usingOnboardingApp) {
        Write-Host 'Opening Microsoft 365 sign-in. Complete sign-in in your browser.' -ForegroundColor Cyan
        $null = Invoke-M365SetupCommand -Arguments @('login', '--authType', 'browser', '--appId', $script:OnboardingAppId, '--tenant', $script:OnboardingTenantId, '--output', 'none') -FailureMessage 'Browser sign-in did not complete. Retry, or ask IT to confirm your account can use the MGP Developer Onboarding CLI app. No SharePoint documents were accessed.'
        $statusOutput = Invoke-M365SetupCommand -Arguments @('status', '--output', 'json') -FailureMessage 'Could not verify the login after browser sign-in.'
        $status = ($statusOutput -join "`n") | ConvertFrom-Json
        if ($status -is [string] -or $status.appId -ne $script:OnboardingAppId -or -not $status.connectedAs) {
            throw 'Sign-in did not activate the approved onboarding app. Retry the check or contact IT. No SharePoint documents were accessed.'
        }
    }
    Write-Host "Signed in as: $($status.connectedAs)"

    $siteUrl = $script:OnboardingSiteUrl
    $resourceHost = ([uri] $siteUrl).GetLeftPart([UriPartial]::Authority)
    $tokenOutput = Invoke-M365SetupCommand -Arguments @('util', 'accesstoken', 'get', '--resource', $resourceHost, '--output', 'text') -FailureMessage 'Could not obtain a SharePoint token. Ask IT to verify the approved login and application permissions.'
    if (-not $tokenOutput) {
        throw 'Could not obtain a SharePoint token. Ask IT to verify the approved login and application permissions.'
    }
    $token = ($tokenOutput -join "`n").Trim()
    $headers = @{
        Authorization = "Bearer $token"
        Accept = 'application/json;odata=nometadata'
    }
    $folderPath = $script:OnboardingFolderPath
    $folderLiteral = [uri]::EscapeDataString($folderPath.Replace("'", "''"))
    $filesUri = "$siteUrl/_api/web/GetFolderByServerRelativeUrl('$folderLiteral')/Files?`$select=Name"
    $files = Invoke-RestMethod -Method GET -Uri $filesUri -Headers $headers -TimeoutSec 30 -MaximumRedirection 0
    if (-not (@($files.value) | Where-Object { $_.Name -eq 'Connection Test.docx' })) {
        throw 'Folder listed, but Connection Test.docx is missing. Add the synthetic onboarding document and retry.'
    }

    $fileLiteral = [uri]::EscapeDataString("$folderPath/Connection Test.docx".Replace("'", "''"))
    $fileUri = "$siteUrl/_api/web/GetFileByServerRelativeUrl('$fileLiteral')/`$value"
    $download = Invoke-WebRequest -UseBasicParsing -Method GET -Uri $fileUri -Headers $headers -TimeoutSec 30 -MaximumRedirection 0
    if ($download.Content -isnot [byte[]]) {
        throw 'The document download was not binary DOCX content. Check the login and file type.'
    }

    Add-Type -AssemblyName System.IO.Compression
    $stream = [IO.MemoryStream]::new($download.Content)
    try {
        $archive = [IO.Compression.ZipArchive]::new($stream, [IO.Compression.ZipArchiveMode]::Read)
        try {
            $entry = $archive.GetEntry('word/document.xml')
            if ($null -eq $entry) {
                throw 'The downloaded file is not a valid Word document.'
            }
            $documentStream = $entry.Open()
            try {
                $settings = [Xml.XmlReaderSettings]::new()
                $settings.DtdProcessing = [Xml.DtdProcessing]::Prohibit
                $settings.XmlResolver = $null
                $reader = [Xml.XmlReader]::Create($documentStream, $settings)
                try {
                    $document = [Xml.XmlDocument]::new()
                    $document.XmlResolver = $null
                    $document.Load($reader)
                }
                finally {
                    $reader.Dispose()
                }
            }
            finally {
                $documentStream.Dispose()
            }
        }
        finally {
            $archive.Dispose()
        }
    }
    finally {
        $stream.Dispose()
    }
    $namespaces = [Xml.XmlNamespaceManager]::new($document.NameTable)
    $namespaces.AddNamespace('w', 'http://schemas.openxmlformats.org/wordprocessingml/2006/main')
    $paragraphs = foreach ($paragraph in $document.SelectNodes('//w:p', $namespaces)) {
        ($paragraph.SelectNodes('.//w:t', $namespaces) | ForEach-Object { $_.InnerText }) -join ''
    }
    if (($paragraphs -join "`n") -cnotmatch [regex]::Escape('MGP connection test successful.')) {
        throw 'Document read, but the verification phrase does not match the synthetic test.'
    }
}

$repoRoot = Split-Path -Parent $PSScriptRoot

Write-Host ''
Write-Host 'MGP Developer Setup Check' -ForegroundColor White
Write-Host '=========================' -ForegroundColor White
Write-Host "Repository: $repoRoot"
Write-Host ''

if (Test-Path (Join-Path $repoRoot '.git')) {
    Write-Check PASS 'The current folder is a Git repository.'
}
else {
    Write-Check FAIL 'The repository metadata is missing. Clone the MGP repository before continuing.'
}

if (Test-CommandAvailable 'git') {
    $gitVersion = (& git --version 2>$null)
    Write-Check PASS "$gitVersion is available."
}
else {
    Write-Check FAIL 'Git is not available on PATH.'
}

if (Test-CommandAvailable 'az') {
    try {
        $azInfo = (& az version --output json 2>$null | ConvertFrom-Json)
        $azVersion = $azInfo.'azure-cli'
        Write-Check PASS "Azure CLI $azVersion is available."
    }
    catch {
        Write-Check WARN "Azure CLI is on PATH, but its version could not be read: $($_.Exception.Message)"
    }
}
else {
    Write-Check WARN 'Azure CLI is not available on PATH. Ask your IT administrator to install it before starting intake.'
}

$codeCommand = Get-Command 'code' -ErrorAction SilentlyContinue
if ($null -ne $codeCommand) {
    Write-Check PASS 'The VS Code command-line interface is available.'

    try {
        $extensions = @(& code --list-extensions 2>$null)
        $copilotInstalled = $extensions | Where-Object {
            $_ -in @('GitHub.copilot', 'GitHub.copilot-chat')
        }

        if ($copilotInstalled) {
            Write-Check PASS "GitHub Copilot extension detected: $($copilotInstalled -join ', ')."
        }
        else {
            Write-Check WARN 'GitHub Copilot was not found in the VS Code extension list. It may be built in, disabled, or installed in another VS Code profile.'
        }
    }
    catch {
        Write-Check WARN "Could not inspect VS Code extensions: $($_.Exception.Message)"
    }
}
else {
    Write-Check WARN 'The VS Code command-line interface is not on PATH. Open VS Code and confirm GitHub Copilot Chat manually.'
}

$recommendedExtensionsPath = Join-Path $repoRoot '.vscode\extensions.json'
if (Test-Path $recommendedExtensionsPath) {
    try {
        $recommendedExtensions = Get-Content $recommendedExtensionsPath -Raw | ConvertFrom-Json
        foreach ($extensionId in $recommendedExtensions.recommendations) {
            if ($extensions -contains $extensionId) {
                Write-Check PASS "Recommended extension detected: $extensionId."
            }
            elseif ($null -ne $codeCommand) {
                Write-Check WARN "Recommended extension is not installed in the active VS Code profile: $extensionId."
            }
        }
    }
    catch {
        Write-Check FAIL "The extension recommendation file is not valid JSON: $($_.Exception.Message)"
    }
}

$requiredFiles = @(
    '.github\copilot-instructions.md',
    '.github\agents\mgp-delivery.agent.md',
    '.github\skills\solution-intake\SKILL.md',
    '.vscode\extensions.json',
    'standards\intake-and-triage.md',
    'templates\solution-intake.md'
)

foreach ($relativePath in $requiredFiles) {
    if (Test-Path (Join-Path $repoRoot $relativePath)) {
        Write-Check PASS "$relativePath is present."
    }
    else {
        Write-Check FAIL "$relativePath is missing."
    }
}

$mcpCandidates = @(
    (Join-Path $repoRoot '.vscode\mcp.json'),
    (Join-Path $env:APPDATA 'Code\User\mcp.json')
)
$detectedMcpFiles = $mcpCandidates | Where-Object { Test-Path $_ }

if ($detectedMcpFiles) {
    foreach ($mcpFile in $detectedMcpFiles) {
        Write-Check INFO "MCP configuration file detected: $mcpFile"
    }
    Write-Check WARN 'Configuration was detected, but this script cannot prove that an approved SharePoint/Microsoft 365 tool is authenticated or authorized for the CSM folder.'
}
else {
    Write-Check WARN 'No standard MCP configuration file was detected. Your approved connection may be managed by VS Code, an extension, or organizational policy.'
}

Write-Host ''
if ($SharePointFolderUrl.Trim() -eq $script:DefaultTestFolderUrl) {
    Write-Host 'SharePoint test (read-only)' -ForegroundColor White
    try {
        Test-OnboardingSharePointConnection
        Write-Check PASS 'Test folder listed and Connection Test.docx read; verification phrase matched.'
    }
    catch {
        Write-Check FAIL "SharePoint test blocked: $($_.Exception.Message)"
    }
    Write-Host 'This checks CLI access, not whether Copilot has a SharePoint tool.'
    Write-Host ''
}
if ([string]::IsNullOrWhiteSpace($SharePointFolderUrl)) {
    Write-Host 'SharePoint access check' -ForegroundColor White
    Write-Host 'Use the onboarding Test Connection folder or your authorized CSM project folder.'
    $SharePointFolderUrl = Read-Host 'Paste folder URL (Enter to skip)'
    if (-not [string]::IsNullOrWhiteSpace($SharePointFolderUrl)) {
        Assert-SharePointFolderUrl $SharePointFolderUrl
    }
    else {
        Write-Host 'Skipped: SharePoint access is not verified.' -ForegroundColor Yellow
    }
}
Write-Host ''
Write-Host 'Next: verify access in Copilot' -ForegroundColor White
Write-Host '-----------------------------' -ForegroundColor White
Write-Host '1. Keep this repository open in VS Code.'
Write-Host '2. In Copilot Chat, select "MGP Delivery".'
Write-Host '3. Paste the prompt below into Chat, not this terminal.'
if ([string]::IsNullOrWhiteSpace($SharePointFolderUrl)) {
    Write-Host '   Replace the URL placeholder first.' -ForegroundColor Yellow
}
Write-Host ''
Write-Host '--- Copy into MGP Delivery ---' -ForegroundColor Cyan
Write-Host 'Verify read access to this approved SharePoint folder:'
if ([string]::IsNullOrWhiteSpace($SharePointFolderUrl)) {
    Write-Host '<REPLACE WITH THE APPROVED TEST OR AUTHORIZED PROJECT-FOLDER URL>'
}
else {
    Write-Host $SharePointFolderUrl.Trim()
}
Write-Host ''
Write-Host 'Use only the approved authenticated SharePoint/Microsoft 365 connection and AI-use boundary.'
Write-Host 'Actually list the folder and read its authorized documents; report whether both succeed.'
Write-Host 'For the synthetic test, read Connection Test.docx and return its verification phrase.'
Write-Host 'If the URL, connection, or permission is missing, stop and report the blocker.'
Write-Host 'Do not modify anything, start intake, expose client-sensitive content, or substitute browser/local-file access.'
Write-Host '--- End prompt ---' -ForegroundColor Cyan
Write-Host ''
Write-Host 'Success: Copilot used the approved tool to list and read; the test phrase matches.'
Write-Host 'Blocked: ask IT to enable the approved Copilot connection and folder read access.'
Write-Host 'Local checks and test-folder access do not prove access to a client project.'
Write-Host 'Never paste credentials or secrets.'
Write-Host ''

if ($script:Failed) {
    Write-Host 'Setup check failed. Resolve the FAIL items before starting intake.' -ForegroundColor Red
    exit 1
}

if ($script:Warnings -gt 0) {
    Write-Host "Local checks passed with $script:Warnings warning(s). Complete the manual checks before intake." -ForegroundColor Yellow
}
else {
    Write-Host 'Local checks passed. Complete the manual tenant-access check before intake.' -ForegroundColor Green
}

exit 0
