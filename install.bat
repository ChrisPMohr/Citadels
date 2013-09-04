REM Select current version of virtualenv:
SET VERSION=1.10.1

REM Name of virtual environment:
SET ENV=env

REM Set to whatever python interpreter you will be used to make the 
REM virutal environment:
FOR /F "tokens=* USEBACKQ" %%F IN (`where.exe python`) DO (
SET PYTHON=%%F
)

REM Set to the location of zip utility:
REM virutal environment:
FOR /F "tokens=* USEBACKQ" %%F IN (`where.exe 7z`) DO (
SET ZIP="%%F"
)

SET URL_BASE=https://pypi.python.org/packages/source/v/virtualenv

REM --- Real work starts here ---
BITSADMIN /TRANSFER env_download /DOWNLOAD /PRIORITY FOREGROUND ^
%URL_BASE%/virtualenv-%VERSION%.tar.gz %~dp0virtualenv-%VERSION%.tar.gz

%ZIP% x virtualenv-%VERSION%.tar.gz
%ZIP% x dist/virtualenv-%VERSION%.tar

REM Create the virtual environment.
%PYTHON% virtualenv-%VERSION%\virtualenv.py %ENV%

REM Install requirements
CALL %ENV%\Scripts\activate.bat
pip install -r requirements.txt

REM Clean up
DEL virtualenv-%VERSION%.tar.gz
RMDIR /S /Q dist
RMDIR /S /Q virtualenv-%VERSION%
