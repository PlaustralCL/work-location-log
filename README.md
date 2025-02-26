# Work Location Tracker

## Overview
For hybrid workers who need to be in the office a minimum number of times each week.
This is a simple method to log your location, office or remote, each day.
You can also add days that were missed or revise a day if the wrong location was recorded.
It is intended to be used with a scheduling tool, such as Task Scheduler on Widows to run at a set time or based on startup.


## Goal
The goal of this project was to make a Python GUI app that only used native python functionality.
There are no packages imported from other repositories.

## Installation
The simplest way to install is to just clone the repo.
```
git clone https://github.com/PlaustralCL/work-location.git
```
Otherwise, you can just copy the files that you want.
You can initialize an empty database using db_setup.py. 
The default setup assumes there is a `./Data/location.csv` file that will be imported into the database.
If that will not be used, you can comment out that line in db_setup.py.
The file `./Data/location.csv` is assumed to be in the format "Year,Month,Day,Location" and contain a header row.


When db_setup.py is initially run, an SQLite file will be created, if one does not already exist.
The default database is `./Data/worklocation.db`.
A log file is created at `./Data/work_location_log.txt`.

A test database is provided and can bue used with the `test_database.py` file to run tests on the database queries.

