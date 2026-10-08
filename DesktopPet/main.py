#importing module
from multiprocessing import Process
import os
import json

import tkinter as tk

import pyttsx3 as tts

from googlesearch import search
import webbrowser as wb

import keyboard as kb

from AppOpener import open as AOopen, update_list

#importing classes and their variables
from DesktopPet import DesktopPet
from Label import LabelPet as labelP



#functions
def updateVar():
    global domains, commands, farewells, steps
    global maxTabs, giveUpTabs, bookmarks, varSetUp
    global indivCommands, speechRate, voice, varSetUp, loadApps
    
    #variables
    #getting variables
    with open(os.path.abspath("PassionProjectIST\\variables.json"), "r") as f:
        varSetUp = json.load(f)


    #setting variables
    domains = varSetUp["domains"]
    commands = varSetUp["commands"]
    farewells = varSetUp["farewells"]
    steps = varSetUp["misc"]["steps"]
    maxTabs = varSetUp["misc"]["max_tabs"]
    giveUpTabs = varSetUp["misc"]["give_up_tabs"]
    bookmarks = varSetUp["misc"]["bookmarks"]
    speechRate = varSetUp["misc"]["speech_rate"]
    voice = varSetUp["misc"]["voice"]
    loadApps = varSetUp["misc"]["load_apps"]

    indivCommands = [word for command in commands.values() for word in command] #getting all the words for commands


def chat():
    def interact():
        global varSetUp

        #get input here
        textInput.takeInput()
        window.wait_window(textInput.topLevelWin)

        userInp = textInput.userInp.get()
        userLi = userInp.split()

        try:
            if userLi[0] in indivCommands: #checking if the first word is a command
                userInp = userInp.removeprefix(userLi[0]) #removing the command word from user input

                pet.ChangeState(4)

                #searching the internet
                if userLi[0] in commands["search"]:
                    for result in search(query=userInp, tld="com", num=maxTabs, stop=giveUpTabs, pause=2): #opens 10 new tabs
                        wb.open(url=result, new=1, autoraise=True)
                    textToSpeech(f"here are the results for {userInp}")


                #open website/app
                elif userLi[0] in commands["open"]:
                    userInp = userInp.replace(" ", "")

                    if userInp in bookmarks:
                        wb.open(bookmarks[userInp])
                    else:
                        if [domain for domain in domains if domain in userInp]: #checking if there is a domain in user input
                            wb.open(userInp)
                        else:
                            AOopen(userInp, match_closest=True) #if not found a domain in user input then it will open an app
                    textToSpeech(f"opened {userInp}")


                #freeze the pet
                elif userLi[0] in commands["freeze"]:
                    textToSpeech("move mouse to desired location")
                    window.after(5000, func=lambda: pet.MovePos(
                        new_loc=[
                            window.winfo_pointerx(), 
                            window.winfo_pointery()
                            ]
                            ))
                    pet.explore = False


                #unfreeze the pet
                elif userLi[0] in commands["unfreeze"]:
                    pet.explore = True


                elif userLi[0] in commands["add"] and "bookmark" in userInp:
                    window.update_idletasks()

                    textToSpeech("what do you want it to be called?")
                    textInput.takeInput()
                    window.wait_window(textInput.topLevelWin)
                    nickname = textInput.userInp.get()

                    textToSpeech("what is the link?")
                    textInput.takeInput()
                    window.wait_window(textInput.topLevelWin)
                    link = textInput.userInp.get()

                    varSetUp["misc"]["bookmarks"][nickname] = link

                    with open(os.path.abspath("PassionProjectIST\\variables.json"), "w") as f:
                        json.dump(varSetUp, f, indent=4)

                    updateVar()
                    window.update_idletasks()
                    textToSpeech(f"bookmark {nickname} with link {link} added")


                elif userLi[0] in commands["set"]:
                    if type(varSetUp["misc"][userLi[1]]) == int:
                        varSetUp["misc"][userLi[1]] = int(userLi[2])
                    elif type(varSetUp["misc"][userLi[1]]) == bool:
                        if userLi[2] == "f":
                            newVariable = False
                        elif userLi[2] == "t":
                            newVariable = True
                        varSetUp["misc"][userLi[1]] = newVariable

                    with open(os.path.abspath("PassionProjectIST\\variables.json"), "w") as f:
                        json.dump(varSetUp, f, indent=4)

                    updateVar()
                    textToSpeech("variables updated")

                elif userLi[0] in commands["reset"]:
                    textToSpeech("resetting program")
                    with open(os.path.abspath("PassionProjectIST\\DefaultVariables.json"), "r") as f:
                        defaultVarSetUp = json.load(f)

                    varSetUp = defaultVarSetUp

                    with open(os.path.abspath("PassionProjectIST\\variables.json"), "w") as f:
                        json.dump(varSetUp, f, indent=4)

                    updateVar()

                    window.destroy()
                    textToSpeech("turn program on manually for changes to be seen")

                elif userLi[0] in commands["help"]:
                    textToSpeech(
                        """
                        Here are all the commands:\n
                        search: opens websites for you to help you in your research\n
                        open: opens websites and apps (by default you need the full address
                        for a website however, you can add bookmarks so you only need to say
                        the nickname for it)\n
                        freeze/move: make the pet move to where your mouse is and stay there\n
                        unfreeze: allow pet to move freely on the screen\n
                        add bookmark: add a bookmark for easy use of opening websites\n
                        set: you can change the values of (steps, speech_rate, voice, 
                        explore, max_tabs, give_up_tabs, bookmarks, load_apps)\n
                        reset: reset all variables
                        """
                        )


            else:
                if [farewell for farewell in farewells if farewell in userInp]:
                    textToSpeech("goodbye")
                    window.destroy()
        except Exception as e:
            print(e)


    if kb.is_pressed("ctrl+f8"): #execute functions if user pressed the keys
        pet.busy = True
        pet.ChangeState(3)
        window.update_idletasks()
        
        textToSpeech("yes?")
        interact()

        pet.busy = False
        pet.ChangeState(1)
        window.update_idletasks()

    window.after(20, func=chat) #not checking the inputs every ms so that its more efficient


