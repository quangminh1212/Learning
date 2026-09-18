param(
  [Parameter(Mandatory=$true)]
  [string[]]$Path
)

Add-Type -AssemblyName System.IO.Compression.FileSystem

foreach ($pptx in $Path) {
  $full = [System.IO.Path]::GetFullPath($pptx)
  $zip = [System.IO.Compression.ZipFile]::OpenRead($full)
  try {
    Write-Output "`n=== $full ==="
    $slideEntries = $zip.Entries | Where-Object { $_.FullName -match '^ppt/slides/slide(\d+)\.xml$' } | Sort-Object { [int]([regex]::Match($_.FullName, 'slide(\d+)').Groups[1].Value) }
    foreach ($entry in $slideEntries) {
      $number = [int]([regex]::Match($entry.FullName, 'slide(\d+)').Groups[1].Value)
      $stream = $entry.Open()
      try {
        $xml = New-Object System.Xml.XmlDocument
        $xml.Load($stream)
        $ns = New-Object System.Xml.XmlNamespaceManager($xml.NameTable)
        $ns.AddNamespace('a','http://schemas.openxmlformats.org/drawingml/2006/main')
        $texts = @($xml.SelectNodes('//a:t', $ns) | ForEach-Object { $_.InnerText })
        Write-Output "[SLIDE $number]"
        if ($texts.Count) { Write-Output ($texts -join ' | ') }
      } finally { $stream.Dispose() }
    }
  } finally { $zip.Dispose() }
}
