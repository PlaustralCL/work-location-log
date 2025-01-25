import unittest
from pathlib import Path
from sqlite3 import DatabaseError
import shutil
import os
import logging


from database import Database


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data_folder = Path("./Data")
        source_file = data_folder / "test_db.db"
        cls.dest_file = data_folder / "test_db_copy.db"
        shutil.copy(source_file, cls.dest_file)
        cls.db = Database(cls.dest_file.resolve())

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        os.remove(cls.dest_file)

    def test_get_most_recent_days_default(self):
        days = self.db.get_recent_days()
        expected = 15
        self.assertEqual(len(days), expected)

    def test_get_most_recent_days_10(self):
        days = self.db.get_recent_days(10)
        expected = 10
        self.assertEqual(len(days), expected)

    def test_get_work_day(self):
        work_day = self.db.get_work_day("2024-11-25")
        self.assertEqual(work_day[0], "2024-11-25")
        self.assertEqual(work_day[2], "office")

    def test_get_work_day_not_exist(self):
        work_day = self.db.get_work_day("2024-12-25")
        self.assertIsNone(work_day)

    def test_set_location_same_location(self):
        work_day = self.db.get_work_day("2024-11-25")
        current_location = work_day[2]

        self.db.set_location(work_date="2024-11-25",
                                        new_location=current_location)
        work_day = self.db.get_work_day("2024-11-25")
        self.assertEqual(current_location, work_day[2])

    def test_set_location_new_valid_location(self):
        work_day = self.db.get_work_day("2024-11-25")
        original_location = work_day[2]
        if original_location == "office":
            new_location = 'remote'
        else:
            new_location = 'office'

        self.db.set_location(work_date="2024-11-25",
                                        new_location=new_location)
        work_day = self.db.get_work_day("2024-11-25")
        self.assertEqual(new_location, work_day[2])

    def test_set_location_invalid_location(self):
        work_day = self.db.get_work_day("2024-11-25")
        original_location = work_day[2]
        new_location = 'New York'

        with self.assertRaises(DatabaseError):
            self.db.set_location(work_date="2024-11-25",
                                 new_location=new_location)

        self.db.set_location(work_date="2024-11-25",
                             new_location=original_location)

        # Verify no change to the database
        work_day = self.db.get_work_day("2024-11-25")
        self.assertEqual(original_location, work_day[2])

    def test_set_location_invalid_date(self):
        self.db.set_location(work_date="2024-11-23",
                             new_location='office')
        self.assertIsNone(self.db.get_work_day("2024-11-23"))

    def test_set_location_error_logging(self):
        work_day = self.db.get_work_day("2024-11-25")
        self.assertEqual('office', work_day[2])
        with self.assertLogs('database', level=logging.ERROR) as cm:
            try:
                self.db.set_location(work_date="2024-11-25",
                                     new_location='New York')
                self.fail("Should have raised DatabaseError")
            except:
                if cm.output:
                    output = cm.output[0].split(":")
                    level = output[0]
                    self.assertEqual('ERROR', level)
                else:
                    self.fail("Should have logged something")

    def test_set_location_info_logging(self):
        work_day = self.db.get_work_day("2024-11-25")
        self.assertEqual('office', work_day[2])
        with self.assertLogs('database', level=logging.INFO) as cm:
            try:
                self.db.set_location(work_date="2024-11-25",
                                 new_location='remote')
                output = cm.output[0].split(":")
                level = output[0]
                self.assertEqual('INFO', level)
            except:
                self.fail("Should not have raised an exception")

    def test_new_work_day(self):
        self.assertIsNone(self.db.get_work_day("2025-01-01"))
        self.db.new_work_day(work_date="2025-01-01",
                             week_number="2025-01",
                             location="remote")
        self.assertIsNotNone(self.db.get_work_day("2025-01-01"))
        self.assertEqual(3, len(self.db.get_work_day("2025-01-01")))
        self.assertEqual("remote", self.db.get_work_day("2025-01-01")[2])

    def test_new_work_day_duplicate_day(self):
        self.assertIsNotNone(self.db.get_work_day("2024-11-19"))
        with self.assertRaises(DatabaseError):
            self.db.new_work_day(work_date="2024-11-19",
                                 week_number="2024-47",
                                 location="office")

    def test_new_work_day_invalid_location(self):
        self.assertIsNone(self.db.get_work_day("2025-01-02"))
        with self.assertRaises(DatabaseError):
            self.db.new_work_day(work_date="2025-01-02",
                                 week_number="2025-01",
                                 location="New York")
        self.assertIsNone(self.db.get_work_day("2025-01-02"))

    def test_get_year_average(self):
        self.assertEqual(2.9,self.db.get_year_average(year=2024))
        self.assertEqual(2.0, self.db.get_year_average(year=2023))








if __name__ == '__main__':
    unittest.main()



