@echo off
echo Starting up project...

pushd "%~dp0" > NUL
set BASE_DIR=%~dp0
popd > NUL

echo.BASE_DIR : %BASE_DIR%

::--------------------------------------------------------
:: Main
::--------------------------------------------------------

call cd %BASE_DIR%
set OPT_ENV_FORCE=%1
echo.OPT_ENV_FORCE : %OPT_ENV_FORCE%
if "%OPT_ENV_FORCE%x" == "-fx" (
  python "%BASE_DIR%manage.py" "clean"
)

python "%BASE_DIR%manage.py" "prepare"

call :build_venv
%BASE_DIR%env\Scripts\nosetests.exe

echo.&pause&goto:eof


::--------------------------------------------------------
::-- Function definition starts below here
::--------------------------------------------------------

:logging
echo "[INFO] %*"
goto :eof


:build_venv
if not exist env (
  virtualenv env
)
call env\Scripts\activate
call pip install -r requirements.txt
call pip install -r test-requirements.txt
exit /b

PAUSE
