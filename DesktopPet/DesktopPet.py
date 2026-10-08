#importing modules
from tkinter import ttk
from PIL import Image, ImageTk
import os
from os import listdir
from os.path import isfile, join
import random



filepath = "PassionProjectIST\\images"


states = [ #states of the pet
    {
        "name": "running",
        "files": [f for f in listdir(f"{filepath}\\running") if isfile(join(f"{filepath}\\running", f))]
    },
    {
        "name": "idle",
        "files": [f for f in listdir(f"{filepath}\\idle") if isfile(join(f"{filepath}\\idle", f))]
    },
    {
        "name": "sleeping",
        "files": [f for f in listdir(f"{filepath}\\sleeping") if isfile(join(f"{filepath}\\sleeping", f))]
    },
    {
        "name": "talking",
        "files": [f for f in listdir(f"{filepath}\\talking") if isfile(join(f"{filepath}\\talking", f))]
    },
    {
        "name": "loading",
        "files": [f for f in listdir(f"{filepath}\\loading") if isfile(join(f"{filepath}\\loading", f))]
    }
]



#the class itself
class DesktopPet(ttk.Label):
    def __init__(self, window, displaySize, steps, petState):
        #setting variables
        self.window = window
        self.displaySize = displaySize
        self.steps = steps
        self.busy = False
        self.explore = True
        self.winLocation = [int(window.winfo_x()), int(window.winfo_y())]
        self.index = 0
        self.activeAnimation = None

        #creating the pet
        self.img = ImageTk.PhotoImage(Image.open(f"{filepath}\\{states[petState]["name"]}\\{states[petState]["files"][0]}").resize((100,100)))
        super().__init__(window, text="desktopPet", image=self.img, borderwidth=0, background="white")
        self.pack()


    def DecideStateLoop(self):
        ranState = random.randint(0, 2)

        if not self.busy:
            if "running" == states[ranState]["name"]:
                self.MovePos(new_loc=None)
            else:
                self.ChangeState(ranState)

        if ranState != 2:
            self.after(5000, func=self.DecideStateLoop)
        else:
            self.after(10000, func=self.DecideStateLoop)


    def PlayAnimation(self, state):
        animation = [ImageTk.PhotoImage(Image.open(f"{filepath}\\{states[state]["name"]}\\{f}").resize((100,100))) for f in states[state]["files"]]
        self.index += 1

        if self.index < len(animation):
            new_image = animation[self.index]
            self.img = new_image
            self.config(image=animation[self.index])
            self.activeAnimation = self.after(100, func=lambda: self.PlayAnimation(state))
        else:
            self.index = 0
            self.activeAnimation = None


    def ChangeState(self, state):
        self.index = 0
        if self.activeAnimation is not None:
            self.after_cancel(self.activeAnimation)
        
        self.PlayAnimation(state)

    def MovePos(self, new_loc):
        if not self.busy and self.explore or not self.busy and new_loc != None:# or not self.busy and not explore and new_loc==None:
            self.busy = True

            prev_loc = self.winLocation

            if new_loc == None:
                new_loc = [random.randint(0, int(self.displaySize[0])), random.randint(0, int(self.displaySize[1]))]
            self.ChangeState(0)

            for i in range(self.steps):
                frac = i / float(self.steps)

                x = int(prev_loc[0] + (new_loc[0] - prev_loc[0]) * frac)
                y = int(prev_loc[1] + (new_loc[1] - prev_loc[1]) * frac)

                self.window.geometry(f"+{x}+{y}")
                self.window.update()

            self.ChangeState(1)
            self.winLocation = [int(self.window.winfo_x()), int(self.window.winfo_y())]
            self.busy = False