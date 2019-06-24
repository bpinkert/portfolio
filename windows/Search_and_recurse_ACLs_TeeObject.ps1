[string[]]$SearchDirectories = @('')
$rawpath = ''
$decoded = ''

foreach ($RootDir in $SearchDirectories) {
    $DirACL = Get-Acl -Path $RootDir
    foreach ($ACL in $DirACL.Access){
        Write-Output $RootDir | Tee-Object -FilePath $rawpath -Append
        Write-Output $DirACL | Select-Object AccessToString | fl AccessToString | Tee-Object -FilePath $rawpath -Append
		
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