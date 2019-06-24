# Fields: 
#AssociatedItemCount                        
#DeletedItemCount                           
#DisplayName                                
#ItemCount                                  
#LastLoggedOnUserAccount                    
#LastLogoffTime                             
#LastLogonTime                              
#TotalDeletedItemSize                       
#TotalItemSize                              
#Database                                   
#ServerName                                 
#DatabaseName                               
#IsArchiveMailbox                           
#SamAccountName
#PrimarySmtpAddress



# https://stackoverflow.com/questions/33407839/add-column-from-a-variable-to-select-object-results

# https://stackoverflow.com/questions/20858133/output-powershell-variables-to-a-text-file#20858374

$outarray = @()

$AllMailBox = Get-Mailbox   -OrganizationalUnit "" -resultsize unlimited

ForEach ($MailBox in $AllMailbox) 
	{
		$a = Get-mailboxstatistics -Identity $Mailbox.PrimarySmtpAddress.Address |  Select-Object AssociatedItemCount, DeletedItemCount, DisplayName, ItemCount, LastLoggedOnUserAccount, LastLogoffTime, LastLogonTime, TotalDeletedItemSize, TotalItemSize, Database, ServerName, DatabaseName, IsArchiveMailbox 
		$outarray += $a
	}
	
$outarray | Export-CSV -path C:\temp\test3.csv -Encoding ascii -NoTypeInformation 

# https://stackoverflow.com/questions/17022017/add-column-to-csv-windows-powershell

ForEach ($Mailbox in $AllMailBox)
	{
		Import-Csv -path C:\temp\test3.csv | 
		$b = Get-Recipient -Identity  $Mailbox.PrimarySmtpAddress.Address | 
		Select-Object SamAccountName, PrimarySmtpAddress,@{Name='SamAccountName';Expression={$b.SamAccountName}}, @{Name='PrimarySmtpAddress';Expression={$b.PrimarySmtpAddress}} |
		Export-CSV -path C:\temp\test4.csv
	}




