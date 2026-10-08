#import things needed
from tkinter import ttk, StringVar, BooleanVar, Tk, Toplevel, PhotoImage
from password import password
from multiprocessing import Process, Queue



def worker(queue: Queue, 
           passInput: str, 
           lower: bool, 
           upper: bool, 
           number: bool, 
           symbol: bool):
    """
    creates password objects and solves the passwordInput
    """
    PW = password(passInput, lower, upper, number, symbol, queue=queue) #init password class
    t, r = PW.solve() #solve password and get outputs

    #add to queue
    queue.put(f"Password cracked in\n{t}\nseconds...")
    queue.put(r)
    queue.put(100)

def solve(root: Tk, 
          passInput: str, 
          lower: bool, 
          upper: bool, 
          number: bool, 
          symbol: bool):
    """
    window for cracking the password
    """
    
    queue = Queue() #create multiprocessing queue

    #configure window
    window = Toplevel(root)
    window.geometry("270x200")
    window.title("Sim Window")
    window.configure(background="#170F11")
    window.resizable(False, False)

    #configure items within the window
    label = ttk.Label(window, text="SIMULATING BRUTE FORCE ATTACK")
    progressBar = ttk.Progressbar(window, orient="horizontal", mode="determinate", length=230, maximum=100)
    recommend = ttk.Label(window, text="")

    label.pack(anchor="w")
    progressBar.pack(anchor="w")
    recommend.pack(anchor="w")


    def update():
        """
        Updates GUI
        """
        
        try:
            result = queue.get_nowait() #get item from queue without blocking
        except Exception: #if queue empty do nothing
            pass
        else: #update if queue is not empty
            #updates GUI depending on the type of item taken from the queue
            if isinstance(result, str):
                if "Recommended" in result:
                    recommend.config(text=result)
                else:
                    label.config(text=result)
            elif isinstance(result, int):
                progressBar["value"] = result

        #update window every 100 ms
        window.update_idletasks()
        window.after(100, update)

    #start a worker thread to work in the background so that the GUI do not get stopped by trying to solve the password
    Process(
        target=worker, 
        args=(queue, passInput, lower, upper, number, symbol), 
        daemon=True
        ).start()

    window.after(100, update) #start updating GUI
    window.mainloop()

def main():
    """
    mainloop that contains and runs the main window which gets input from the user
    """
    #init and config main window
    root = Tk()
    root.geometry("300x300")
    root.title("Brute Force Hacker Sim")
    root.config(bg="#170F11", border=5, borderwidth=5)
    root.resizable(False, False)

    #try to get photo
    try:
        photo = PhotoImage(file="11ECP02_DavidSantillan_HackingSim\\icon.png")
    except:
        photo = PhotoImage(file="icon.png")
    #set the photo as the icon photo
    root.wm_iconphoto(True, photo)

    #configure theme of the program
    style = ttk.Style() #colour scheme: FFFCF9, 170F11, F72585, 7209B7, 3A0CA3, 4361EE, 4CC9F0
    style.theme_use("clam")
    style.configure("TLabel", background="#170F11", foreground="#FFFCF9")
    style.configure("TEntry", foreground="#7209B7")
    style.configure("TCheckbutton", background="#170F11", foreground="#FFFCF9")
    style.configure("TButton", foreground="#FFFCF9", background="#7209B7")
    style.configure("Horizontal.TProgressbar", background="#4CC9F0", troughcolor="#7209B7")

    style.map("TCheckbutton", #remove highlight
              background=[
                  ("active", "#170F11"),
                  ("!focus", "#170F11")],
                  )
    
    style.map("TButton", #make button change colour if hovered on
              background=[
                  ("active", "#F72585"),
                  ("!focus", "#7209B7")
              ]
              )

    #create variables to pass to solve()
    passInput = StringVar()
    lower = BooleanVar()
    upper = BooleanVar()
    number = BooleanVar()
    symbol = BooleanVar()

    #getting password for confirmation
    ttk.Label(root, text="What is your password (this will not be saved)").pack(side="top", pady=5)
    ttk.Entry(root, textvariable=passInput, justify="center", show="*").pack(side="top", pady=5)

    #checkboxes for misc details about the password
    ttk.Label(root, text="Tick the following that applies:").pack(side="top", pady=(20,5))
    ttk.Checkbutton(root, text="Does it have lowercase letters?", variable=lower).pack(
        side="top", 
        pady=5, 
        padx=(70,0), 
        anchor="w"
        )
    ttk.Checkbutton(root, text="Does it have uppercase letters?", variable=upper).pack(
        side="top",
        pady=5, 
        padx=(70,0), 
        anchor="w"
        )
    ttk.Checkbutton(root, text="Does it have numbers?", variable=number).pack(
        side="top", 
        pady=5, 
        padx=(70,0), 
        anchor="w"
        )
    ttk.Checkbutton(root, text="Does it have symbols?", variable=symbol).pack(
        side="top", 
        pady=(5,20), 
        padx=(70,0), 
        anchor="w"
        )

    ttk.Button(root, text="CRACK PASSWORD",
               command=lambda: solve(root, passInput.get(), lower.get(), upper.get(), number.get(), symbol.get()) #call solve() when pressed
               ).pack(side="top")

    root.mainloop() #start tkinter mainloop



if __name__ == "__main__": #start program
    main()