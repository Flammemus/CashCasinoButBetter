import random
import time
import survey

def coinflip(betAmount, balance):

    print()
    action = ("Heads", "Tails")
    index = survey.routines.select('Pick a side', options = action)
    
    if random.randint(1, 2) == 1:
        result = 1
    
    else:
        result = 2

    def printHeads():
        print("\r| Heads |", end="")

    def printTails():
        print("\r| Tails |", end="")

    while True:

        print()
        p = 0.05
        for i in range(10):
            printHeads()
            time.sleep(p)
            p = p * 1.1
            printTails()
            time.sleep(p)
            p = p * 1.1

        if result == "h":
            printHeads()
            print("\r")
        else:
            printTails()
            print("\r")

        time.sleep(0.5)
    
        if index == result:
            print("\nYou win!\n")
            balance += int(betAmount)
        else:
            print("\nYou lose!\n")
            balance -= int(betAmount)

        return balance

# coinflip(100, 10000)