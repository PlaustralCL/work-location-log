import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import date
from datetime import timedelta

import constants
from database import Database


class DashboardView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.db = Database()

        title_label = ttk.Label(self, text="Dashboard", font=("TkDefaultFont", constants.title_size))
        title_label.grid(column=0, row=0, columnspan=2)

        ytd_label = ttk.Label(self, text="YTD average:", font=("TkDefaultFont", constants.label_size))
        ytd_label.grid(row=1, column=0, padx=10, pady=10)

        curr_week_label = ttk.Label(self, text="Current week:", font=("TkDefaultFont", constants.label_size))
        curr_week_label.grid(row=2, column=0, padx=10, pady=10)

        self.update()

    def update(self):
        iso_year = date.today().isocalendar().year
        previous_iso_week = (date.today() - timedelta(weeks=1)).isocalendar().week
        previous_week_number = f"{iso_year}-{previous_iso_week:>02}"
        current_iso_week = date.today().isocalendar().week
        current_week_number = f"{iso_year}-{current_iso_week:>02}"

        ytd_average = self.db.get_ytd_average(year=iso_year, end_week=previous_week_number)
        current_week_count = self.db.get_weekly_count(week_number=current_week_number)

        ytd_data_label = ttk.Label(self, text=f"{ytd_average:.2f}", font=("TkDefaultFont", constants.label_size))
        ytd_data_label.grid(row=1, column=1, padx=10, pady=10)

        curr_week_data_label = ttk.Label(self, text=f"{current_week_count}",
                                         font=("TkDefaultFont", constants.label_size))
        curr_week_data_label.grid(row=2, column=1, padx=10, pady=10)

    def on_close(self):
        self.db.close()
        root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Dashboard")
    root.geometry("500x500")
    frame = DashboardView(root)
    root.protocol("WM_DELETE_WINDOW", frame.on_close)
    frame.pack()
    root.mainloop()