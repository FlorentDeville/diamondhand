@echo off
set MYSQL_ROOT=C:\wamp64\bin\mysql\mysql8.2.0\bin

set DB_NAME=wallstreet

REM Get current date
For /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%b-%%a-%%c)
For /f "tokens=1-2 delims=/:" %%a in ("%TIME%") do (set mytime=%%a-%%b)
set DATETIME=%mydate%_%mytime%

set OUTPUT=C:\Workspace\diamondhand\db_backup\history\%DB_NAME%_backup_%DATETIME%.sql

%MYSQL_ROOT%\mysqldump.exe --databases %DB_NAME% --result-file %OUTPUT% --user root

echo Dump saved in %OUTPUT%
pause
