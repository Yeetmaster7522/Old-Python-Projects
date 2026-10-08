#importing modules
import tkinter as tk
from tkinter import Toplevel



#the class itself
class LabelPet(tk.Entry):
    def __init__(self, window):
        #setting variables
        self.userInp = tk.StringVar()
        self.window = window


    def appear(self):
        self.topLevelWin = Toplevel(self.window)
        self.topLevelWin.config(background="blue")
        self.topLevelWin.overrideredirect(True)
        self.topLevelWin.wm_attributes("-topmost", True)
        self.topLevelWin.wm_attributes("-transparentcolor", "blue")


    def takeInput(self):
        self.userInp.set("")
        self.appear()

        super().__init__(self.topLevelWin, textvariable=self.userInp, bg="black", fg="white", bd=5)
        self.pack()

        x = int(self.topLevelWin.winfo_pointerx()) - 60
        y = int(self.topLevelWin.winfo_pointery()) - 20
        self.topLevelWin.geometry(f"+{x}+{y}")
        self.topLevelWin.update_idletasks()

        self.topLevelWin.bind("<Return>", func=self.submit)
        self.focus_force()


    def submit(self, event=None):
        self.topLevelWin.destroy()