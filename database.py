import logging
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)
# TODO: Add file for logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(funcName)s >>> %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    )

# TODO: Log changes to the database
class Database:
    def __init__(self, file_path: Path = Path('Data/worklocation.db')) -> None:
        """
        Creates a connection to the database. The connection should be closed
        it is no longer needed by using the close() method.
        :param file_path: A path the database file. A default path is using
        worklocation.db is used is no parameter is passed.
        """

        self.con = sqlite3.connect(str(file_path))
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
            logger.error(f"{err=}. work_date={work_date} new_location={new_location}")
            raise

        self.con.commit()

    def get_work_day(self, work_date: str) -> tuple[str, str, str]:
        """
        Gets the work day information of the provided work_date
        :param work_date: ISO formatted date string, yyyy-mm-dd
        :return: Returns a tuple of the WorkDay table, (work_date, week_number, location),
        if the work_date is present in the database. Otherwise, returns None.
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

    def new_work_day(self, work_date: str, week_number: str, location: str) -> None:
        """
        Sets the work day information of the provided work_date
        :param work_date: A date string in the format yyyy-mm-dd
        :param week_number: Week number string in the format yyyy-ww
        :param location: Location string. Needs to match one of the existing
        locations in the Location table.
        :raises IntegrityError: If work_date already exists or if week_number
        or location is not are not in the Week or Location tables.
        """

        try:
        # noinspection SqlNoDataSourceInspection
            self.cur.execute(
                """
                INSERT INTO WorkDay
                VALUES (?, ?, ?)
                """,(work_date, week_number, location)
            )
        except(sqlite3.IntegrityError, sqlite3.DatabaseError) as err:
            logger.error(f"{err=}. work_date={work_date} week_number={week_number} location={location}")
            raise

        self.con.commit()

    def close(self) -> None:
        """
        Closes the connection to the database.
        """
        self.con.close()
