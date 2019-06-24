for /d %d in (%systemdrive%\users\*) do rd /s /q %d\appdata\local\temp
for /d %d in (%systemdrive%\users\*) do rd /s /q %d\appdata\local\microsoft\windows\tempor~1
for /d %d in (%systemdrive%\docume~1\*) do rd /s /q %d\locals~1\temp
for /d %d in (%systemdrive%\docume~1\*) do rd /s /q %d\locals~1\tempor~1
--rem clean up firefox cache 
for /d %d in (%systemdrive%\users\*) do del /s /q %d\appdata\local\mozilla\firefox\profiles\
--rem clean up chrome cache 
for /d %d in (%systemdrive%\users\*) do del /s /q %d\"appdata\local\google\chrome\user data\default\cache\"
--rem clean up msft edge cache 
for /d %d in (%systemdrive%\users\*) do del /s /q %d\appdata\local\Packages\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\AC\#!001\Temp\
--rem clean up inet explorer cache 
for /d %d in (%systemdrive%\users\*) do del /s /q %d\appdata\local\Microsoft\Windows\INetCache\
--rem the rest are system cleanups 
rd /s /q "%systemdrive%\temp"
rd /s /q "%windir%\temp"
rd /s /q %systemroot%\SoftwareDistribution\Download\
del /s /q %windir%\prefetch
del /s /q %systemdrive%\*.hdmp
del /s /q %systemdrive%\*.dmp
cleanmgr /sagerun:200