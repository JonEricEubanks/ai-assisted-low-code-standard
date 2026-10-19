[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$catalogPath = Join-Path $repoRoot "docs\admin\catalog.json"

$sources = @(
    @{ Category = "Skills"; Patterns = @("skills\*\SKILL.md", ".github\skills\*\SKILL.md") },
    @{ Category = "Instructions"; Patterns = @(".github\copilot-instructions.md", "AGENT_WORKFLOW.md", "CONTRIBUTING.md") },
    @{ Category = "Agents"; Patterns = @("agents\*.md", ".github\agents\*.md") },
    @{ Category = "Standards"; Patterns = @("standards\*.md") },
    @{ Category = "Templates"; Patterns = @("templates\*.md") },
    @{ Category = "QA"; Patterns = @("qa\*.md") },
    @{ Category = "Governance"; Patterns = @("governance\*.md") },
    @{ Category = "Architecture"; Patterns = @("docs\architecture\*.md") },
    @{ Category = "Training"; Patterns = @("docs\*.md", "blog\*.md") },
    @{ Category = "Planning"; Patterns = @("README.md", "requirements.md", "plan.md", "BRANCHING.md") }
)

function Get-DocumentMetadata {
    param(
        [System.IO.FileInfo]$File,
        [string]$Category
    )

    $relativePath = $File.FullName.Substring($repoRoot.Length + 1).Replace("\", "/")
    $content = [System.IO.File]::ReadAllText($File.FullName)
    $frontMatter = [regex]::Match($content, "(?s)\A---\s*\r?\n(.*?)\r?\n---")
    $nameMatch = if ($frontMatter.Success) {
        [regex]::Match($frontMatter.Groups[1].Value, "(?m)^name:\s*(.+?)\s*$")
    }
    else {
        $null
    }
    $descriptionMatch = if ($frontMatter.Success) {
        [regex]::Match($frontMatter.Groups[1].Value, "(?m)^description:\s*(.+?)\s*$")
    }
    else {
        $null
    }
    $headingMatch = [regex]::Match($content, "(?m)^#\s+(.+?)\s*$")

    if ($nameMatch -and $nameMatch.Success) {
        $title = $nameMatch.Groups[1].Value.Trim().Trim('"').Trim("'")
    }
    elseif ($headingMatch.Success) {
        $title = $headingMatch.Groups[1].Value.Trim()
    }
    else {
        $title = [System.IO.Path]::GetFileNameWithoutExtension($File.Name).Replace("-", " ")
    }

    if ($descriptionMatch -and $descriptionMatch.Success) {
        $summary = $descriptionMatch.Groups[1].Value.Trim().Trim('"').Trim("'")
    }
    else {
        $body = if ($frontMatter.Success) {
            $content.Substring($frontMatter.Length)
        }
        else {
            $content
        }
        $paragraphs = [regex]::Split($body, "\r?\n\s*\r?\n")
        $summary = $paragraphs |
            ForEach-Object { $_.Trim() } |
            Where-Object {
                $_ -and
                -not $_.StartsWith('#') -and
                -not $_.StartsWith('-') -and
                -not $_.StartsWith('|') -and
                -not $_.StartsWith('```')
            } |
            Select-Object -First 1
    }

    if (-not $summary) {
        $summary = "Open this repository resource in preview or source view."
    }

    if ($summary.Length -gt 220) {
        $summary = $summary.Substring(0, 217).TrimEnd() + "..."
    }

    [PSCustomObject]@{
        category = $Category
        title = $title
        path = $relativePath
        summary = $summary
        source = if ($relativePath.StartsWith(".github/")) { "Active Copilot customization" } else { "Governed repository source" }
    }
}

$documents = foreach ($source in $sources) {
    foreach ($pattern in $source.Patterns) {
        Get-ChildItem -Path (Join-Path $repoRoot $pattern) -File -ErrorAction SilentlyContinue |
            ForEach-Object { Get-DocumentMetadata -File $_ -Category $source.Category }
    }
}

$documents = $documents |
    Sort-Object category, title, path -Unique

$catalog = [PSCustomObject]@{
    schemaVersion = 1
    documents = @($documents)
}

$json = $catalog | ConvertTo-Json -Depth 5
$utf8WithoutBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($catalogPath, $json + [Environment]::NewLine, $utf8WithoutBom)

Write-Host "Wrote $($documents.Count) documents to $catalogPath"
