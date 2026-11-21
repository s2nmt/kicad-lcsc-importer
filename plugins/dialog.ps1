$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
[Windows.Forms.Application]::EnableVisualStyles()

$form = New-Object Windows.Forms.Form
$form.Text = 'Import LCSC'
$form.ClientSize = [Drawing.Size]::new(560, 203)
$form.FormBorderStyle = 'FixedDialog'
$form.MaximizeBox = $false
$form.MinimizeBox = $false
$form.StartPosition = 'CenterScreen'
$form.TopMost = $true

function Add-Control($type, $label, $x, $y, $width) {
    $control = New-Object "Windows.Forms.$type"
    $control.Text = $label
    $control.Location = [Drawing.Point]::new($x, $y)
    $control.Width = $width
    $form.Controls.Add($control)
    return $control
}

$null = Add-Control Label 'LCSC ID' 12 17 95
$part = Add-Control TextBox '' 110 14 350
$null = Add-Control Label 'Library name' 12 53 95
$libraryName = Add-Control TextBox $env:LCSC_IMPORTER_LIBRARY_NAME 110 50 350
$null = Add-Control Label 'Library folder' 12 89 95
$documentsHome = $env:KICAD_DOCUMENTS_HOME
if (-not $documentsHome) {
    $documentsHome = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'KiCad'
}
$defaultFolder = Join-Path $documentsHome '10.0\libs'
$folder = Add-Control TextBox $defaultFolder 110 86 350
$browse = Add-Control Button 'Browse...' 468 84 80
$overwrite = Add-Control CheckBox 'Overwrite existing library entries' 110 121 350
$import = Add-Control Button 'Import' 380 161 80
$cancel = Add-Control Button 'Cancel' 468 161 80

$browse.Add_Click({
    $picker = New-Object Windows.Forms.FolderBrowserDialog
    try {
        $picker.SelectedPath = $folder.Text
        if ($picker.ShowDialog($form) -eq 'OK') { $folder.Text = $picker.SelectedPath }
    } finally { $picker.Dispose() }
})
$import.DialogResult = 'OK'
$cancel.DialogResult = 'Cancel'
$form.AcceptButton = $import
$form.CancelButton = $cancel
$form.Add_Shown({ $part.Select() })

try {
    if ($form.ShowDialog() -eq 'OK') {
        @{
            part = $part.Text
            library_name = $libraryName.Text
            folder = $folder.Text
            overwrite = $overwrite.Checked
        } | ConvertTo-Json -Compress
    }
} finally { $form.Dispose() }
