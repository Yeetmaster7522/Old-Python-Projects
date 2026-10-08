import json
import tkinter as tk
import threading

with open("FRIDAY\FridayV2\intents.json", "r") as f:
    data = json.load(f)

from AppOpener import open, close, give_appnames

#intsalling things ^^^

#functions
def useProgram(user_input, action):
    def openProgram(app_input):
        open(app_input, throw_error=False)
    def closeProgram(app_input):
        close(app_input, throw_error=False)
    def restartProgram(app_input):
        close(app_input, throw_error=False)
        open(app_input, throw_error=False)
    
    for app in apps:
        if app in user_input:
            if action == "open":
                openProgram(app)
            elif action == "close":
                closeProgram(app)
            elif action == "restart":
                restartProgram(app)

def main():
    def fInput():
        while True:
            user_input = str(input("You: "))
            user_input = user_input.lower()

            if user_input == "!stop":
                break

            if any(word in user_input for word in data["openProgram"]):
                useProgram(user_input, "open")
            elif any(word in user_input for word in data["closeProgram"]):
                useProgram(user_input, "open")
            elif any(word in user_input for word in data["restartProgram"]):
                useProgram(user_input, "open")

    root = tk.Tk()
    root.geometry("400x400")
    root.attributes('-alpha', 0.5)

    text_var = tk.StringVar()
    text_var.set("hello")

    label = tk.Button(root,
                     textvariable=text_var,
                     anchor=tk.CENTER,
                     command=lambda: threading.Thread(target=fInput).start()
                     )
    label.pack()
    root.mainloop()

#get apps
apps = give_appnames()
print(apps)

if __name__ == "__main__":
    main()