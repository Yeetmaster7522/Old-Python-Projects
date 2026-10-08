#https://mcsp.wartburg.edu/zelle/python/graphics/graphics.pdf
"""
NOTES ABOUT CODE:
- Press m to mute and unmute background music (is put into effect once user clicks onto screen)
- Be careful with text shape, it can block the options menu and there is no way to fix that
- Run this on windows if you can
"""


#import modules
from graphics import *
from threading import Thread
import pickle
import os
#if it is not a windows device, there will be no sound
try:
    import winsound
    windows_device = True
except:
    print("RUN ON WINDOWS FOR SOUND")
    windows_device = False

script_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_path)

start_program_file = os.path.abspath("start_program.wav")
background_file = os.path.abspath("laidback_painting.wav")


def play_tutorial():
    #tutorial for user to go through
    #drawing the base window
    win = GraphWin("GraphicsPro++ Tutorial", 1500, 800, autoflush=False)
    option_bg, option_border = Rectangle(Point(0,0), Point(100, 1000)), Line(Point(100, 0), Point(100, 1000))
    thickness_button0, thickness_button1, thickness_button2, thickness_button3, thickness_button4 = Rectangle(Point(20, 50), Point(69, 70)), Line(Point(27, 50), Point(27, 70)), Line(Point(35, 50), Point(35, 70)), Line(Point(45, 50), Point(45, 70)), Line(Point(57, 50), Point(57, 70))
    colour_button = Rectangle(Point(19, 90), Point(68, 120))
    colour_symbol = Rectangle(Point(29, 90), Point(58, 120))
    shape_button, shape_symbol = Rectangle(Point(19, 140), Point(68, 170)), Line(Point(24, 155), Point(63, 155))
    undo_button, redo_button, undo_symbol, redo_symbol = Rectangle(Point(18, 240), Point(38, 200)), Rectangle(Point(70, 240), Point(50, 200)), Polygon(Point(18, 220), Point(38, 200), Point(38, 240)), Polygon(Point(70, 220), Point(50, 200), Point(50, 240))
    clear_button, escape_button = Text(Point(43, 500), "♻"), Text(Point(43, 550), "❌")
    
    option_bg.setFill("light grey")
    option_bg.setOutline("light grey")
    thickness_button0.setFill("white")
    colour_button.setFill("white")
    colour_symbol.setFill("black")
    shape_button.setFill("white")
    shape_symbol.setFill("black")
    undo_button.setFill("white")
    redo_button.setFill("white")
    undo_symbol.setFill("black")
    redo_symbol.setFill("black")
    
    option_border.setWidth(10)
    thickness_button1.setWidth(3)
    thickness_button2.setWidth(5)
    thickness_button3.setWidth(7)
    thickness_button4.setWidth(9)
    clear_button.setSize(20)
    escape_button.setSize(20)
    
    option_bg.draw(win)
    option_border.draw(win)
    thickness_button0.draw(win)
    thickness_button1.draw(win)
    thickness_button2.draw(win)
    thickness_button3.draw(win)
    thickness_button4.draw(win)
    colour_button.draw(win)
    colour_symbol.draw(win)
    shape_button.draw(win)
    shape_symbol.draw(win)
    undo_button.draw(win)
    redo_button.draw(win)
    undo_symbol.draw(win)
    redo_symbol.draw(win)
    clear_button.draw(win)
    escape_button.draw(win)
    
    #drawing the lines that point to the options on the options menu
    pointer_line1, pointer_line2, pointer_line3, pointer_line4, pointer_line5, pointer_line6 = Line(Point(69, 60), Point(150, 60)), Line(Point(69, 105), Point(150, 105)), Line(Point(69, 155), Point(150, 155)), Line(Point(71, 220), Point(150, 220)), Line(Point(55, 500), Point(150, 500)), Line(Point(55, 550), Point(150, 550))
    
    pointer_line1.setWidth(5)
    pointer_line2.setWidth(5)
    pointer_line3.setWidth(5)
    pointer_line4.setWidth(5)
    pointer_line5.setWidth(5)
    pointer_line6.setWidth(5)
    
    pointer_line1.draw(win)
    pointer_line2.draw(win)
    pointer_line3.draw(win)
    pointer_line4.draw(win)
    pointer_line5.draw(win)
    pointer_line6.draw(win)
    
    #drawing the text that tells the user what the buttons are
    pointer_text1, pointer_text2, pointer_text3, pointer_text4, pointer_text5, pointer_text6 = Text(Point(230, 60), "Line thickness"), Text(Point(190, 105), "Colour"), Text(Point(190, 155), "Shape"), Text(Point(235, 220), "Undo and redo"), Text(Point(185, 500), "Reset"), Text(Point(195, 550), "Escape")
    pointer_text1.setSize(18)
    pointer_text2.setSize(18)
    pointer_text3.setSize(18)
    pointer_text4.setSize(18)
    pointer_text5.setSize(18)
    pointer_text6.setSize(18)
    
    pointer_text1.draw(win)
    pointer_text2.draw(win)
    pointer_text3.draw(win)
    pointer_text4.draw(win)
    pointer_text5.draw(win)
    pointer_text6.draw(win)

    #Setting a variable for use with undo and redo
    tutorial_list_drawn = []
    tutorial_list_undrawn = []

    #telling use what to do
    objective = Text(Point(500, 10), "Click on the screen to go through tutorial")
    objective.draw(win)

    #telling user how to draw a line
    win.getMouse()
    objective.setText("Left clicked")
    clickAnim = Circle(Point(400, 200), 20)
    clickAnim.draw(win)
    win.redraw()

    win.getMouse()
    objective.setText("Left clicked")
    clickAnim.undraw()
    tutorial_obj = Line(Point(400, 200), Point(1000, 200))
    tutorial_obj.setWidth(10)
    tutorial_obj.draw(win)
    win.redraw()

    #telling user how line thickness works
    win.getMouse()
    objective.setText("Left clicked on line thickness")
    entry_box = Entry(Point(45, 700), 10)
    entry_box.setText("Line thickness: 10")
    entry_box.draw(win)
    win.redraw()
    
    win.getMouse()
    objective.setText("Entered 50 by using manual input/arrow keys and then pressing enter")
    entry_box.setText("50")
    option_border.setWidth(50)
    win.redraw()
    
    #showing what happened to drawing lines when you change the line thickness
    win.getMouse()
    objective.setText("Left clicked")
    entry_box.undraw()
    clickAnim.draw(win)
    win.redraw()

    win.getMouse()
    objective.setText("Left clicked")
    clickAnim.undraw()
    tutorial_obj = Line(Point(400, 200), Point(1000, 200))
    tutorial_obj.setWidth(50)
    tutorial_obj.draw(win)
    win.redraw()

    tutorial_list_drawn.append(tutorial_obj)

    #showing user how to use colour
    for x in range(1, 3):
        win.getMouse()
        objective.setText("Left clicked on colour")
        if x == 1:
            entry_box.setText("RED: 0")
            entry_box.draw(win)
        elif x == 2:
            entry_box.setText("GREEN: 0")
        elif x == 3:
            entry_box.setText("BLUE: 0")
    
        win.getMouse()
        objective.setText("Entered 100 by using manual input/arrow keys and then pressing enter")
        entry_box.setText("100")
        win.redraw()

    #showing what happened to the colour of the line
    win.getMouse()
    colour_symbol.setFill(color_rgb(100, 100, 100))
    objective.setText("Left clicked")
    entry_box.undraw()
    clickAnim.draw(win)
    win.redraw()

    win.getMouse()
    objective.setText("Left clicked")
    clickAnim.undraw()
    tutorial_obj = Line(Point(400, 200), Point(1000, 200))
    tutorial_obj.setFill(color_rgb(100, 100, 100))
    tutorial_obj.draw(win)
    win.redraw()

    tutorial_list_drawn.append(tutorial_obj)

    #showing user how to use shape
    win.getMouse()
    objective.setText("Left clicked on shape button")
    entry_box.setText("↑ ➖ ↓")
    entry_box.draw(win)
    win.redraw()

    win.getMouse()
    objective.setText("Up arrow key")
    entry_box.setText("↑ ⬛ ↓")
    win.redraw()

    win.getMouse()
    entry_box.setText("↑ ⭕ ↓")
    win.redraw()

    win.getMouse()
    entry_box.setText("↑ 🔺 ↓")
    win.redraw()

    win.getMouse()
    entry_box.setText("↑ TXT ↓")
    win.redraw()

    win.getMouse()
    objective.setText("Down arrow key")
    entry_box.setText("↑ 🔺 ↓")
    win.redraw()
    
    #showing user how to draw a polygon
    win.getMouse()
    objective.setText("Left clicked")
    entry_box.undraw()
    clickAnim1 = Circle(Point(400, 300), 20)
    clickAnim1.draw(win)
    win.redraw()

    win.getMouse()
    objective.setText("Left clicked")
    clickAnim2 = Circle(Point(600, 300), 20)
    clickAnim2.draw(win)
    win.redraw()

    win.getMouse()
    objective.setText("Enter and then left clicked")
    clickAnim1.undraw()
    clickAnim2.undraw()
    tutorial_obj = Polygon(Point(400, 300), Point(600, 300), Point(500, 500))
    tutorial_obj.setFill(color_rgb(100, 100, 100))
    tutorial_obj.setWidth(50)
    tutorial_obj.draw(win)
    win.redraw()

    tutorial_list_drawn.append(tutorial_obj)

    #showing what undo and redo do
    win.getMouse()
    objective.setText("Left clicked on undo")
    undrawn = tutorial_list_drawn.pop()
    undrawn.undraw()
    win.redraw()

    tutorial_list_undrawn.append(undrawn)
    
    win.getMouse()
    objective.setText("Left clicked on redo")
    drawn = tutorial_list_undrawn.pop()
    drawn.draw(win)
    win.redraw()

    tutorial_list_drawn.append(drawn)

    win.getMouse()
    win.close()



