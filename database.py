from datetime import date
import sqlite3

class Database:
    def __init__(self):
        self.con = sqlite3.connect('Data/worklocation.db')
        self.con.execute('PRAGMA foreign_keys = ON')
        self.cur = self.con.cursor()

    def get_recent_days(self, num_of_days: int = 15) -> list:
        """
        Queries the database and returns the location data about the most
        recent work days. The number of days is determined by the num_of_days
        parameter. It defaults to 15 days, (approximately 3 weeks of data).
        Returns a list of tuples. Each tuple is of the form (work_date, location)
        :param num_of_days: The number of days to return. The default value is 15.
        :return: A list of tuples, where tuple is of the form (work_date, location).
        """
        # noinspection SqlNoDataSourceInspection
        res = self.cur.execute(
            """
            SELECT work_date, location
            FROM WorkDay
            ORDER BY work_date DESC
            Limit ?;
            """, (num_of_days,)
        )
        return res.fetchall()

    def set_location(self, work_date: str, new_location: str) -> None:
        """
        Sets the location of the provided work_date. If work_date is not a date
        that is already in the database, nothing will happen.
        :param work_date: The work date that will be revised
        :param new_location: The new location to set
        :raises IntegrityError: If new_location is not in the Location table
        """
        try:
        # noinspection SqlNoDataSourceInspection
            self.cur.execute(
                """
                UPDATE WorkDay
                SET location = ?
                WHERE work_date = ?
                """, (new_location, work_date)
            )
        except (sqlite3.IntegrityError, sqlite3.DatabaseError) as err:
            print(f"Unexpected {err=}")
            print(f"work_date={work_date}, new_location={new_location}")
            raise

        self.con.commit()

    def get_work_day(self, work_date: str) -> tuple:
        """
        Gets the work day information of the provided work_date
        :param work_date: ISO formatted date string
        :return: tuple of the row from the WorkDay table: (work_date, week_number, location)
        """
        # noinspection SqlNoDataSourceInspection
        res = self.cur.execute(
            """
            SELECT 
                work_date, 
                week_number, 
                location
            FROM WorkDay
            WHERE work_date = ?
            """, (work_date,)
        )
        return res.fetchone()

    def close_connection(self) -> None:
        """
        Closes the connection to the database.
        """
        self.con.close()
