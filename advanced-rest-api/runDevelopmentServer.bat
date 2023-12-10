:: ################# REQUIREMENTS ###################

:: Virtual environment with all packages defined in Pipfile.lock must be installed

:: ##################################################

@echo OFF

call ".venv\Scripts\activate.bat"

start run_client.py

run.py
