import tkinter as tk

from .core import Activity
from .RegistrationActivity import RegistrationActivity
from .VerificationActivity import VerificationActivity


class MainMenu(Activity):
    def display(self, app, args=None):
        def onRegisterClicked():
            app.startActivity(RegistrationActivity())

        def onVerifyClicked():
            app.startActivity(VerificationActivity())

        background_label = tk.Label(app.window,
                                    image=app.getImageResource('bg.png'),
                                    width=795,
                                    height=595)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = app.getImageResource('bg.png')
        background_label.grid(rowspan=3, columnspan=3, sticky='news')

        rootView = tk.Frame(app.window)
        rootView.config(bg='#2d3653')
        rootView.grid(row=1, column=1)

        registerButton = tk.Button(rootView, command=onRegisterClicked)
        registerButton.config(image=app.getImageResource('btn_register.png'),
                              width='100',
                              height='30',
                              bd=0)
        registerButton.grid(row=1, sticky='ew', pady=('30', '5'), padx='30')

        verifyButton = tk.Button(rootView, command=onVerifyClicked)
        verifyButton.config(image=app.getImageResource('btn_verify.png'),
                            width='100',
                            height='30',
                            bd=0)
        verifyButton.grid(row=2, sticky='ew', pady=('5', '30'), padx='30')
