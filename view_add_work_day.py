import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import date
from datetime import timedelta

import constants
from database import Database
import ytd_html_report

class AddWorkDay(tk.Frame):
    """
    Create a frame that allows a work day to be added. The user can select the
    date and the location that will be added to the database.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.db = Database()

        self.btn_style = ttk.Style()
        self.btn_style.configure('daily_input.TButton',
                                 font=("TkDefaultFont", constants.label_size))
        self.radio_style = ttk.Style()
        self.radio_style.configure("radio.TRadiobutton", font=('TkDefaultFont', constants.label_size))

        self.title_label = ttk.Label(self, text="Add Work Day", font=("Arial", constants.title_size))
        self.title_label.grid(column=1, row=1, columnspan=2)

        self.working_date = date.today()
        self.date_label = ttk.Label(self,
                                    text=f"{self.working_date}",
                                    padding=10,
                                    font=("TkDefaultFont", constants.label_size))
        self.plus_date_btn = ttk.Button(self,
                                        text="+",
                                        style='daily_input.TButton',
                                        command=lambda: self.adjust_working_date(direction="add"))

        self.minus_date_btn = ttk.Button(self,
                                         text="-",
                                         style='daily_input.TButton',
                                         command=lambda: self.adjust_working_date(direction="minus"))

        self.date_label.grid(column=1, row=2, columnspan=2)
        self.minus_date_btn.grid(column=1, row=3)
        self.plus_date_btn.grid(column=2, row=3)

        self.radio_location = tk.StringVar(self)
        self.radio_office = ttk.Radiobutton(self,
                                            text="Office",
                                            variable=self.radio_location,
                                            style='radio.TRadiobutton',
                                            value='office',
                                            )
        self.radio_remote = ttk.Radiobutton(self,
                                            text="Remote",
                                            variable=self.radio_location,
                                            style='radio.TRadiobutton',
                                            value='remote')
        self.radio_office.grid(column=1, row=4)
        self.radio_remote.grid(column=2, row=4)

        self.submit_btn = ttk.Button(self,
                                     text="Submit",
                                     style='daily_input.TButton',
                                     command=lambda: self.set_location(self.radio_location.get()))
        self.submit_btn.grid(column=1, row=5, columnspan=2)

    def refresh(self):
        self.working_date = date.today()
        self.date_label.configure(text=f"{self.working_date}")

    def adjust_working_date(self, direction: str) -> None:
        """Changes the working date based on the provided direction and updates
        the date label accordingly.
        :param direction: The direction for the change of working date. The
        only allowed values are 'add' and 'minus'
        """
        if str(direction) == "add":
            self.working_date += timedelta(days=1)
        elif str(direction) == "minus":
            self.working_date -= timedelta(days=1)
        self.date_label.configure(text=f"{self.working_date}")


    def set_location(self, location: str) -> None:
        """
        Updates the database with the given location. If a location has
        already been saved for the current work_date, then a message box is
        shown and no updates to the database are made. If updating the database
        is successful, a message box will show that. Use the recent_days_view
        if a revision to the location is needed. Returns immediately if no
        location is provided or if the provided location is not in the
        Location table of the database.
        :param location: The work location for the current work day.
        """
        if location == '' or location not in self.db.get_locations():
            return

        work_date = self.working_date.isoformat()
        iso_year = str(self.working_date.isocalendar().year)
        iso_week = self.working_date.isocalendar().week
        week_number = f'{iso_year}-{iso_week:>02}'
        if not self.db.get_work_day(work_date=work_date):
            self.db.new_work_day(work_date=work_date,
                                 week_number=week_number,
                                 location=location)
            messagebox.showinfo(
                message=f"Date: {self.working_date}\nLocation: {location.title()}\nAdded to the database")
            self.refresh()
        else:
            messagebox.showerror(message=f"A location for {work_date} was already recorded.",)

        ytd_html_report.generate_report()

    def on_close(self):
        self.db.close()
        root.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Recent Days View")
    root.geometry("500x500")
    frame = AddWorkDay(root)
    root.protocol("WM_DELETE_WINDOW", frame.on_close)
    frame.pack()
    root.mainloop()
