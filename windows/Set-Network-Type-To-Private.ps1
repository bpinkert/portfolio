$net = get-netconnectionprofile;Set-NetConnectionProfile -Name $net.Name -NetworkCategory Private