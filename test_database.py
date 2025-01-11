import unittest
from pathlib import Path
from sqlite3 import DatabaseError
import shutil
import os


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

        # reset database to original condition
        self.db.set_location(work_date="2024-11-25",
                             new_location=original_location)

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








if __name__ == '__main__':
    unittest.main()



