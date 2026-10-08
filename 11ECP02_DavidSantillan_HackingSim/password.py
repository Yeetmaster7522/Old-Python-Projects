from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from itertools import product
from time import perf_counter as pfc
from random import randint



class password:
    def __init__(self,
                 password: str, 
                 lower: bool, 
                 upper: bool, 
                 numbers: bool, 
                 symbols: bool,
                 queue=None #need to add function so class can run without queue
                 ):
        """
        Create password object with a password and details about it.
        To reduce time for demonstration, it takes the length of the
        given password instead of guessing it.\n
        This also initialises a common password database.
        queue is a multiprocessing Queue object
        """
        
        self.queue = queue #communication with main

        #traits about the password
        self.password = password
        self.lower = lower
        self.upper = upper
        self.numbers = numbers
        self.symbols = symbols
        self.length = len(self.password)

        #recommendations
        self.recommend = "Recommended:\n"

        #get common passwords
        self.commonPasswords = self.getCommonPasswords()
    
    def getCommonPasswords(self) -> list:
        """
        Return list of common passwords
        """
        
        commonPasswords = []
        try: #try to open files to get common passwords
            f = open("11ECP02_DavidSantillan_HackingSim\\commonPasswords.txt", "r")
        except:
            f = open("commonPasswords.txt", "r")

        #add to the list of common passwords
        for line in f:
            line = line.removesuffix("\n")
            if len(line) == self.length:
                commonPasswords.append(line)

        f.close()

        return commonPasswords

    def possiblePasswords(self, possible: str) -> map:
        """
        outputs a map object with all of the possible combinations of the characters in possible.
        the strings in the output are of self.length characters
        """
        return map("".join, product(possible, repeat=self.length))

    def update(self, text: str, percent: int):
        """
        Add to multiprocessing queue.\n
        Also prints debug info about what is added to the queue.
        """
        #add text and percent to queue
        if self.queue:
            self.queue.put(text)
            self.queue.put(percent)
        print("checking", text, percent) #output debug info, useful for testing just the password solver

    def searchCommon(self) -> bool:
        """
        checks if the password is in common passwords
        """

        self.update("CHECKING COMMON PASSWORDS", 10+randint(0,5)) #update GUI

        #check if password in common passwords
        #this works because it is essentially a for loop but python makes it look different
        if self.password in self.commonPasswords:
            self.recommend += "- Make your password more unique\n\tYour password is a common password.\n"
            return True
        return False
    
    def searchMixed(self) -> bool:
        """
        creates a str of characters that fit the given description of the
        password from initialisation, creates a list of possible combinations
        using that, and then checks if it is in there
        """

        if self.queue: self.queue.put(30)
        #creating str of valid characters that fit password description
        valid = "" #what is given to possiblePasswords()
        validOut = "" #what is given to the user
        if self.lower:
            valid += ascii_lowercase
            validOut += f"- {ascii_lowercase}\n"
        if self.upper:
            valid += ascii_uppercase
            validOut += f"- {ascii_uppercase}\n"
        if self.numbers:
            valid += digits
            validOut += f"- {digits}\n"
        if self.symbols:
            valid += punctuation
            validOut += f"- {punctuation}\n"

        self.update(f"checking passwords with:\n{validOut}", 50+randint(-10,10)) #update GUI

        possiblePass = self.possiblePasswords(valid) #find all possible combinations

        #check if password in possible passwords
        #this works because it is essentially a for loop but python makes it look different
        if self.password in possiblePass: #check if it is in there
            #adding to recommendations
            if not self.lower: self.recommend += "- Add lowercase letters\n"
            if not self.upper: self.recommend += "- Add uppercase letters\n"
            if not self.numbers: self.recommend += "- Add numbers\n"
            if not self.symbols: self.recommend += "- Add symbols\n"
            return True

        return False

    def solve(self) -> tuple[int, str]:
        """
        starts a timer
        """

        startTime = pfc()
        if self.searchCommon() or self.searchMixed(): #call both functions sequentially and check if the password is found
            time = pfc()-startTime
            #add password length recommendation if it is not long enough
            if self.length < 10: self.recommend += "- Increase password length\n\tRecommended at least 10 characters."
            
            return time, self.recommend
        return -1, "ERROR PASSWORD NOT FOUND WITH GIVEN TRAITS" #give an error if not found


#used for testing the solver without GUI involved
if __name__ == "__main__":
    #inputs to test out password solver
    passwordInput = "apple1"
    lower = True
    upper = False
    number = False
    symbol = False

    PW = password(passwordInput, lower, upper, number, symbol)
    print(PW.solve()) #solve