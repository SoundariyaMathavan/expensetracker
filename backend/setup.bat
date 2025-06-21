@echo off
echo Running setup script from parent directory...
cd ..
python setup.py
echo.
echo If setup was successful, activate the environment with:
echo ..\venv\Scripts\activate
echo.
pause