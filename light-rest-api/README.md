# Light REST-API

**Complete Flask application template, with useful plugins.**

It contains:
* user authentication with flask-login
* database created using SQLAlchemy
* CRUD for computer performance (params)
* periodic tasks with APScheduler
* tests for api methods with pytest

## Requirements

Python 3.8+

## Installation

First, clone this repository.

    $ git clone https://github.com/Michalek007/Flask-apps.git

After, to install virtual environment with all necessary packages run:

    $ venvSetup.bat

## Starting Application

To run development server run:
    
    $ py run.py

To run production server run:
    
    $ run.bat

or

    $ py server.py

To see your application, access this url in your browser: 

	http://127.0.0.1:5000

Or different url defined in `configuration.py` as variable `LISTENER`.

## Application development

To activate virtual environment in terminal run:
    
    $ ".venv\Scripts\activate.bat"

To install new package run:
    
    $ pipenv install <package_name>

## Project structure
    
Rest-api is dived into subdirectories which contains:
* **app** - Flask app, blueprints and api methods, periodic tasks
* **database** - SQLAlchemy database, schemas, cli commands and data.db 
* **tests** - tests for all service functionalities
* **utils** - utility classes

All configuration is in: `configuration.py`. 
Configuration, requirements and run files are placed in the main directory.