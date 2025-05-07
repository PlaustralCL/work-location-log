import tkinter as tk
from tkinter import ttk

import constants
from view_recent_days import RecentDaysView
from view_dashboard import DashboardView
from view_add_work_day import AddWorkDay
from view_ytd_summary import YTDSummary


class WorkLocation():
    """
    Main drive class for the application. Creates the main window and manages
    the window.
    """
    def __init__(self, root):
        self.root = root
        root.rowconfigure(1, weight=1)
        root.grid_columnconfigure(1, weight=1)

        self.content_frame = tk.Frame(self.root)
        self.content_frame.grid(column=1, row=1, sticky='nsew')

        self.frames = {'home': DashboardView(self.content_frame),
                       'recent_days': RecentDaysView(self.content_frame),
                       'add_day': AddWorkDay(self.content_frame),
                       'ytd_summary': YTDSummary(self.content_frame), }
        self.current_frame = self.frames['home']
        self.current_frame.pack()

        self.nav_frame = tk.Frame(self.root)
        self.build_nav_buttons(self.nav_frame)
        self.nav_frame.grid(column=1, row=2, sticky='s')

    def build_nav_buttons(self, parent) -> None:
        """
        Build the frame and buttons for the nav bar
        :param parent: The parent frame
        :return: None
        """

        nav_buttons = tk.Frame(parent)
        btn_style = ttk.Style()
        btn_style.configure('btn.TButton',
                                 font=("TkDefaultFont", constants.label_size))

        nav_home_btn = ttk.Button(nav_buttons,
                                       text="Home",
                                       style='btn.TButton',
                                       command=lambda: self.change_frame('home'))
        nav_home_btn.grid(column=1, row=1)

        nav_add_btn = ttk.Button(nav_buttons,
                                      text="Add Day",
                                      style='btn.TButton',
                                      command=lambda: self.change_frame('add_day'))
        nav_add_btn.grid(column=2, row=1)

        nav_recent_btn = ttk.Button(nav_buttons,
                                         text="Recent",
                                         style='btn.TButton',
                                         command=lambda: self.change_frame('recent'))
        nav_recent_btn.grid(column=3, row=1)



        nav_add_btn = ttk.Button(nav_buttons,
                                      text="YTD",
                                      style='btn.TButton',
                                      command=lambda: self.change_frame('ytd_summary'))
        nav_add_btn.grid(column=4, row=1)

        nav_buttons.grid(column=1, row=2, sticky='nsew')

    def change_frame(self, frame: str) -> None:
        """
        Updates the content frame to show the requested frame/view. Before the
        new frame is displayed, the contents are refreshed.
        :param frame: The requested frame/view.
        :return: None
        """
        self.current_frame.pack_forget()

        if frame == 'home':
            self.current_frame = self.frames['home']
        elif frame == 'recent':
            self.current_frame = self.frames['recent_days']
        elif frame == 'add_day':
            self.current_frame = self.frames['add_day']
        elif frame == 'ytd_summary':
            self.current_frame = self.frames['ytd_summary']

        self.current_frame.refresh()
        self.current_frame.pack()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Work Location")
    root.geometry("650x500")
    app = WorkLocation(root)

    root.mainloop()

