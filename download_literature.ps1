$ErrorActionPreference = 'Continue'
$dest = 'D:\lmy-graduate\workspace\docs\mynotes\literature'
New-Item -ItemType Directory -Force -Path $dest | Out-Null

$papers = @(
  @{ Name='Bourhis_2026_TFT_Backplane_Chronic_Neural_Interfaces.pdf'; Urls=@() },
  @{ Name='Zhou_2025_High_Density_OECT_Brain_Mapping.pdf'; Urls=@('https://pubs.rsc.org/ak/content/articlepdf/2025/tc/d4tc02839b?page=search') },
  @{ Name='Garcia_Cortadella_2021_Graphene_Active_Sensor_Arrays.pdf'; Urls=@('https://epub.ub.uni-muenchen.de/74847/1/s41467-020-20546-w.pdf','https://www.nature.com/articles/s41467-020-20546-w.pdf') },
  @{ Name='Jung_2025_BISC_65536_Electrodes.pdf'; Urls=@('https://sld.cs.columbia.edu/pubs/jung_nature25.pdf','https://escholarship.org/content/qt9b21w2xd/qt9b21w2xd_noSplash_ceb1f406312677e778010f302b65c2b0.pdf') },
  @{ Name='Uguz_2024_Flexible_Switch_Matrix_OECT_pn_Diode.pdf'; Urls=@('https://bioee.ee.columbia.edu/wp-content/uploads/2024/10/s41467-023-44024-1.pdf','https://repository.kaust.edu.sa/bitstreams/558ce41d-647f-4c92-b761-327247321659/download','https://www.nature.com/articles/s41467-023-44024-1.pdf') },
  @{ Name='Porto_Cruz_2025_Crosstalk_Brain_Recordings.pdf'; Urls=@('https://www.nature.com/articles/s41467-025-59391-0.pdf') },
  @{ Name='Fathy_2022_JSSC_Digitally_Assisted_Multiplexed_Neural_Recording.pdf'; Urls=@('https://escholarship.org/content/qt61z008bz/qt61z008bz.pdf') },
  @{ Name='Fathy_2024_TBCAS_Chopper_TDMA_Neural_Recording.pdf'; Urls=@('https://iebl.ucsd.edu/sites/default/files/iebl/2024-02/A_0.00179_mm2_Ch_Chopper-Stabilized_TDMA_Neural_Recording_System_with_Dynamic_EOV_Cancellation_and_Predictive_Mixed-Signal_Impedance_Boosting.pdf') },
  @{ Name='Jain_2025_JSSC_In_Pixel_Digitization_ECoG.pdf'; Urls=@('https://iebl.ucsd.edu/sites/default/files/iebl/2025-01/A_2.520_kS_s_In-Pixel_Direct_Digitization_ECoG_Front_End_With_Submillisecond_Stimulation_Artifact_Recovery.pdf') },
  @{ Name='Cisneros_Fernandez_2021_TBCAS_1024_Channel_GFET_ROIC.pdf'; Urls=@('https://ddd.uab.cat/record/309383/files/') }
)

$results = @()
foreach ($p in $papers) {
  $target = Join-Path $dest $p.Name
  $success = $false
  $used = ''
  if (Test-Path -LiteralPath $target) {
    $stream = [System.IO.File]::OpenRead($target)
    try {
      $header = New-Object byte[] 5
      $count = $stream.Read($header,0,5)
      $success = ($count -eq 5 -and [Text.Encoding]::ASCII.GetString($header) -eq '%PDF-')
    } finally { $stream.Dispose() }
    if (-not $success) { Remove-Item -LiteralPath $target -Force }
  }
  if (-not $success) {
    foreach ($url in $p.Urls) {
      $temp = "$target.part"
      if (Test-Path -LiteralPath $temp) { Remove-Item -LiteralPath $temp -Force }
      Write-Host "TRY $($p.Name) $url"
      & curl.exe -L --fail --silent --show-error --retry 1 --retry-delay 2 --max-time 75 -A 'Mozilla/5.0' -o $temp $url
      if ($LASTEXITCODE -eq 0 -and (Test-Path -LiteralPath $temp)) {
        $stream = [System.IO.File]::OpenRead($temp)
        try {
          $header = New-Object byte[] 5
          $count = $stream.Read($header,0,5)
          $success = ($count -eq 5 -and [Text.Encoding]::ASCII.GetString($header) -eq '%PDF-')
        } finally { $stream.Dispose() }
        if ($success) {
          Move-Item -LiteralPath $temp -Destination $target -Force
          $used = $url
          break
        }
      }
      if (Test-Path -LiteralPath $temp) { Remove-Item -LiteralPath $temp -Force }
    }
  }
  if ($success) { $status='downloaded'; $bytes=(Get-Item -LiteralPath $target).Length } else { $status='unavailable'; $bytes=0 }
  Write-Host "$status $($p.Name) $bytes"
  $results += [pscustomobject]@{Status=$status;File=$p.Name;Bytes=$bytes;Source=$used}
}
$results | Export-Csv -LiteralPath (Join-Path $dest 'download_status.csv') -Encoding UTF8 -NoTypeInformation
