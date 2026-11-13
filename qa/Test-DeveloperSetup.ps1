$ErrorActionPreference = 'Stop'
$setupPath = Join-Path (Split-Path -Parent $PSScriptRoot) 'scripts\Test-DeveloperSetup.ps1'
$tokens = $null
$parseErrors = $null
$ast = [Management.Automation.Language.Parser]::ParseFile($setupPath, [ref] $tokens, [ref] $parseErrors)
if ($parseErrors.Count -gt 0) {
    throw 'Setup script has PowerShell syntax errors.'
}
$functionAst = $ast.Find({
    param($node)
    $node -is [Management.Automation.Language.FunctionDefinitionAst] -and
        $node.Name -eq 'Test-OnboardingSharePointConnection'
}, $false)
$commandAst = $ast.Find({
    param($node)
    $node -is [Management.Automation.Language.FunctionDefinitionAst] -and
        $node.Name -eq 'Invoke-M365SetupCommand'
}, $false)
. ([scriptblock]::Create($commandAst.Extent.Text))
. ([scriptblock]::Create($functionAst.Extent.Text))
$constantAssignments = $ast.FindAll({
    param($node)
    $node -is [Management.Automation.Language.AssignmentStatementAst] -and
        $node.Left.Extent.Text -match '^\$script:(DefaultTestFolderUrl|Onboarding\w+)$'
}, $false)
foreach ($assignment in $constantAssignments) {
    . ([scriptblock]::Create($assignment.Extent.Text))
}

function Assert-True {
    param([bool] $Condition, [string] $Message)
    if (-not $Condition) { throw $Message }
}

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

function Test-CommandAvailable { return $script:CliAvailable }
function Write-Host {}
function Read-Host { throw 'The check must not prompt in the terminal.' }
function m365 {
    $global:LASTEXITCODE = $script:CliExitCode
    if ($args[0] -eq 'status') {
        if ($script:SignedOut) { return '"Logged out"' }
        return '{"connectedAs":"tester@example.invalid","authType":"Browser","appId":"' + $script:ActiveAppId + '"}'
    }
    if ($args[0] -eq 'login') {
        Assert-True ($args[1] -eq '--authType' -and $args[2] -eq 'browser') 'Sign-in must use the browser, not passwords or secrets.'
        Assert-True ($args[4] -eq $script:OnboardingAppId -and $args[6] -eq $script:OnboardingTenantId) 'Login must use the read-only onboarding app and tenant.'
        $script:LoginCalls += 1
        $global:LASTEXITCODE = $script:LoginExitCode
        Write-Error 'Synthetic CLI progress or error must not reach the user.' -ErrorAction Continue
        if ($script:LoginExitCode -eq 0) {
            $script:SignedOut = $false
            $script:ActiveAppId = $script:OnboardingAppId
        }
        return
    }
    Assert-True ($args[0] -eq 'util' -and $args[1] -eq 'accesstoken' -and $args[2] -eq 'get') 'Unexpected CLI operation.'
    if ($script:TokenFailure) { $global:LASTEXITCODE = 1 }
    return 'synthetic-token'
}
function Invoke-RestMethod {
    param($Method, $Uri, $Headers, $TimeoutSec, $MaximumRedirection)
    Assert-True ($Method -eq 'GET' -and $MaximumRedirection -eq 0) 'Only non-redirecting GET requests are allowed.'
    Assert-True ($Uri.StartsWith("$script:OnboardingSiteUrl/_api/web/GetFolderByServerRelativeUrl(")) 'Unexpected folder endpoint.'
    Assert-True ([uri]::UnescapeDataString($Uri).Contains("('$script:OnboardingFolderPath')/Files?")) 'Request escaped the test library.'
    $script:Requests += 1
    if ($script:DenyAccess) { throw 'Synthetic HTTP 403.' }
    return @{ value = @(@{ Name = $script:FileName }) }
}
function Invoke-WebRequest {
    param([switch] $UseBasicParsing, $Method, $Uri, $Headers, $TimeoutSec, $MaximumRedirection)
    Assert-True ($Method -eq 'GET' -and $MaximumRedirection -eq 0) 'Only non-redirecting GET requests are allowed.'
    Assert-True ([uri]::UnescapeDataString($Uri).EndsWith("$script:OnboardingFolderPath/Connection Test.docx')/`$value")) 'Download escaped the test document.'
    $script:Requests += 1
    return @{ Content = $script:DocumentBytes }
}

