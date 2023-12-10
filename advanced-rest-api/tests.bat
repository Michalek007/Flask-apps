:: ################# REQUIREMENTS ###################

:: Pytest must be installed globally

:: py -m pip install pytest

:: Virtual environment with all packages defined in Pipfile.lock must be installed before executing this script

:: ##################################################

@echo OFF

call ".venv\Scripts\activate.bat"

py -m pytest
