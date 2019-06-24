$outarray = @()
$outarray2 = @()

$AllMailBox = Get-Mailbox   -OrganizationalUnit "example.com/" -resultsize unlimited

ForEach ($MailBox in $AllMailbox) 
	{
		$a = Get-mailboxstatistics -Identity $Mailbox.PrimarySmtpAddress.Address |  Select-Object AssociatedItemCount, DeletedItemCount, DisplayName, ItemCount, LastLoggedOnUserAccount, LastLogoffTime, LastLogonTime, TotalDeletedItemSize, TotalItemSize, Database, ServerName, DatabaseName, IsArchiveMailbox 
		$outarray += $a
	}
	
$outarray | Export-CSV -path C:\temp\Mailboxes_A.csv -Encoding ascii -NoTypeInformation 

ForEach ($MailBox in $AllMailbox) 
	{
		$b = Get-Recipient -Identity  $Mailbox.PrimarySmtpAddress.Address | Select-Object SamAccountName, PrimarySmtpAddress
		$outarray2 += $b
	}

$outarray2 | Export-CSv -path C:\temp\Mailboxes_B.csv -Encoding ASCII -NoTypeInformation