#accessing save files to check whether or not the program has to show the user how to use it
try:
    with open("save.txt", "rb") as file:
        used = pickle.load(file)
except Exception as e:
    print(e)
    with open("save.txt", "wb") as file:
        pickle.dump("Ran", file)

    play_tutorial()


#setting global variable which can reset or quit the program
reset_canvas = False
muted = False


#gets multiple mouse coordinates to draw shapes
def multi_coord_mouse():
    #getting global variables
    global win, xVal1, yVal1, xVal2, yVal2, point_list
    global shape, option_chosen
    global clickAnim, clickAnim_list
    global muted, windows_device
    global background_file

    #drawing polygons
    if shape == "polygon":
        #a while true loop which allows user to click multiple locations infinitely
        while True:
            #breaking the loop if the user clicked on the enter key
            user_key = win.checkKey()
            if user_key == "Return":
                break
            
            #checking if the user clicked on m to mute/unmute music
            elif windows_device == True:
                if user_key == "m" and muted == False:
                    winsound.PlaySound(None, winsound.SND_PURGE)
                    muted, user_key = True, None
                elif user_key == "m" and muted == True:
                    winsound.PlaySound(background_file, winsound.SND_ASYNC + winsound.SND_NODEFAULT + winsound.SND_LOOP)
                    muted, user_key = False, None

            #getting mouse coordinates
            clickPoint = win.getMouse()
            xVal1, yVal1 = clickPoint.getX(), clickPoint.getY()

            #checking if the user clicked on any options
            options()
            #breaking the loop if the user clicked on any options 
            if option_chosen:
                break

            else:
                #appending all the points into a list so that polygon drawing is flexible
                user_append = Point(xVal1, yVal1)
                point_list.append(user_append)

                #drawing click animations
                if not abs(xVal1) <= 100 and abs(150 - yVal1) <= 1000:
                    clickAnim = Circle(Point(xVal1, yVal1), 20)
                    clickAnim.draw(win)
                    clickAnim_list.append(clickAnim)
    elif shape == "text":
        if windows_device == True:
            #checking if the user clicked on m to mute/unmute music
            user_key = win.checkKey()
            if user_key == "m" and muted == False:
                winsound.PlaySound(None, winsound.SND_PURGE)
                muted, user_key = True, None
            elif user_key == "m" and muted == True:
                winsound.PlaySound(background_file, winsound.SND_ASYNC + winsound.SND_NODEFAULT + winsound.SND_LOOP)
                muted, user_key = False, None

        #getting mouse coordinates
        clickPoint = win.getMouse()
        xVal1, yVal1 = clickPoint.getX(), clickPoint.getY()

        #checking if user clicked on options
        options()
    #this is for everything that isn't a polygon or text shape
    else:
        if windows_device == True:
            #checking if the user clicked on m to mute/unmute music
            user_key = win.checkKey()
            if user_key == "m" and muted == False:
                winsound.PlaySound(None, winsound.SND_PURGE)
                muted, user_key = True, None
            elif user_key == "m" and muted == True:
                winsound.PlaySound(background_file, winsound.SND_ASYNC + winsound.SND_NODEFAULT + winsound.SND_LOOP)
                muted, user_key = False, None

        #getting mouse coordinates
        clickPoint1 = win.getMouse()
        xVal1, yVal1 = clickPoint1.getX(), clickPoint1.getY()

        #drawing click animations
        if not abs(xVal1) <= 100 and abs(150 - yVal1) < 1000:
            clickAnim = Circle(Point(xVal1, yVal1), 20)
            clickAnim.draw(win)

        #checking if user clicked on options
        options()

        #if the user has not clicked on any options, it will continue to get the second mouse coordinates
        if not option_chosen:
            if windows_device == True:
                #checking if the user clicked on m to mute/unmute music
                user_key = win.checkKey()
                if user_key == "m" and muted == False:
                    winsound.PlaySound(None, winsound.SND_PURGE)
                    muted, user_key = True, None
                elif user_key == "m" and muted == True:
                    winsound.PlaySound(background_file, winsound.SND_ASYNC + winsound.SND_NODEFAULT + winsound.SND_LOOP)
                    muted, user_key = False, None

            clickPoint2 = win.getMouse()
            xVal2, yVal2 = clickPoint2.getX(), clickPoint2.getY()
            try:
                clickAnim.undraw()
            except Exception as e:
                print(e)
                pass
            #checking if the user has clicked on options again
            options()


