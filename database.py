import logging
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)
# TODO: Add file for logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s.%(funcName)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    )

# TODO: Log changes to the database
class Database:
    """
    Manage all queries to the database.
    """
    def __init__(self, file_path: Path = Path('Data/worklocation.db')) -> None:
        """
        Creates a connection to the database. The connection should be closed
        it is no longer needed by using the close() method.
        :param file_path: A path the database file. A default path of
        'Data/worklocation.db' is used if no parameter is passed.
        """

        self.con = sqlite3.connect(str(file_path))
        self.con.execute('PRAGMA foreign_keys = ON')
        self.cur = self.con.cursor()

    def get_weekly_summary(self, start_week: str, end_week: str) -> list[tuple]:
        """
        Returns a list of tuples, where each tuple has the first date of the
        week, the last date of the week, and the number of days in the office
        for that week.
        :param start_week: First week to collect data, in 'yyyy-ww' format
        :param end_week: Last week to collect data, in 'yyyy-ww' format.
        :return: List of tuples, where each tuple has the first date of the
                week, the last date of the week, and the number of days in the
                office for that week. Each tuple is (week number, week start
                date, week end date, office count)
        """

        # noinspection SqlNoDataSourceInspection
        res = self.cur.execute(
            """
            SELECT 
                w.week_number, 
                w.week_start, 
                w.week_end, 
                COUNT(
                        CASE
                            WHEN wd.location = 'office' THEN 1
                            ELSE NULL	
                        END
                    ) as office_count
            FROM 
                Week AS w 
                LEFT OUTER JOIN WorkDay AS wd ON w.week_number = wd.week_number
            WHERE 
                w.week_number >= ? AND 
                w.week_number <= ? 
            GROUP BY w.week_number
           """, (start_week, end_week)
        )
        weeks = res.fetchall()
        return weeks

    def get_recent_days(self, num_of_days: int = 15) -> list[tuple[str, str]]:
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
        logger.info(f"work_date={work_date} new_location={new_location}")

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

    def get_locations(self) -> list[str]:
        """
        Gets the locations from the location table.
        :return: List of allowed locations
        """

        # noinspection SqlNoDataSourceInspection
        res = self.cur.execute(
            """
            SELECT location
            FROM Location
            """
        )
        locations = []
        for location in res.fetchall():
            locations.append(location[0])
        return locations

    def new_work_day(self, work_date: str, week_number: str, location: str) -> None:
        """
        Sets the work day information of the provided work_date
        :param work_date: A date string in the format yyyy-mm-dd
        :param week_number: Week number string in the format yyyy-ww
        :param location: Location string. Needs to match one of the existing
        locations in the Location table.
        :raises IntegrityError: If work_date already exists or if week_number
        or location are not in the Week or Location tables.
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
        logger.info(f"work_date={work_date} week_number={week_number} location={location}")

    def get_ytd_average(self, year: int, end_week: str) -> float :
        """Get the weekly average for the given year, through the current date.
        If the year is complete, the average will be for the full year.
        A week is determined to be in a given year based on the year of ISO
        week.
        :param year: The year to calculate the average for
        :param end_week: The last week to include in the calculation, in ISO
        week format: yyyy-ww
        :return: The weekly average for the given year. If the year is not in
        the database, None is returned. If there is no data for the given range,
        None is returned. If the end_week is before the provided year, None is
        returned.
        """
        start_week = str(year) + "-01"

        # noinspection SqlNoDataSourceInspection
        res = self.cur.execute(
            """
            SELECT AVG(office_count)
            FROM (
                SELECT 
                    w.week_number,
                    COUNT(
                        CASE
                            WHEN wd.location = 'office' THEN 1
                            ELSE NULL	
                        END
                    ) as office_count                    
                FROM Week as w LEFT OUTER JOIN WorkDay as wd on w.week_number = wd.week_number
                WHERE 
                    w.week_number BETWEEN ? AND ?
                GROUP BY w.week_number
            )            
           """, (start_week, end_week)
        )
        return res.fetchone()[0]

    def get_weekly_count(self, week_number: str) -> int :
        """Returns the count of office days for the provided week.
        :param week_number: The week to get the count of. The week is in the
        format yyyy-ww
        :return: The count of office days for the given week
        """

        # noinspection SqlNoDataSourceInspection
        res = self.cur.execute(
            """
            SELECT COUNT(work_date)
            FROM WorkDay
            WHERE 
                week_number = ? AND
                location = 'office'
            """, (week_number,)
        )
        return res.fetchone()[0]

    def close(self) -> None:
        """
        Closes the connection to the database.
        """
        self.con.close()
