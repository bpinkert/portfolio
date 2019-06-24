for /d %d in (%systemdrive%\users\*) do rd /s /q %d\appdata\local\temp
for /d %d in (%systemdrive%\users\*) do rd /s /q %d\appdata\local\microsoft\windows\tempor~1
for /d %d in (%systemdrive%\users\*) do rd /s /q %d\appdata\local\temp
for /d %d in (%systemdrive%\users\*) do rd /s /q %d\appdata\local\microsoft\windows\tempor~1
for /d %d in (%systemdrive%\docume~1\*) do rd /s /q %d\locals~1\temp
for /d %d in (%systemdrive%\docume~1\*) do rd /s /q %d\locals~1\tempor~1
for /d %d in (%systemdrive%\users\*) do del /s /q %d\appdata\local\mozilla\firefox\profiles\
for /d %d in (%systemdrive%\users\*) do del /s /q %d\appdata\local\google\chrome\user data\default\cache\
rmdir /s /q "%systemdrive%\temp"
rmdir /s /q "%windir%\temp"
rmdir /s /q %systemroot%\SoftwareDistribution\Download\
del /s /q %windir%\prefetch
del /s /q %systemdrive%\*.hdmp
del /s /q %systemdrive%\*.dmp
del /s /q %systemdrive%\*.hdmp
del /s /q %systemdrive%\*.dmp