def options():
    #accessing global variables
    global win, objects_drawn, objects_removed
    global xVal1, yVal1, xVal2, yVal2, point_list
    global line_thickness, shape, red, green, blue
    global reset_canvas, undo, redo, option_chosen
    global clickAnim, clickAnim_list

    #ressetting/setting variables used for user input in the window
    user_box, text_list = Entry(Point(45, 700), 10), []

    #when user clicks on size button
    if abs(xVal1) <= 70 and abs(50 - yVal1) <= 20 or abs(xVal2) <= 70 and abs(50 - yVal2) <= 20:
        #undrawing any click animations
        for object in clickAnim_list:
            object.undraw()

        #draws an entry box in which the user can input what size they want
        user_box.setText(line_thickness)
        user_box.draw(win)
        text_list = list(str(line_thickness))
        
        #put in a while true loop with try and excepts to make sure the code doesn't break from any errors
        while True:
            try:
                #gets user inputs until the user presses enter
                while True:
                    user_key = win.getKey()
                    if user_key == "BackSpace":
                        text_list.pop()
                    elif user_key == "Up":
                        user_key = str(int("".join(text_list)) + 1)
                        text_list = list(str(user_key))
                    elif user_key == "Down":
                        if int("".join(text_list)) != 0:
                            user_key = str(int("".join(text_list)) - 1)
                            text_list = list(str(user_key))
                    elif user_key == "Return":
                        break
                    elif user_key in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                        text_list.append(user_key)
                    #sets the entry box to the user input
                    user_box.setText("".join(text_list))
                    win.redraw()
                
                #gets the user input and turns it into an interger
                line_thickness = int("".join(text_list))
                if line_thickness >= 201:
                    line_thickness = 200
                #tells other functions that an option has been chosen
                option_chosen = True
                break
            except Exception as e:
                print(e)
    #when user clicks on the colour button
    elif abs(xVal1) <= 69 and abs(100 - yVal1) <= 20 or abs(xVal2) <= 69 and abs(100 - yVal2) <= 20:
        #undrawing any click animations
        for object in clickAnim_list:
            object.undraw()

        #putting it in 3 loops to set red, green and blue
        for x in range(3):
            #using x to figure out which RGB value to use
            if x == 0:
                user_box.setText(f"RED: {red}")
                text_list = list(str(red))
            elif x == 1:
                user_box.setText(f"GREEN: {green}")
                text_list = list(str(green))
            elif x == 2:
                user_box.setText(f"BLUE: {blue}")
                text_list = list(str(blue))
            
            #drawing the entry box
            user_box.draw(win)
            
            #put in a while true in case there is an error
            while True:
                try:
                    #getting user inputs
                    while True:
                        user_key = win.getKey()
                        if user_key == "BackSpace":
                            text_list.pop()
                        elif user_key == "Up":
                            #if it is 255, it will go to 0
                            if int("".join(text_list)) != 255:
                                user_key = str(int("".join(text_list)) + 1)
                            else:
                                user_key = "0"
                            text_list = list(str(user_key))
                        elif user_key == "Down":
                            #if it is 0, it will go to 255
                            if int("".join(text_list)) != 0:
                                user_key = str(int("".join(text_list)) - 1)
                            else:
                                user_key = "255"
                            text_list = list(str(user_key))
                        elif user_key == "Return":
                            break
                        elif user_key in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                            text_list.append(user_key)
            
                        #redrawing entry box with user inputs
                        user_box.setText("".join(text_list))
                        win.redraw()
                    
                    #in case the user sets the value higher than 255, it will make it default to 255
                    if int("".join(text_list)) >= 256:
                        text_list = []
                        text_list.append("255")

                    #setting variable depending on which loop it is
                    if x == 0:
                        red = int("".join(text_list))
                    elif x == 1:
                        green = int("".join(text_list))
                    elif x == 2:
                        blue = int("".join(text_list))
            
                    option_chosen = True
                    user_box.undraw()
                    break
                except Exception as e:
                    print(e)
    #when user clicks on shape
    elif abs(xVal1) <= 69 and abs(150 - yVal1) <= 20 or abs(0 - xVal2) <= 69 and abs(150 - yVal2) < 20:
        #undrawing any click animations
        for object in clickAnim_list:
            object.undraw()

        #draws entry box in which the user can input what shape what they want and sets some variables used for the specific purpose of scrolling through all the shape options
        if shape == "line":
            user_box.setText("↑ ➖ ↓")
            shape_num = 1
        elif shape == "rectangle":
            user_box.setText("↑ ⬛ ↓")
            shape_num = 2
        elif shape == "oval":
            user_box.setText("↑ ⭕ ↓")
            shape_num = 3
        elif shape == "polygon":
            user_box.setText("↑ 🔺 ↓")
            shape_num = 4
        elif shape == "text":
            user_box.setText("↑ TXT ↓")
            shape_num = 5
        
        user_box.draw(win)
        
        #put in a while true loop with try and excepts to make sure the code doesn't break from user error
        while True:
            try:
                #gets user input until user presses enter
                while True:
                    user_key = win.getKey()
                    if user_key == "Up":
                        if shape_num == 5:
                            shape_num = 1
                        else:
                            shape_num += 1
                    elif user_key == "Down":
                        if shape_num == 1:
                            shape_num = 5
                        else:
                            shape_num -= 1
                    elif user_key == "Return":
                        break
                    else:
                        text_list.append(user_key)
        
                    #sets entry box to user input
                    if shape_num == 1:
                        user_box.setText("↑ ➖ ↓")
                    elif shape_num == 2:
                        user_box.setText("↑ ⬛ ↓")
                    elif shape_num == 3:
                        user_box.setText("↑ ⭕ ↓")
                    elif shape_num == 4:
                        user_box.setText("↑ 🔺 ↓")
                    elif shape_num == 5:
                        user_box.setText("↑ TXT ↓")
        
                    win.redraw()
        
                #gets shape
                if shape_num == 1:
                    shape = "line"
                elif shape_num == 2:
                    shape = "rectangle"
                elif shape_num == 3:
                    shape = "oval"
                elif shape_num == 4:
                    shape = "polygon"
                elif shape_num == 5:
                    shape = "text"
        
                #tells other functions that an option has been chosen
                option_chosen = True
                break
            except Exception as e:
                print(e)
    #when user clicks undo
    elif abs(xVal1) <= 37 and abs(220 - yVal1) <= 22 or abs(xVal2) <= 37 and abs(220 - yVal2) <= 22:
        #undrawing any click animations
        for object in clickAnim_list:
            object.undraw()

        #set undo to true and tells other functions that an option has been chosen
        undo, option_chosen = True, True
    #when user clicks redo
    elif abs(xVal1) <= 69 and abs(220 - yVal1) <= 22 or abs(xVal2) <= 69 and abs(220 - yVal2) <= 22:
        #undrawing any click animations
        for object in clickAnim_list:
            object.undraw()

        #set redo to true and tells other functions that an option has been chosen
        redo, option_chosen = True, True
    #when user clicks reset
    elif abs(xVal1) <=  53 and abs(500 - yVal1) <= 10 or abs(0 - xVal2) <= 53 and abs(500 - yVal2) <= 10:
        #undrawing any click animations
        for object in clickAnim_list:
            object.undraw()

        #draws entry box in which user can input yes or no
        user_box.setText("Reset? (y/n)")
        user_box.draw(win)
        
        #put in a while true loop with try and excepts to make sure the code doesn't break from user error
        while True:
            user_key = win.getKey()
            if user_key == "BackSpace":
                text_list.pop()
            elif user_key == "Return":
                break
            else:
                text_list.append(user_key)

            #sets entry box to user input
            user_box.setText("".join(text_list))
            win.redraw()

        #gets input
        option = "".join(text_list)
        #tells other functions that an option has been chosen
        option_chosen = True

        #if y or yes was inputted, it will close the window and sets reset_canvas to None to make program reset
        if option == "y" or option == "yes":
            win.close()
            reset_canvas = None
    #when user clicks on escape button
    elif abs(xVal1) <= 53 and abs(550 - yVal1) < 10 or abs(xVal2) <= 53 and abs(550 - yVal2) < 10:
        #undrawing any click animations
        for object in clickAnim_list:
            object.undraw()

        #Same thing as reset button except it sets reset_canvas to True which quits and closes the program
        user_box.setText("Escape? (y/n)")
        user_box.draw(win)

        while True:
            user_key = win.getKey()
            if user_key == "BackSpace":
                text_list.pop()
            elif user_key == "Return":
                break
            else:
                text_list.append(user_key)

            user_box.setText("".join(text_list))
            win.redraw()

        option = "".join(text_list)
        option_chosen = True

        if option == "y" or option == "yes":
            win.close()
            reset_canvas = True
        else:
            pass

    #if an option has been chosen it will undraw entry box and reset variables
    if option_chosen == True:
        xVal1, yVal1, xVal2, yVal2, point_list = 0, 0, 0, 0, []
        user_box.undraw()


