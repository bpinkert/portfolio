[string[]]$SearchDirectories = @('C:\')

foreach ($RootDir in $SearchDirectories) {
    $DirACL = Get-Acl -Path $RootDir
    foreach ($ACL in $DirACL.Access){
        Write-Output $RootDir
        Write-Output $DirACL.AccessToString
        Write-Output "---- Folder Separator ----"
		
    foreach ($Directory in (Get-ChildItem -Path $RootDir -Recurse -Depth 2 | `
                            Where-Object -FilterScript {$_.Attributes `
                            -contains 'Directory'})){
        $DirACL = Get-Acl -Path $Directory.FullName
        Write-Output $Directory.FullName
		$acl=get-acl $Directory.FullName
		Write-Output $acl.AccessToString
        Write-Output "---- Folder Separator ----"
            
    }
}
}	