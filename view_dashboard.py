import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import Database

class DashboardView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.db = Database()


    def on_close(self):
        self.db.close()
        root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Dashboard")
    root.geometry("300x500")
    frame = DashboardView(root)
    root.protocol("WM_DELETE_WINDOW", frame.on_close)
    frame.pack()
    root.mainloop()