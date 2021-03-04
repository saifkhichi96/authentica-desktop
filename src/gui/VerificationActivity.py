import cv2
import numpy as np
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

from PIL import Image, ImageTk
from .core import Activity
from . import MainMenu


class VerificationActivity(Activity):
    def __init__(self):
        self.destImgHolder = None
        self.userId = tk.StringVar()
        self.signature = None

        self.v = tk.IntVar()
        self.v.set(1)

    def setSignatureImage(self, signatureImage, window):
        signatureImage = ImageTk.PhotoImage(signatureImage)

        self.destImgHolder.config(image=signatureImage)
        self.destImgHolder.image = signatureImage

    def highlightLocatedSignatures(self, image, bounds):
        img = np.array(image)
        for bound in bounds:
            x, y, w, h = bound
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

        return Image.fromarray(img)

    def display(self, app, args=None):
        def onLogoutClicked():
            app.startActivity(MainMenu.MainMenu())

        def onVerifyClicked():
            if self.userId.get() == '':
                messagebox.showerror('Error', 'User ID not provided')
                return

            if self.signature is None:
                messagebox.showerror('Error', 'Signature not provided')
                return

            uid = self.userId.get().strip()
            if uid != '' and self.signature is not None:
                if not app.client.is_enrolled(uid):
                    messagebox.showerror(uid + ' not found', 'No such user exists. Add a new user using the Register menu.')
                    return

                result = app.client.verify_author(uid, self.signature, is_check=self.v.get()==1)
                if result is True:
                	messagebox.showinfo('Verification Result', 'GENUINE. Signature belongs to user \'' + uid + '\'')
                elif result is False:
                	messagebox.showinfo('Verification Result', 'FORGED. Signature does not belong to user \'' + uid + '\'')
                else:
                	messagebox.showinfo('Verification Result', 'ERROR. Cannot verify the signature at this time. Please try again.')

        def openImage():
            # open a file chooser dialog and allow the user to select an input image
            path = filedialog.askopenfilename()

            # ensure a file path was selected
            if len(path) > 0:
                try:
                    self.signature = cv2.imread(path, 0)

                    im = cv2.imread(path)
                    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
                    signature = Image.fromarray(im).convert('RGB')

                    # if self.v.get() == 1:
                    #     bounds: todo: extract signature from bank check
                    #     signature = self.highlightLocatedSignatures(signature, bounds)

                    signature = self.resize(
                        signature, (self.destImgHolder.winfo_width(), self.destImgHolder.winfo_height())
                    )
                    self.setSignatureImage(signature, app.window)
                except Exception as e:
                    messagebox.showerror('Error', e)

        background_label = tk.Label(app.window,
                                    image=app.getImageResource('bg.png'),
                                    width=795,
                                    height=595)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = app.getImageResource('bg.png')
        background_label.grid(rowspan=60, columnspan=80, sticky='news')

        rootView = app.window

        instructions_image = ImageTk.PhotoImage(
            Image.open('../res/instructions_v.png'))
        instructionsView = tk.Label(
            rootView, image=instructions_image, width=600, height=275)
        instructionsView.config(background='white')
        instructionsView.place(x=0, y=0, relwidth=1, relheight=1)
        instructionsView.image = instructions_image
        instructionsView.grid(row=0, column=0, rowspan=30,
                              columnspan=80, sticky='news')

        backButton = tk.Button(instructionsView, command=onLogoutClicked)
        backButton.config(
            image=app.getImageResource('ic_button_back.png'), width='28', height='28', bd=0)
        backButton.grid(row=1, column=1, padx='5', pady='5')

        tk.Label(instructionsView, text='VERIFICATION', font='Helvetica 20 bold',
                 bg='white', fg='black').grid(row=1, column=2, sticky='w')

        tk.Radiobutton(rootView, variable=self.v, value=1, bg='white',
                       fg='black').grid(row=16, column=17, sticky='sw')
        tk.Radiobutton(rootView, variable=self.v, value=2, bg='white',
                       fg='black').grid(row=17, column=17, sticky='nw')

        captureButton = tk.Button(rootView, command=openImage)
        captureButton.config(
            image=app.getImageResource('btn_capture.png'), width='100', height='30', bd=0)
        captureButton.grid(row=20, column=20)

        userIdField = tk.Entry(rootView, textvariable=self.userId, relief='flat')
        userIdField.grid(row=15, column=51, columnspan=19, sticky='ew')

        registerButton = tk.Button(rootView, command=onVerifyClicked)
        registerButton.config(
            image=app.getImageResource('btn_verify.png'), width='100', height='30', bd=0)
        registerButton.grid(row=17, column=57)

        self.destImgHolder = tk.Label(rootView)
        self.destImgHolder.config(background='white')
        self.destImgHolder.grid(row=30, column=0, rowspan=30,
                                columnspan=80, ipadx='5', ipady='5', sticky='news')
