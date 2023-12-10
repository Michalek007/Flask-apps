# Advanced rest-api

**Complete Flask application template, with sample functionalities.**

Composed of two elements:
* **rest-api**
* **client**

## Requirements

Python 3.8+

## Installation

First, clone this repository.

    $ git clone https://github.com/Michalek007/Flask-apps.git

After, to install virtual environment with all necessary packages run:

    $ venvSetup.bat


## Starting Application

To run development server run:
    
    $ runDevelopementServer.bat

To run production server run:
    
    $ runw.bat

To run production server run with console launch:
    
    $ run.bat

To see your application, access this url in your browser: 

	http://127.0.0.1:5000

Or different url defined in `configuration.py` as variable `LISTENER`.

## Application development

To activate virtual environment in terminal run:
    
    $ ".venv\Scripts\activate.bat"

To install new package run:
    
    $ pipenv install <package_name>

 
## Project structure
    
Advanced-rest-api is dived into subdirectories which contains:
* **app** - Flask app, blueprints and api methods 
* **client** - BlockingScheduler, components and client methods
* **tests** - tests for all service functionalities
* **utils** - utility classes
* **scripts** - Batch scripts used by service

All configuration is in: `configuration.py`. 
Configuration, requirements and run files are placed in the main directory.
