import tkinter as tk

from .core import Activity
from . import MainMenu


class SplashScreen(Activity):
    def display(self, app, args=None):
        background_label = tk.Label(app.window,
                                    image=app.getImageResource('splash.png'),
                                    width=795,
                                    height=595)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = app.getImageResource('splash.png')
        background_label.grid(rowspan=3, columnspan=3, sticky='news')

        app.scheduleActivity(MainMenu(), 1.0)
