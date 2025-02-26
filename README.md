# Work Location Tracker

## Overview
A simple tool for people who need to track how many times they work in-person each week.
For example, hybrid workers who need to be in the office a minimum number of times each week.
This app provides a simple method to log your location each day, make updates to the log, and some basic reporting.
It is intended to be used with a scheduling tool, such as Task Scheduler on Widows, to run at a set time or based on startup.

## Goal
Implement a Python GUI using only native Python functionality. This meant that Tkinter was used for the GUI and unittest was used for testing.
There are no packages imported from other repositories such as pip.

## Installation
The simplest way to install is to just clone the repo.
```
git clone https://github.com/PlaustralCL/work-location.git
```
Otherwise, you can just copy the files that you want.

## Setup
You can initialize an empty database using `db_setup.py`. 
The default setup assumes there is a `./Data/location.csv` file that will be imported into the database.
If that will not be used, you can comment out that line in `db_setup.py`.
The file `./Data/location.csv` is assumed to be in the format "Year,Month,Day,Location" and contain a header row.

When `db_setup.py` is initially run, an SQLite file will be created, if one does not already exist.
The default location for the database file is `./Data/worklocation.db`.
A log file is created at `./Data/work_location_log.txt`.

## Start
To run the app, run `work_location.py`

## Testing
A test database is provided and can be used with the `test_database.py` file to run tests on the database queries. Tests are only provided for the database queries since that is where the majority of work is done. The rest of the app is just the GUI.

