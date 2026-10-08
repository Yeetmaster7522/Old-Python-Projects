import tkinter as tk
from DesktopPet import DesktopPet


window = tk.Tk()
window.config(background="white")
window.overrideredirect(True)
window.wm_attributes("-topmost", True)
window.wm_attributes("-transparentcolor", "white")


#setting the area that the window can move to on your screen
displaySize = [0, 0]
displaySize[0] = int(window.winfo_screenwidth() - window.winfo_screenwidth() * (10/100))
displaySize[1] = int(window.winfo_screenheight() - window.winfo_screenheight() * (20/100))

#creating the objects
pet = DesktopPet(window, displaySize, 200, 0)

input()
pet.ChangeState(0)
pet.ChangeState(1)

window.mainloop()