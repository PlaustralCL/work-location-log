import tkinter as tk
from tkinter import ttk

import constants
from view_recent_days import RecentDaysView
from view_dashboard import DashboardView
from view_add_work_day import AddWorkDay


class WorkLocation():
    def __init__(self, root):
        self.root = root

        self.frames = {'home': DashboardView(self.root),
                       'recent_days': RecentDaysView(self.root),
                       'add_day': AddWorkDay(self.root),}

        self.main_frame = self.frames['home']
        # self.title_label = ttk.Label(self.main_frame,
        #                              text="Main Frame",
        #                              font=("Arial", constants.title_size))
        # self.title_label.pack()
        self.main_frame.grid(column=1, row=1, sticky='nsew')

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


        self.nav_frame.grid(column=1, row=2, sticky='s')


    def change_frame(self, frame: str) -> None:
        print(f"Change Frame: {frame}")
        self.main_frame.grid_forget()

        if frame == 'home':
            self.main_frame = self.frames['home']
        elif frame == 'recent':
            self.main_frame = self.frames['recent_days']
        elif frame == 'add_day':
            self.main_frame = self.frames['add_day']

        self.main_frame.update()
        self.main_frame.grid(column=1, row=1, sticky='nsew')


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Work Location")
    root.geometry("500x500")
    app = WorkLocation(root)

    root.mainloop()