def main_loop():
    #accessing global variables
    global win, objects_drawn, objects_removed
    global xVal1, yVal1, xVal2, yVal2, point_list
    global line_thickness, shape, red, green, blue
    global reset_canvas, undo, redo, option_chosen
    global clickAnim, clickAnim_list

    #setting the option_border to False
    option_border = Line(Point(150, 0), Point(150, 1000))

    #the loop that is the bulk of the code
    while True:
        option_border.undraw()

        #resetting/setting variables
        xVal1, yVal1, xVal2, yVal2, point_list, clickAnim_list, draw_obj = 0, 0, 0, 0, [], [], None
        option_chosen, undo, redo = False, False, False
        
        #drawing/redrawing option menu
        option_bg, option_border = Rectangle(Point(0,0), Point(100, 1000)), Line(Point(100, 0), Point(100, 1000))
        option_bg.setFill("light grey")
        option_bg.setOutline("light grey")

        if line_thickness <= 30:
            option_border.setWidth(line_thickness)
        else:
            option_border.setWidth(30)

        #drawing thickness button
        thickness_button0, thickness_button1, thickness_button2, thickness_button3, thickness_button4 = Rectangle(Point(20, 50), Point(69, 70)), Line(Point(27, 50), Point(27, 70)), Line(Point(35, 50), Point(35, 70)), Line(Point(45, 50), Point(45, 70)), Line(Point(57, 50), Point(57, 70))
        thickness_button0.setFill("white")
        thickness_button1.setWidth(3)
        thickness_button2.setWidth(5)
        thickness_button3.setWidth(7)
        thickness_button4.setWidth(9)

        #drawing colour button
        colour_button, colour_symbol = Rectangle(Point(19, 90), Point(68, 120)), Rectangle(Point(29, 90), Point(58, 120))
        colour_button.setFill("white")
        colour_symbol.setFill(color_rgb(red, green ,blue))

        #drawing shape button
        shape_button = Rectangle(Point(19, 140), Point(68, 170))
        shape_button.setFill("white")
        if shape == "line":
            shape_symbol =  Line(Point(24, 155), Point(63, 155))
        elif shape == "rectangle":
            shape_symbol = Rectangle(Point(24, 145), Point(63, 165))
        elif shape == "oval":
            shape_symbol = Circle(Point(43.5, 155), 10)
        elif shape == "polygon":
            shape_symbol = Polygon(Point(57, 165), Point(43.5, 145), Point(30, 165))
        elif shape == "text":
            shape_symbol = Text(Point(43.5, 155), "TEXT")
        shape_symbol.setFill("black")

        #drawing undo and redo buttons
        undo_button, redo_button, undo_symbol, redo_symbol = Rectangle(Point(18, 240), Point(38, 200)), Rectangle(Point(70, 240), Point(50, 200)), Polygon(Point(18, 220), Point(38, 200), Point(38, 240)), Polygon(Point(70, 220), Point(50, 200), Point(50, 240))
        undo_button.setFill("white")
        redo_button.setFill("white")
        undo_symbol.setFill("black")
        redo_symbol.setFill("black")

        #drawing clear and escape buttons
        clear_button, escape_button = Text(Point(43, 500), "♻"), Text(Point(43, 550), "❌")
        clear_button.setSize(20)
        escape_button.setSize(20)

        #drawing the whole option menu
        option_bg.draw(win)
        option_border.draw(win)

        thickness_button0.draw(win)
        thickness_button1.draw(win)
        thickness_button2.draw(win)
        thickness_button3.draw(win)
        thickness_button4.draw(win)

        colour_button.draw(win)
        colour_symbol.draw(win)

        shape_button.draw(win)
        shape_symbol.draw(win)

        undo_button.draw(win)
        redo_button.draw(win)
        undo_symbol.draw(win)
        redo_symbol.draw(win)

        clear_button.draw(win)
        escape_button.draw(win)

        #calls function to get mouse coordinates
        multi_coord_mouse()

        #resets/quits program
        if reset_canvas == None or reset_canvas == True:
            break

        #setting line
        if shape == "line":
            draw_obj = Line(Point(xVal1, yVal1), Point(xVal2, yVal2))
        #setting rectangles
        elif shape == "rectangle":
            draw_obj = Rectangle(Point(xVal1, yVal1), Point(xVal2, yVal2))
        #setting ovals
        elif shape == "oval":
            draw_obj = Oval(Point(xVal1, yVal1), Point(xVal2, yVal2))
        #setting polygons
        elif shape == "polygon":
            draw_obj = Polygon(point_list)
        #setting text
        elif shape == "text":
            draw_obj = Entry(Point(xVal1, yVal1), 10)
            draw_obj.setText("___")

        #undoing, redoing and drawing shapes
        try:
            #if undo is true, it will undraw the most recently drawn object (works infinitely)
            if undo == True:
                last_object_drawn = objects_drawn.pop()
                last_object_drawn.undraw()
                objects_removed.append(last_object_drawn)
            #if redo is true, it will draw the most recently undrawn object (works infinitely)
            elif redo == True:
                last_object_drawn = objects_removed.pop()
                last_object_drawn.draw(win)
                objects_drawn.append(last_object_drawn)
            #draws shapes
            elif option_chosen == False:
                #checks to make sure that the user didn't click on the option menu
                if not abs(xVal1) <= 100 and abs(150 - yVal1) < 1000: 
                    if not abs(xVal2) <= 100 and abs(150 - yVal2) < 1000:
                        #drawing objects
                        draw_obj.setWidth(line_thickness)
                        draw_obj.setFill(color_rgb(red, green, blue))
                        draw_obj.draw(win)
                        objects_drawn.append(draw_obj)
                    elif shape == "text":
                        try:
                            draw_obj.setSize(line_thickness)
                        except Exception as e:
                            print(e)
                            draw_obj.setSize(5)
                        draw_obj.setTextColor(color_rgb(red, green, blue))
                        draw_obj.draw(win)
                        objects_drawn.append(draw_obj)

                #checks to make sure that the user didn't click on the option menu (polygon only)
                passed_check = None
                for point in point_list:
                    xVal1 = point.getX()
                    yVal1 = point.getY()
                    if not abs(xVal1) <= 100 and abs(150 - yVal1) < 1000:
                        passed_check = True
                    elif abs(xVal1) <= 100 and abs(150 - yVal1) < 1000:
                        passed_check = False
                        break

                if passed_check == True:
                    #drawing polygon
                    draw_obj.setWidth(line_thickness)
                    draw_obj.setFill(color_rgb(red, green, blue))
                    draw_obj.draw(win)
                    objects_drawn.append(draw_obj)

                #undraws all click animations
                try:
                    for object in clickAnim_list:
                        object.undraw()
                #makes sure that code doesn't die from any errors and prints them instead
                except Exception as e:
                    print(e)
                    pass
        except Exception as e:
            print(e)
            pass

