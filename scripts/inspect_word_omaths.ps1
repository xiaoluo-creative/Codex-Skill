param(
    [Parameter(Mandatory = $true)]
    [string]$DocPath
)

$ErrorActionPreference = "Stop"

$wdStatisticPages = 2
$wdActiveEndAdjustedPageNumber = 1

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

try {
    $doc = $word.Documents.Open($DocPath, $false, $true)

    Write-Output ("DOC=" + $DocPath)
    Write-Output ("PAGES=" + $doc.ComputeStatistics($wdStatisticPages))
    Write-Output ("PARAS=" + $doc.Paragraphs.Count)
    Write-Output ("OMATH=" + $doc.OMaths.Count)

    $i = 1
    foreach ($eq in $doc.OMaths) {
        $page = $eq.Range.Information($wdActiveEndAdjustedPageNumber)
        $text = $eq.Range.Text -replace "[\r\n]+", " "
        Write-Output ("EQ" + $i + " PAGE=" + $page + " TEXT=" + $text)
        $i++
    }

    $doc.Close()
}
finally {
    try { $word.Quit() } catch {}
}
