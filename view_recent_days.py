import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sqlite3 import IntegrityError

import constants
from database import Database

class RecentDaysView(tk.Frame):
    # TODO: Add class docstring
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.header_label = ttk.Label(self,
                                      text="Recent Days",
                                      padding=10,
                                      font=("TkDefaultFont", constants.title_size))
        self.header_label.pack()

        self.db = Database()
        days = self.db.get_recent_days()

        self.treeview = ttk.Treeview(self, show='headings', height=15, selectmode='browse')
        self.treeview['columns'] = ('date', 'location')
        self.treeview.heading('date', text="Date")
        self.treeview.heading('location', text="Location")
        self.treeview.column('date', width=100, anchor='center')
        self.treeview.column('location', width=100, anchor='center')
        self.update()

        style = ttk.Style()
        style.configure("Treeview", font=("TkDefaultFont", constants.treeview_size))
        self.treeview.pack()

        btn_style = ttk.Style()
        btn_style.configure("btn.TButton", padding=(10, 5))

        self.btn = ttk.Button(self,
                         text="Revise Location",
                         style="btn.TButton",
                         command=self.revise_location)
        self.btn.pack(pady=10)

    def update(self):
        for i in self.treeview.get_children():
            self.treeview.delete(i)
        days = self.db.get_recent_days()
        for day in days:
            self.treeview.insert("", "end", values=day)

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
    frame = RecentDaysView(root)
    root.protocol("WM_DELETE_WINDOW", frame.on_close)
    frame.pack()
    root.mainloop()