$xmlPrefix = '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p>'
$xmlSuffix = '</w:p></w:body></w:document>'
$script:CliAvailable = $true
$script:CliExitCode = 0
$script:FileName = 'Connection Test.docx'
$script:DenyAccess = $false
$script:TokenFailure = $false
$script:SignedOut = $false
$script:ActiveAppId = $script:OnboardingAppId
$script:LoginCalls = 0
$script:LoginExitCode = 0
$script:Requests = 0
$script:DocumentBytes = New-TestDocument ($xmlPrefix + '<w:r><w:t>MGP connection </w:t></w:r><w:r><w:t>test successful.</w:t></w:r>' + $xmlSuffix)
Test-OnboardingSharePointConnection
Assert-True ($script:Requests -eq 2 -and $script:LoginCalls -eq 0) 'An existing onboarding login must be reused without signing in again.'

$script:SignedOut = $true
$script:Requests = 0
Test-OnboardingSharePointConnection
Assert-True ($script:LoginCalls -eq 1 -and $script:Requests -eq 2) 'Signed-out users must sign in once and continue automatically.'

$script:ActiveAppId = 'provisioning-app'
$script:LoginCalls = 0
$script:Requests = 0
Test-OnboardingSharePointConnection
Assert-True ($script:LoginCalls -eq 1 -and $script:Requests -eq 2) 'A different active app must never be used for the read-only test.'

foreach ($case in @('missing-cli', 'browser-login-failed', 'failed-status', 'failed-token', 'denied', 'missing-file', 'wrong-phrase', 'invalid-docx')) {
    $script:CliAvailable = $case -ne 'missing-cli'
    $script:CliExitCode = if ($case -eq 'failed-status') { 1 } else { 0 }
    $script:DenyAccess = $case -eq 'denied'
    $script:TokenFailure = $case -eq 'failed-token'
    $script:SignedOut = $case -eq 'browser-login-failed'
    $script:ActiveAppId = $script:OnboardingAppId
    $script:LoginExitCode = if ($case -eq 'browser-login-failed') { 1 } else { 0 }
    $script:LoginCalls = 0
    $script:FileName = if ($case -eq 'missing-file') { 'Other.docx' } else { 'Connection Test.docx' }
    $script:DocumentBytes = if ($case -eq 'invalid-docx') {
        [Text.Encoding]::UTF8.GetBytes('not a zip archive')
    }
    else {
        New-TestDocument ($xmlPrefix + '<w:r><w:t>Not the expected verification phrase.</w:t></w:r>' + $xmlSuffix)
    }
    $script:Requests = 0
    $failure = $null
    try { Test-OnboardingSharePointConnection }
    catch { $failure = $_ }
    Assert-True ($null -ne $failure) "$case must fail explicitly."
    if ($case -eq 'browser-login-failed') {
        Assert-True ($failure.Exception.Message.Contains('Browser sign-in did not complete')) 'Failed browser sign-in must give the specific blocker.'
        Assert-True ($script:LoginCalls -eq 1) 'A failed login must not loop or retry automatically.'
    }
    if ($case -in @('missing-cli', 'browser-login-failed', 'failed-status', 'failed-token')) {
        Assert-True ($script:Requests -eq 0) "$case must not access SharePoint."
    }
    if ($case -in @('denied', 'missing-file')) {
        Assert-True ($script:Requests -eq 1) "$case must stop before downloading."
    }
}
Write-Output 'PASS: onboarding-app reuse, automatic sign-in, and app switching succeed; eight blocker cases fail safely.'
