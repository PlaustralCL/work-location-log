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


## Start
To run the app, run `work_location.py`
To facilitate daily data collection, there is a small "widget" that just collects the work location for the day and then closes.
The widget is launched from the `daily_input.py`.
It will show a small window that shows the current date and large buttons to allow the user to choose recording the location as "office" or "remote".
Once the location is selected, the window will close automatically. This work flow is the simplest to automate.

## Logging
Changes and attempted changes to the database are tracked in a log file.
The default location for the log file is `./Data/work_location_log.txt`.
The location can be changed in the `database.py` file.

## Testing
A test database is provided and can be used with the `test_database.py` file to run tests on the database queries. Tests are only provided for the database queries since that is where the majority of work is done. The rest of the app is just the GUI.

