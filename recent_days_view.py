import tkinter as tk
from tkinter import ttk
from database import Database

class RecentDaysView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.header_label = ttk.Label(self,
                                      text="Recent Days",
                                      padding=10,
                                      font=("TkDefaultFont", 20))
        self.header_label.pack()

        self.db = Database()
        days = self.db.get_recent_days()

        self.treeview = ttk.Treeview(self, show='headings', height=15, selectmode='browse')
        self.treeview['columns'] = ('date', 'location')
        self.treeview.heading('date', text="Date")
        self.treeview.heading('location', text="Location")
        self.treeview.column('date', width=100, anchor='center')
        self.treeview.column('location', width=100, anchor='center')
        for day in days:
            self.treeview.insert("", "end", values=day)

        self.treeview.pack()

        btn_style = ttk.Style()
        btn_style.configure("btn.TButton", padding=(10, 5))

        self.btn = ttk.Button(self,
                         text="Revise Location",
                         style="btn.TButton",
                         command=self.revise_location)
        self.btn.pack(pady=10)

        # self.db.close_connection()

    def get_selected_item_id(self):
        selected_item = self.treeview.selection()
        item_id = None
        if selected_item:
            item_id = self.treeview.focus()
        return item_id

    def revise_location(self):
        item_id = self.get_selected_item_id()
        if item_id:
            # print( self.treeview.item(item_id, 'values'))
            work_date = self.treeview.item(item_id, 'values')[0]
            current_location = self.treeview.item(item_id, 'values')[1]
            if current_location == 'office':
                new_location = 'remote'
            else:
                new_location = 'office'

            self.db.set_location(work_date, new_location)
            workday = self.db.get_work_day(work_date)
            location = workday[2]
            print(workday)
            self.treeview.item(item_id, values=(work_date, location))








if __name__ == "__main__":
    root = tk.Tk()
    root.title("Recent Days View")
    root.geometry("300x500")
    frame = RecentDaysView(root)
    frame.pack()
    root.mainloop()

