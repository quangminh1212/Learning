$ErrorActionPreference = "Stop"
$app = New-Object -ComObject MSProject.Application
$app.Visible = $false
$app.DisplayAlerts = $false

$srcDir = "C:\Dev\Learning\VIII.HUST\Quản trị dự án\Mẫu\QLDA_BTCN_202490069_BuiQuocLuyt"
$outDir = "C:\Dev\Learning\tmp"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$files = Get-ChildItem -LiteralPath $srcDir -Filter "*.mpp"
foreach ($f in $files) {
    Write-Host "===== OPEN $($f.Name) ====="
    $app.FileOpen($f.FullName)
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
    $info += "MinutesPerWeek=$($proj.MinutesPerWeek)"
    $info += "DaysPerMonth=$($proj.DaysPerMonth)"
    $info += "StatusDate=$($proj.StatusDate)"
    $info += "CurrentDate=$($proj.CurrentDate)"
    $info += "TaskCount=$($proj.Tasks.Count)"
    $info += "ResourceCount=$($proj.Resources.Count)"
    $info += ""
    $info += "ID`tUID`tOutline`tName`tDuration`tStart`tFinish`tPredecessors`tSuccessors`tCritical`tTotalSlack`tFreeSlack`tMilestone`tSummary`tWBS`tNotes"
    foreach ($t in $proj.Tasks) {
        if ($null -eq $t) { continue }
        $line = "{0}`t{1}`t{2}`t{3}`t{4}`t{5}`t{6}`t{7}`t{8}`t{9}`t{10}`t{11}`t{12}`t{13}`t{14}`t{15}" -f `
            $t.ID, $t.UniqueID, $t.OutlineLevel, ($t.Name -replace "`t"," "), $t.Duration, $t.Start, $t.Finish, `
            $t.Predecessors, $t.Successors, $t.Critical, $t.TotalSlack, $t.FreeSlack, $t.Milestone, $t.Summary, $t.WBS, `
            (($t.Notes -replace "`r|`n"," ") )
        $info += $line
    }

    $info += ""
    $info += "=== RESOURCES ==="
    foreach ($r in $proj.Resources) {
        if ($null -eq $r) { continue }
        $info += "{0}`t{1}`t{2}`t{3}" -f $r.ID, $r.Name, $r.Type, $r.MaxUnits
    }

    $info += ""
    $info += "=== CALENDARS ==="
    foreach ($c in $proj.BaseCalendars) {
        $info += "Calendar=$($c.Name)"
    }

    $xmlPath = Join-Path $outDir ($f.BaseName + ".xml")
    $txtPath = Join-Path $outDir ($f.BaseName + ".txt")
    $info | Set-Content -LiteralPath $txtPath -Encoding UTF8
    try {
        $app.FileSaveAs($xmlPath, 21)  # pjMSPDI = 21 XML
    } catch {
        Write-Host "XML save failed: $_"
    }
    $app.FileClose(0)
    Write-Host "Wrote $txtPath"
}

$app.Quit(0)
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($app) | Out-Null
Write-Host "DONE"
