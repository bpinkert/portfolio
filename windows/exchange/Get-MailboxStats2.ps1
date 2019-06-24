# https://stackoverflow.com/questions/17022017/add-column-to-csv-windows-powershell

$AllMailBox = Get-Mailbox   -OrganizationalUnit "example.com/" -resultsize unlimited

ForEach ($Mailbox in $AllMailBox)
	{
		Import-Csv -path C:\temp\test3.csv | 
		$a = Get-Recipient -Identity  $Mailbox.PrimarySmtpAddress.Address | 
		Select-Object SamAccountName
		$b = Get-Recipient -Identity $Mailbox.PrimarySmtpAddress.Address | Select-Object PrimarySmtpAddress.Address |
		@{Name='SamAccountName';Expression={$a}}, @{Name='PrimarySmtpAddress';Expression={$b.}} |
		Export-CSV -path C:\temp\test4.csv
	}
 
