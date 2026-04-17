param(
    [Parameter(Mandatory = $true)]
    [string]$DocPath,

    [Parameter(Mandatory = $true)]
    [string]$RepairJsonPath,

    [string]$OutputPath = ""
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $DocPath)) {
    throw "Document not found: $DocPath"
}

if (-not (Test-Path -LiteralPath $RepairJsonPath)) {
    throw "Repair JSON not found: $RepairJsonPath"
}

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $dir = Split-Path -LiteralPath $DocPath -Parent
    $base = [IO.Path]::GetFileNameWithoutExtension($DocPath)
    $ext = [IO.Path]::GetExtension($DocPath)
    $OutputPath = Join-Path $dir ($base + "_fixed" + $ext)
}

$repairSpec = Get-Content -LiteralPath $RepairJsonPath -Raw | ConvertFrom-Json
if ($repairSpec.Count -eq 0) {
    throw "Repair JSON is empty."
}

$tempDir = Join-Path $env:TEMP "codex-word-formula-repair"
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

$workPath = Join-Path $tempDir ("repair-" + [guid]::NewGuid().ToString("N") + ".docx")
Copy-Item -LiteralPath $DocPath -Destination $workPath -Force

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

try {
    $doc = $word.Documents.Open($workPath)
    $orderedRepairs = $repairSpec | Sort-Object -Property index -Descending

    foreach ($repair in $orderedRepairs) {
        $index = [int]$repair.index
        $linear = [string]$repair.linear

        if ($index -le 0 -or $index -gt $doc.OMaths.Count) {
            throw "Equation index $index is out of range. Current OMath count: $($doc.OMaths.Count)"
        }

        $range = $doc.OMaths.Item($index).Range
        $range.Text = $linear
        $range.OMaths.Add($range) | Out-Null
        $range.OMaths.BuildUp()
    }

    $doc.Save()
    $doc.Close()
}
finally {
    try { $word.Quit() } catch {}
}

Copy-Item -LiteralPath $workPath -Destination $OutputPath -Force
Remove-Item -LiteralPath $workPath -Force

Write-Output ("OUTPUT=" + $OutputPath)
