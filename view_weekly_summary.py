import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sqlite3 import IntegrityError
from datetime import date

import constants
from database import Database

class WeeklySummary(tk.Frame):
    """
    Create a frame that shows a summary of the weekly data
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.header_label = ttk.Label(self,
                                      text="Weekly Summary",
                                      padding=10,
                                      font=("TkDefaultFont", constants.title_size))
        self.header_label.pack()

        self.db = Database()

        self.treeview = ttk.Treeview(self, show='headings', height=15, selectmode='browse')
        self.treeview['columns'] = ('week_number', 'week_start', 'week_end', 'office_count')
        self.treeview.heading('week_number', text="Week Number")
        self.treeview.heading('week_start', text="Start Date")
        self.treeview.heading('week_end', text="End Date")
        self.treeview.heading('office_count', text="Count")
        self.treeview.column('week_number', width=100, anchor='center')
        self.treeview.column('week_start', width=100, anchor='center')
        self.treeview.column('week_end', width=100, anchor='center')
        self.treeview.column('office_count', width=100, anchor='center')
        self.refresh()

        style = ttk.Style()
        style.configure("Treeview", font=("TkDefaultFont", constants.treeview_size))
        self.treeview.pack()

    def refresh(self):
        start_week = str(date.today().year) + '-01'
        end_week = str(date.today().year) + "-" + str(date.today().isocalendar().week).zfill(2)
        for i in self.treeview.get_children():
            self.treeview.delete(i)
        weeks = self.db.get_weekly_summary(start_week=start_week, end_week=end_week)
        for week in weeks:
            self.treeview.insert("", "end", values=week)

    def get_selected_item_id(self) -> str:
        """
        Finds and returns the id of the item selected in the treeview.
        :return: A string representing the selected item id
        """
        selected_item = self.treeview.selection()
        item_id = None
        if selected_item:
            item_id = self.treeview.focus()
        return item_id

    def revise_location(self):
        """
        Revised the location of the day in the database. The location will
        toggle between 'office' and 'remote'.
        """
        item_id = self.get_selected_item_id()
        if item_id:
            work_date = self.treeview.item(item_id, 'values')[0]
            current_location = self.treeview.item(item_id, 'values')[1]
            # TODO: use the locations in the database instead of hardcoding them
            if current_location == 'office':
                new_location = 'remote'
            else:
                new_location = 'office'
            try:
                self.db.set_location(work_date, new_location)
            except IntegrityError:
                messagebox.showwarning(message=f"Not a valid location. No changes made.")

            workday = self.db.get_work_day(work_date)
            location = workday[2]
            self.treeview.item(item_id, values=(work_date, location))

    def on_close(self):
        self.db.close()
        root.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Recent Days View")
    root.geometry("500x500")
    frame = WeeklySummary(root)
    root.protocol("WM_DELETE_WINDOW", frame.on_close)
    frame.pack()
    root.mainloop()