#playing background music
def bg_music():
    global reset_canvas, windows_device
    global start_program_file, background_file
    if windows_device == True:
        winsound.PlaySound(start_program_file, winsound.SND_FILENAME + winsound.SND_NODEFAULT)
        winsound.PlaySound(background_file, winsound.SND_ASYNC + winsound.SND_NODEFAULT + winsound.SND_LOOP)

#Function that loops the main loop
def main_looping_loop():
    #accessing global variables
    global win, xVal1, yVal1, xVal2, yVal2, point_list, line_thickness, shape, red, green, blue, undo, redo, objects_drawn, objects_removed, option_chosen, reset_canvas
    #as long as reset_canvas isn't true it will keep looping the main loop
    while reset_canvas is not True:
        #setting variables
        win = GraphWin("Graphics PRO++", 1500, 800, autoflush=False)
        xVal1, yVal1, xVal2, yVal2, point_list = 0, 0, 0, 0, []
        line_thickness, shape = 10, "line"
        red, green, blue = 0, 0, 0
        undo, redo, objects_drawn, objects_removed = False, False, [], []
        option_chosen = False
        reset_canvas = False
        #calling main loop
        main_loop()


#starts the program
if __name__ == '__main__':
    #starts a thread which allow paint program to work with music
    Thread(target = bg_music).start()
    #calls paint program as a main thread
    main_looping_loop()
else:
    print("Hello there")

winsound.PlaySound(None, winsound.SND_PURGE)
