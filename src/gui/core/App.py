import os
import tkinter as tk
import threading

from PIL import Image, ImageTk


class App:
    def __init__(self, app_name='My Application', width=800, height=600, resizable=False):
        self.images = {}
        self.resources = None
        self.window = tk.Tk()
        self.window.config(background='white')
        self.window.title = app_name
        self.window.resizable(width=resizable, height=resizable)
        self.window.geometry('{}x{}'.format(width, height))
        self.window.padx = '0'
        self.window.pady = '0'
        self.__centerOnScreen(self.window)

    def __centerOnScreen(self, window):
        window.update_idletasks()
        w = window.winfo_screenwidth()
        h = window.winfo_screenheight()
        size = tuple(int(_)
                     for _ in window.geometry().split('+')[0].split('x'))
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2 - 50
        window.geometry('%dx%d+%d+%d' % (size + (x, y)))

    def setResourcesPath(self, path):
        self.resources = path

    def getImageResource(self, name):
        try:
            if name not in self.images:
                self.images[name] = ImageTk.PhotoImage(Image.open(os.path.join(self.resources, name)))

            return self.images[name]
        except:
            return None

    def clear(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def scheduleActivity(self, activity, delay):
        def delayedTask():
            self.startActivity(activity)

        t = threading.Timer(delay, delayedTask)
        t.start()

    def startActivity(self, activity, args=None):
        self.clear()
        activity.display(self, args)

    def startApp(self, firstActivity, args=None):
        self.startActivity(firstActivity, args)
        self.window.mainloop()
