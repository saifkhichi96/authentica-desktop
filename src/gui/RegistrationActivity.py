import cv2
import numpy as np
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox


from PIL import Image, ImageTk
from .core import Activity
from . import MainMenu


class RegistrationActivity(Activity):
    def __init__(self):
        self.destImgHolder = None
        self.userId = tk.StringVar()
        self.signatures = None

    def setSignatureImage(self, signatureImage, window):
        signatureImage = ImageTk.PhotoImage(signatureImage)

        self.destImgHolder.config(image=signatureImage)
        self.destImgHolder.image = signatureImage

    def highlightLocatedSignatures(self, image, bounds):
        img = np.array(image)
        for bound in bounds:
            try:
                x, y, w, h = bound
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            except Exception as ex:
                print(ex)

        return Image.fromarray(img)

    def display(self, app, args=None):
        def onLogoutClicked():
            app.startActivity(MainMenu.MainMenu())

        def onRegisterClicked():
            if self.userId.get() == '':
                messagebox.showerror('Error', 'User ID not provided')
                return

            if self.signatures is None:
                messagebox.showerror(
                    'Error', 'Reference signatures not provided')
                return

            uid = self.userId.get()
            if uid != '' and self.signatures is not None:
                if app.client.is_enrolled(uid):
                    messagebox.showerror(uid + ' already exists', 'This user ID is already taken. Please provide a different ID.')
                    return

                if app.client.enroll(uid, self.signatures):
                    messagebox.showinfo('Enrollment Result', 'Enrollment successful')

        def openImage():
            # open a file chooser dialog and allow the user to select an input image
            #path =  scanImage(outfile='scanned')
            path = filedialog.askopenfilename()

            # ensure a file path was selected
            if len(path) > 0:
                try:
                    self.signatures = cv2.imread(path, 0)

                    im = cv2.imread(path)
                    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
                    signature = Image.fromarray(im).convert('RGB')

                    # bounds: todo: extract signatures from specimen grid
                    # signature = self.highlightLocatedSignatures(signature, bounds)

                    signature = self.resize(
                        signature, (self.destImgHolder.winfo_width(), self.destImgHolder.winfo_height())
                    )
                    self.setSignatureImage(signature, app.window)
                except Exception as ex:
                    messagebox.showerror('Error', f'No signature detected. {ex}')

        background_label = tk.Label(app.window,
                                    image=app.getImageResource('bg.png'),
                                    width=795,
                                    height=595)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = app.getImageResource('bg.png')
        background_label.grid(rowspan=60, columnspan=80, sticky='news')

        rootView = app.window

        instructions_image = ImageTk.PhotoImage(
            Image.open('../res/instructions.png'))
        instructionsView = tk.Label(
            rootView, image=instructions_image, width=275, height=400)
        instructionsView.config(background='white')
        instructionsView.place(x=0, y=0, relwidth=1, relheight=1)
        instructionsView.image = instructions_image
        instructionsView.grid(row=0, column=0, rowspan=60,
                              columnspan=40, sticky='news')

        tk.Label(instructionsView, text='REGISTRATION', font='Helvetica 20 bold',
                 bg='white', fg='black').grid(row=1, column=2, sticky='w')

        backButton = tk.Button(instructionsView, command=onLogoutClicked)
        backButton.config(
            image=app.getImageResource('ic_button_back.png'), width='28', height='28', bd=0)
        backButton.grid(row=1, column=1, padx='5', pady='5')

        captureButton = tk.Button(rootView, command=openImage)
        captureButton.config(
            image=app.getImageResource('btn_capture.png'), width='100', height='30', bd=0)
        captureButton.grid(row=34, column=22)

        userIdField = tk.Entry(rootView, textvariable=self.userId, relief='flat')
        userIdField.grid(row=43, column=16, columnspan=14, sticky='ew')

        registerButton = tk.Button(rootView, command=onRegisterClicked)
        registerButton.config(
            image=app.getImageResource('btn_register.png'), width='100', height='30', bd=0)
        registerButton.grid(row=53, column=22)

        self.destImgHolder = tk.Label(rootView)
        self.destImgHolder.config(background='white')
        self.destImgHolder.grid(row=0, column=40, rowspan=60,
                                columnspan=40, ipadx='5', ipady='5', sticky='news')