def speech(text, speechRate, voice):
    engine = tts.init()
    engine.setProperty("rate", speechRate)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[voice].id)
    engine.say(text)
    engine.runAndWait()


def textToSpeech(text):
    p = Process(target=speech, args=(text, speechRate, voice,), daemon=False)
    threadQueue.append(p)
    
    try:
        for thread in threadQueue:
            thread.terminate()
    except AttributeError:
        pass

    #threading
    p.start()



if __name__ == "__main__":
    #variables
    #getting variables
    updateVar()

    indivCommands = [word for command in commands.values() for word in command] #getting all the words for commands
    threadQueue = []
    
    if loadApps:
        update_list.update() #update the list of apps that can be opened

    window = tk.Tk() #initialise window

    #make window transparent
    window.config(background="white")
    window.overrideredirect(True)
    window.wm_attributes("-topmost", True)
    window.wm_attributes("-transparentcolor", "white")
    

    #setting the area that the window can move to on your screen
    displaySize = [0, 0]
    displaySize[0] = int(window.winfo_screenwidth() - window.winfo_screenwidth() * (10/100))
    displaySize[1] = int(window.winfo_screenheight() - window.winfo_screenheight() * (20/100))

    #creating the objects
    pet = DesktopPet(window, displaySize, steps, 0)
    textInput = labelP(window)

    pet.MovePos(new_loc=None)

    #binds for the program
    window.bind("<Enter>", func=lambda event: pet.MovePos(new_loc=None))
    
    #start timers for the pet
    pet.DecideStateLoop()
    window.after(20, func=chat)
    window.after(20, textToSpeech("press control f8 and type help if you need any help"))

    window.mainloop() #run the program