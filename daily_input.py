import sys
import tkinter as tk
from tkinter import ttk
from datetime import date
import sqlite3

class DailyInput(tk.Tk):
    """
    Stand alone tkinter widget to collect the office location each day.
    Creates a window with buttons to choose the work location for the current
    day. The location is then inserted into the database.
    """
    def __init__(self):
        super().__init__()

        self.title("Daily Input")
        self.geometry("175x150")
        self.resizable(width=False, height=False)

        self.btn_style = ttk.Style()
        self.btn_style.configure('daily_input.TButton',
                                 font=("TkDefaultFont", 20))

        self.today = date.today()
        self.date_label = ttk.Label(self,
                                    text=f"{self.today}",
                                    padding=10,
                                    font=("TkDefaultFont", 20))
        self.date_label.pack()

        self.office_btn = ttk.Button(self,
                                     text="Office",
                                     style='daily_input.TButton',
                                     command=lambda: self.set_location('office'))
        self.office_btn.pack(fill='x')

        self.remote_btn = ttk.Button(self,
                                     text="Remote",
                                     style='daily_input.TButton',
                                     command=lambda: self.set_location('remote'))
        self.remote_btn.pack(fill='x')


    def set_location(self, location: str) -> None:
        """
        Updates the database with the given location.
        :param location: The work location for the current work day.
        """
        year = self.today.year
        month = self.today.month
        day = self.today.day
        iso_year = str(self.today.isocalendar().year)
        iso_week = self.today.isocalendar().week
        week_number = f'{iso_year}-{iso_week}'
        work_day = (year, month, day, week_number, location)

        con = sqlite3.connect('worklocation.db')
        con.execute('PRAGMA foreign_keys = ON')
        cur = con.cursor()

        # noinspection SqlNoDataSourceInspection
        cur.execute(
            """
            INSERT OR IGNORE INTO
                WorkDay(year, month, day, week_number, location)
                VALUES (?, ?, ?, ?, ?)
            """, work_day
        )
        con.commit()
        con.close()
        sys.exit(0)

if __name__ == "__main__":
    root = DailyInput()
    root.mainloop()