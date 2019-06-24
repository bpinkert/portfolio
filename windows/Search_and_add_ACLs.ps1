$ReferenceAccountName = ''
$Right="FullControl"
$Principal=""
$rule=new-object System.Security.AccessControl.FileSystemAccessRule($Principal,$Right,"Allow")

[string[]]$SearchDirectories = @('')

foreach ($RootDir in $SearchDirectories) {
    $DirACL = Get-Acl -Path $RootDir
    foreach ($ACL in $DirACL.Access){
        if ($ACL.IdentityReference -like $ReferenceAccountName){
            Write-Output $RootDir
        }
    }
    foreach ($Directory in (Get-ChildItem -Path $RootDir -Recurse | `
                            Where-Object -FilterScript {$_.Attributes `
                            -contains 'Directory'})){
        $DirACL = Get-Acl -Path $Directory.FullName
        foreach ($ACL in $DirACL.Access){
            if ($ACL.IdentityReference -like $ReferenceAccountName){
                Write-Output $Directory.FullName
				$acl=get-acl $Directory.FullName
				$acl.SetAccessRule($rule)
				set-acl $Directory.Fullname $acl
            }
        }
    }
}