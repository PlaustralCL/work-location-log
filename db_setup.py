import csv
import sqlite3
from datetime import date
from datetime import timedelta

def create_tables() -> None:
    """
    Creates the tables in the database. If the database file doesn't exist, it
    will be created.
    """

    con = sqlite3.connect('./Data/worklocation.db')
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()

    # noinspection SqlNoDataSourceInspection
    cur.execute(
        """
         CREATE TABLE IF NOT EXISTS Week (
            week_number TEXT NOT NULL, 
            week_start TEXT NOT NULL, 
            week_end TEXT NOT NULL,
            PRIMARY KEY (week_number)
        );   
        """)

    # noinspection SqlNoDataSourceInspection
    cur.execute(
        """
         CREATE TABLE IF NOT EXISTS Location (
            location TEXT NOT NULL PRIMARY KEY
        );   
        """)

    # noinspection SqlNoDataSourceInspection
    cur.execute(
        """
         CREATE TABLE IF NOT EXISTS WorkDay (
            work_date TEXT NOT NULL,
            week_number TEXT NOT NULL,
            location TEXT NOT NULL,
            notes TEXT NULL, 
            PRIMARY KEY (work_date),
            FOREIGN KEY (week_number) REFERENCES Week (week_number),
            FOREIGN KEY (location) REFERENCES Location (location)
        );   
        """)

    con.close()

def fill_week_table(start_year: int, end_year: int) -> None:
    """
    Initialize the Week table with data from the years 2023 - 2025.
    """

    data = generate_week_data(start_year, end_year)

    con = sqlite3.connect('./Data/worklocation.db')
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()

    # noinspection SqlNoDataSourceInspection
    cur.executemany(
        """
        INSERT OR IGNORE INTO
            Week(week_number, week_start, week_end)
            VALUES (?, ?, ?)
        """, data
    )
    con.commit()
    con.close()

def generate_week_data(start_year: int, end_year: int) -> list:
    """
    Generates the week data used to populate the Week table. The data range
    is the first ISO week of the start_year to the last ISO week of the year
    before end_year. The end_year is not inclusive.
    :param start_year: Four digit year. The start date will be the first day of
    the first ISO week of the start year. This means the first day may be in the
    previous calendar year.
    :param end_year: Four digit year. The end_year is not inclusive.
    :return: List of week tuples, where each tuple is (week_number, week_start, week_end).
    The week number is in the format yyyy-ww. The week_start and week_end are Python dates.
    """

    start_date = date.fromisocalendar(year=start_year, week=1, day=1)
    working_date = start_date
    data = []
    while working_date.isocalendar().year < end_year:
        iso_year = str(working_date.isocalendar().year)
        iso_week = str(working_date.isocalendar().week)
        iso_week = f"{iso_week:>02}"
        week_number = f"{iso_year}-{iso_week}"
        week_start = working_date
        week_end = working_date + timedelta(days=6)
        week = (week_number, week_start.isoformat(), week_end.isoformat())
        data.append(week)

        working_date += timedelta(days=7)
    return data

def fill_location_table() -> None:
    """
    Initialize the Location table
    """
    locations = [('office',), ('remote',)]

    con = sqlite3.connect('./Data/worklocation.db')
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()

    # noinspection SqlNoDataSourceInspection
    cur.executemany(
        """
        INSERT OR IGNORE INTO 
            Location(location) 
            VALUES(?)
        """, locations
    )
    con.commit()
    con.close()

def fill_workday_table() -> None:
    """
    Initialize the WorkDay table from the data in the
    location.csv file.
    """
    data = []
    with open('Data/location.csv', "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            year = int(row["Year"])
            month = int(row["Month"])
            day = int(row["Day"])
            work_date = date(year, month, day)

            iso_year = str(work_date.isocalendar().year)
            iso_week = str(work_date.isocalendar().week)
            iso_week = f"{iso_week:>02}"
            week_number = f"{iso_year}-{iso_week}"

            work_date = work_date.isoformat()
            location = row["Location"]
            work_day = (work_date, week_number, location)
            data.append(work_day)

    con = sqlite3.connect('./Data/worklocation.db')
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()

    # noinspection SqlNoDataSourceInspection
    cur.executemany(
        """
        INSERT OR IGNORE INTO 
            WorkDay(work_date, week_number, location) 
            VALUES (?, ?, ?)
        """, data
    )
    con.commit()
    con.close()

if __name__ == '__main__':
    create_tables()
    fill_week_table(start_year=2023, end_year=2027)
    fill_location_table()
    fill_workday_table()


