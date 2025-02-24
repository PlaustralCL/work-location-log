import tkinter as tk
from tkinter import ttk

import constants
from view_recent_days import RecentDaysView
from view_dashboard import DashboardView
from view_add_work_day import AddWorkDay
from view_weekly_summary import WeeklySummary


class WorkLocation():
    def __init__(self, root):
        self.root = root
        root.rowconfigure(1, weight=1)

        self.content_frame = ttk.Frame(self.root)
        self.content_frame.grid(column=1, row=1, sticky='n')

        self.frames = {'home': DashboardView(self.content_frame),
                       'recent_days': RecentDaysView(self.content_frame),
                       'add_day': AddWorkDay(self.content_frame),
                       'weekly_summary': WeeklySummary(self.content_frame),}
        self.current_frame = self.frames['home']
        self.current_frame.pack()

        self.nav_frame = tk.Frame(self.root)
        self.btn_style = ttk.Style()
        self.btn_style.configure('btn.TButton',
                                 font=("TkDefaultFont", constants.label_size))

        self.nav_home_btn = ttk.Button(self.nav_frame,
                                       text="Home",
                                       style='btn.TButton',
                                       command=lambda: self.change_frame('home'))
        self.nav_home_btn.grid(column=1, row=1)

        self.nav_recent_btn = ttk.Button(self.nav_frame,
                                         text="Recent",
                                         style='btn.TButton',
                                         command=lambda: self.change_frame('recent'))
        self.nav_recent_btn.grid(column=2, row=1)

        self.nav_add_btn = ttk.Button(self.nav_frame,
                                         text="Add Day",
                                         style='btn.TButton',
                                         command=lambda: self.change_frame('add_day'))
        self.nav_add_btn.grid(column=3, row=1)

        self.nav_add_btn = ttk.Button(self.nav_frame,
                                         text="Week",
                                         style='btn.TButton',
                                         command=lambda: self.change_frame('weekly_summary'))
        self.nav_add_btn.grid(column=4, row=1)


        self.nav_frame.grid(column=1, row=2, sticky='nsew')


    def change_frame(self, frame: str) -> None:
        self.current_frame.pack_forget()

        if frame == 'home':
            self.current_frame = self.frames['home']
        elif frame == 'recent':
            self.current_frame = self.frames['recent_days']
        elif frame == 'add_day':
            self.current_frame = self.frames['add_day']
        elif frame == 'weekly_summary':
            self.current_frame = self.frames['weekly_summary']

        self.current_frame.refresh()
        self.current_frame.pack()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Work Location")
    root.geometry("650x500")
    app = WorkLocation(root)

    root.mainloop()

