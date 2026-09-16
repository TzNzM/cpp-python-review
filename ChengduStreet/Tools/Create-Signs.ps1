$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$projectDirectory = Split-Path -Parent $PSScriptRoot
$signDirectory = Join-Path $projectDirectory 'Assets\Resources\Signs'
New-Item -ItemType Directory -Force -Path $signDirectory | Out-Null
$signs = @(
    @{Name='tea'; Text='蓉城 · 盖碗茶'; Sub='CHENGDU TEA HOUSE'; Background='#294844'},
    @{Name='hotpot'; Text='蜀味老火锅'; Sub='SICHUAN HOT POT'; Background='#922E27'},
    @{Name='noodles'; Text='担担面 · 钟水饺'; Sub='A TASTE OF CHENGDU'; Background='#B17D41'},
    @{Name='books'; Text='巷里书屋'; Sub='BOOKS & SLOW LIVING'; Background='#394B57'},
    @{Name='coffee'; Text='少城咖啡'; Sub='SHAOCHENG COFFEE'; Background='#565A46'},
    @{Name='market'; Text='成都小吃'; Sub='LOCAL FLAVOURS'; Background='#963D2E'},
    @{Name='street'; Text='银杏街'; Sub='YINXING ST.'; Background='#23585C'}
)
foreach ($sign in $signs) {
    $width = if ($sign.Name -eq 'street') {1024} else {2048}
    $bitmap = New-Object System.Drawing.Bitmap($width,256)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $graphics.Clear([System.Drawing.ColorTranslator]::FromHtml($sign.Background))
    $ink = New-Object System.Drawing.SolidBrush([System.Drawing.ColorTranslator]::FromHtml('#F1D8A0'))
    $pen = New-Object System.Drawing.Pen($ink,3)
    $graphics.DrawRectangle($pen,12,12,($width-24),232)
    $font = New-Object System.Drawing.Font('Microsoft YaHei',100,[System.Drawing.FontStyle]::Bold,[System.Drawing.GraphicsUnit]::Pixel)
    $small = New-Object System.Drawing.Font('Segoe UI',27,[System.Drawing.FontStyle]::Regular,[System.Drawing.GraphicsUnit]::Pixel)
    $format = New-Object System.Drawing.StringFormat
    $format.Alignment = [System.Drawing.StringAlignment]::Center
    $format.LineAlignment = [System.Drawing.StringAlignment]::Center
    $graphics.DrawString($sign.Text,$font,$ink,[System.Drawing.RectangleF]::new(20,25,($width-40),143),$format)
    $graphics.DrawString($sign.Sub,$small,$ink,[System.Drawing.RectangleF]::new(20,176,($width-40),44),$format)
    $bitmap.Save((Join-Path $signDirectory ($sign.Name+'.png')),[System.Drawing.Imaging.ImageFormat]::Png)
    $format.Dispose(); $font.Dispose(); $small.Dispose(); $pen.Dispose(); $ink.Dispose(); $graphics.Dispose(); $bitmap.Dispose()
}
Write-Output "Created $($signs.Count) Chinese sign textures."
