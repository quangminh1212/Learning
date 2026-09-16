$ErrorActionPreference = "Stop"
try {
    $app = [System.Runtime.InteropServices.Marshal]::GetActiveObject("MSProject.Application")
    Write-Host "Attached to running Project"
} catch {
    Write-Host "GetActiveObject failed: $_"
    $app = New-Object -ComObject MSProject.Application
}

$app.Visible = $true
$srcDir = "C:\Dev\Learning\VIII.HUST\Quản trị dự án\Mẫu\QLDA_BTCN_202490069_BuiQuocLuyt"
$outDir = "C:\Dev\Learning\tmp"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$files = Get-ChildItem -LiteralPath $srcDir -Filter "*.mpp"
foreach ($f in $files) {
    Write-Host "===== OPEN $($f.Name) ====="
    $app.FileOpen($f.FullName)
    Start-Sleep -Seconds 1
    $proj = $app.ActiveProject

    $info = @()
    $info += "FILE=$($f.Name)"
    $info += "Name=$($proj.Name)"
    $info += "Title=$($proj.Title)"
    $info += "Subject=$($proj.Subject)"
    $info += "Author=$($proj.Author)"
    $info += "Manager=$($proj.Manager)"
    $info += "Company=$($proj.Company)"
    $info += "Comments=$($proj.Comments)"
    $info += "Start=$($proj.ProjectStart)"
    $info += "Finish=$($proj.ProjectFinish)"
    $info += "Calendar=$($proj.Calendar.Name)"
    $info += "MinutesPerDay=$($proj.MinutesPerDay)"
    $info += "TaskCount=$($proj.Tasks.Count)"
    $info += "ResourceCount=$($proj.Resources.Count)"
    $info += ""
    $info += "ID`tUID`tOutline`tName`tDuration`tStart`tFinish`tPredecessors`tCritical`tTotalSlack`tFreeSlack`tSummary`tWBS"
    foreach ($t in $proj.Tasks) {
        if ($null -eq $t) { continue }
        $line = "{0}`t{1}`t{2}`t{3}`t{4}`t{5}`t{6}`t{7}`t{8}`t{9}`t{10}`t{11}`t{12}" -f `
            $t.ID, $t.UniqueID, $t.OutlineLevel, ($t.Name -replace "`t"," "), $t.Duration, $t.Start, $t.Finish, `
            $t.Predecessors, $t.Critical, $t.TotalSlack, $t.FreeSlack, $t.Summary, $t.WBS
        $info += $line
    }

    $txtPath = Join-Path $outDir ($f.BaseName + ".txt")
    $info | Set-Content -LiteralPath $txtPath -Encoding UTF8
    $xmlPath = Join-Path $outDir ($f.BaseName + ".xml")
    try {
        $app.FileSaveAs($xmlPath, 21)
        Write-Host "Saved XML $xmlPath"
    } catch {
        Write-Host "XML save failed: $_"
    }
    $app.FileClose(0)
    Write-Host "Wrote $txtPath"
}

Write-Host "DONE"
