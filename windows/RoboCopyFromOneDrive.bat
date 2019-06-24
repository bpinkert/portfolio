@ECHO Off

set HR=%time:~0,2%
set HR=%Hr: =0% 
set HR=%HR: =%

if exist Z:\ (
ECHO Z drive is available 
GOTO :START
) else (
ECHO Z drive is not currently available. 
GOTO :STOP
)


:START
if exist "C:\RoboCopyLogs\OneDriveSyncLog.txt" (
ECHO OneDriveSyncLog log exists, Renaming OneDriveSyncLog
GOTO Rename-OneDriveSyncLog
) else (
ECHO No Existing OneDriveSyncLog File - Going to OneDriveSync
GOTO OneDriveSync
)

:Rename-OneDriveSyncLog
rename C:\RoboCopyLogs\OneDriveSyncLog.txt OneDriveSyncLog._%date:~10,4%-%date:~4,2%-%date:~7,2%_%HR%%time:~3,2%.txt

:OneDriveSync
REM Connecting to Z: drive with a wait time to allow for Zee drive to access cloud share
dir z:\ > c:\RoboCopyLogs\Dir-of-Z1.txt
timeout /t 30 > timeout-output.txt
dir z:\ > c:\RoboCopyLogs\Dir-of-Z2.txt
ECHO Copying OneDrive Data
robocopy C:\Users\daves\OneDrive "Z:\OneDriveBackup" /SEC /E /X /R:2 /W:2 /LOG:c:\RoboCopyLogs\OneDriveSyncLog.txt

:STOP
ECHO Can't copy OneDrive data because Z Drive is not available. 
