$AllMailBox = Get-Mailbox   -OrganizationalUnit "example.com/" -resultsize unlimited

ForEach ($MailBox in $AllMailbox) 
	{
		$a = Get-MailboxStatistics -Identity $Mailbox.PrimarySmtpAddress.Address| Sort-Object TotalItemSize -Descending | fl DisplayName,@{label="TotalItemSize(GB)";expression={"$([math]::round($_.TotalItemSize.Value.ToBytes() /1Gb, 2)) GB"}} , ItemCount
		write-host $a
	}

