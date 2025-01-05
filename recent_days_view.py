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

        db = Database()
        days = db.get_recent_days()

        self.listbox = tk.Listbox(self, height=15, width=30,)
        self.listbox.pack()
        for day in days:
            self.listbox.insert(tk.END, day)

        db.close_connection()





if __name__ == "__main__":
    root = tk.Tk()
    root.title("Recent Days View")
    root.geometry("300x400")
    frame = RecentDaysView(root)
    frame.pack()
    root.mainloop()

