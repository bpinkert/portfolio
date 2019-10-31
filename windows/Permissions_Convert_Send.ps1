[string[]]$SearchDirectories = @('')
$rawpath = ''
$decoded = ''

foreach ($RootDir in $SearchDirectories) {
    $DirACL = Get-Acl -Path $RootDir
    foreach ($ACL in $DirACL.Access){
        Write-Output $RootDir | Tee-Object -FilePath $rawpath -Append
        Write-Output $DirACL | Select-Object AccessToSTring | fl AccessToString | Tee-Object -FilePath $rawpath -Append
		
    foreach ($Directory in (Get-ChildItem -Path $RootDir -Recurse -Depth 1 | `
                            Where-Object -FilterScript {$_.Attributes `
                            -contains 'Directory'})){
        $DirACL = Get-Acl -Path $Directory.FullName
        Write-Output $Directory.FullName | Tee-Object -FilePath $rawpath -Append
        Write-Output $DirACL | Select-Object AccessToString | fl AccessToString | Tee-Object -FilePath $rawpath -Append
            
    }
}
}

Get-Content $rawpath | Set-Content -Encoding Ascii $decoded

C:\apex\format_raw_logs\format_permissions_raw.exe --file C:\temp\test_dec.txt --output C:\temp\test.xlsx

$Username = "";
$Password = "";
$path = "";

function Send-ToEmail([string]$email, [string]$attachmentpath){

    $message = new-object Net.Mail.MailMessage;
    $message.From = "";
    $message.To.Add($email);
    $message.Subject = "";
    $message.Body = "Permissions Audit Report attached, in excel format"
    $attachment = New-Object Net.Mail.Attachment($attachmentpath);
    $message.Attachments.Add($attachment);

    $smtp = new-object Net.Mail.SmtpClient("smtp.office365.com", "587");
    $smtp.EnableSSL = $true;
    $smtp.Credentials = New-Object System.Net.NetworkCredential($Username, $Password);
    $smtp.send($message);
    write-host "Mail Sent" ; 
    $attachment.Dispose();
 }
del $rawpath
del $decoded
del $path
