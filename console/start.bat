@echo off

ECHO :: Welcome to Silo console client ::
ECHO.

SET inputFolder=input
set /p inputFolder=Enter packets folder location [press enter for "input"]:

SET outputFolder=output
set /p outputFolder=Enter output folder location [press enter for "output"]:

SET projectId=
SET projectIdParam=-projectId
set /p projectId=Enter project handle [Leave empty if only one project]:
if "%projectId%"==""  SET projectIdParam=

:CLEANOUTPUT
SET /P CLEANOUTPUT=Clean output folder (y/n) (WARNING : this will delete files in output folder) ? [press enter for "n"]
if "%CLEANOUTPUT%"=="y" SET CLEANOUTPUT=-cleanOutput
if "%CLEANOUTPUT%"=="Y" SET CLEANOUTPUT=-cleanOutput
if "%CLEANOUTPUT%"=="n" SET CLEANOUTPUT=
if "%CLEANOUTPUT%"=="N" SET CLEANOUTPUT=
if "%CLEANOUTPUT%"==""  SET CLEANOUTPUT=

:FACILE
SET /P FACILE=Include facile validation on server (y/n) ? [press enter for "n"]
if "%FACILE%"=="y" SET FACILE=-facileValidation
if "%FACILE%"=="Y" SET FACILE=-facileValidation
if "%FACILE%"=="n" SET FACILE=
if "%FACILE%"=="N" SET FACILE=
if "%FACILE%"==""  SET FACILE=

:REPLACE
SET /P REPLACE=Replace metadata or data+metadata (y/n) ? [press enter for "n"]
if "%REPLACE%"=="y" SET REPLACE=-replace
if "%REPLACE%"=="Y" SET REPLACE=-replace
if "%REPLACE%"=="n" SET REPLACE=
if "%REPLACE%"=="N" SET REPLACE=
if "%REPLACE%"==""  SET REPLACE=

IF "%REPLACE%"=="" GOTO EMAIL

:UPDATEDATA_ONLY
SET /P UPDATEDATA_ONLY=Update data files only (y/n) ? [press enter for "n"]
if "%UPDATEDATA_ONLY%"=="y" SET UPDATEDATA_ONLY=-updateDataOnly
if "%UPDATEDATA_ONLY%"=="Y" SET UPDATEDATA_ONLY=-updateDataOnly
if "%UPDATEDATA_ONLY%"=="n" SET UPDATEDATA_ONLY=
if "%UPDATEDATA_ONLY%"=="N" SET UPDATEDATA_ONLY=
if "%UPDATEDATA_ONLY%"==""  SET UPDATEDATA_ONLY=

:EMAIL
set /p email=Enter email address:
if "%email%"=="" GOTO EMAIL

:APIKEY
SET apiKeyFile=
set /p apiKeyFile=Enter api key file location [press enter for "nakala-key.txt"]:
if "%apiKeyFile%"==""  SET apiKeyFile=nakala-key.txt

rem echo java -jar nakala-console.jar -email %email% -inputFolder %inputFolder% -outputFolder %outputFolder% %projectIdParam% %projectId% -apiKeyFile %apiKeyFile% %FACILE% %CLEANOUTPUT% %METADATAREPLACE% %DATAREPLACE%

java -jar nakala-console.jar -email %email% -inputFolder %inputFolder% -outputFolder %outputFolder% %projectIdParam% %projectId% -apiKeyFile %apiKeyFile% %FACILE% %CLEANOUTPUT% %REPLACE% %UPDATEDATA_ONLY%
pause