[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$script:Failed = $false
$script:Warnings = 0

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
    $azOutput = & az version --output json 2>$null
    try {
        if ($LASTEXITCODE -ne 0) {
            Write-Check WARN "Azure CLI version check failed with exit code $LASTEXITCODE."
        }
        elseif ([string]::IsNullOrWhiteSpace(($azOutput -join '').Trim())) {
            Write-Check WARN 'Azure CLI version check returned no version information.'
        }
        else {
            $azInfo = $azOutput | ConvertFrom-Json
            $azVersion = $azInfo.'azure-cli'
            if ([string]::IsNullOrWhiteSpace([string]$azVersion)) {
                Write-Check WARN 'Azure CLI version information does not include azure-cli.'
            }
            else {
                Write-Check PASS "Azure CLI $azVersion is available."
            }
        }
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
Write-Host 'Manual checks required' -ForegroundColor White
Write-Host '----------------------' -ForegroundColor White
Write-Host '1. Open this repository as the active VS Code workspace.'
Write-Host '2. Open GitHub Copilot Chat and select "MGP Delivery" from the agent picker.'
Write-Host '3. Confirm an approved SharePoint/Microsoft 365 tool appears and can list the CSM project folder.'
Write-Host '4. Do not paste credentials or tenant secrets into chat or repository files.'
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
