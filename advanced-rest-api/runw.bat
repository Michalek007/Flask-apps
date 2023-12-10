:: ################# REQUIREMENTS ###################

:: Virtual environment with all packages defined in Pipfile.lock must be installed

:: ##################################################

@echo OFF

call ".venv\Scripts\activate.bat"

start pythonw run_client.py

start pythonw server.py

exit