import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import date

from database import Database

class DailyInput(tk.Tk):
    """
    Stand alone tkinter widget to collect the office location each day.
    Creates a window with buttons to choose the work location for the current
    day. The location is then inserted into the database.
    """
    def __init__(self):
        super().__init__()
        self.db = Database()

        # GUI
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
        Updates the database with the given location. If a location has
        already been saved for the current work_date, then a message box is
        shown and no updates to the database are made. Use the recent_days_view
        if a revision to the location is needed.
        :param location: The work location for the current work day.
        """
        work_date = self.today.isoformat()
        iso_year = str(self.today.isocalendar().year)
        iso_week = self.today.isocalendar().week
        week_number = f'{iso_year}-{iso_week:>02}'
        if not self.db.get_work_day(work_date=work_date):
            self.db.new_work_day(work_date=work_date,
                                 week_number=week_number,
                                 location=location)
        else:
            messagebox.showinfo(message=f"A location for {work_date} was already recorded.")

        self.db.close()
        self.destroy()

    def on_close(self):
        self.db.close()
        root.destroy()


if __name__ == "__main__":
    root = DailyInput()
    root.protocol("WM_DELETE_WINDOW", root.on_close)
    root.mainloop()