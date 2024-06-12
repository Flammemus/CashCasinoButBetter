import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from art import *
import survey

from coinflip import coinflip

cred = credentials.Certificate("myKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

games = ["Coinflip", "Wheel"]
def showCommands():
    print("Command\tDescription\n")
    print("Bal\tdisplays current balance")
    print("Logout\tlogs out of account")
    print("Help\tdisplays list of commands")

def login(db):
    print("----------------------------------\n")
    accountActions = ("Create new account", "Log into existing account", "Log into test account")
    index = survey.routines.select('Choose account actions: ', options = accountActions)
    print()

    if index == 0:
        while True:
            accountName = input("Username: ")

            if db.collection("Accounts").document(accountName).get().exists:
                print("Name is taken")
            else:
                break

        accountPassword = survey.routines.conceal('Password: ')

        db.collection("Accounts").document(accountName).set({
            "Password": accountPassword,
            "Balance": 100
        })

    elif index == 1:
        while True:
            accountName = input("Username: ")

            if not db.collection("Accounts").document(accountName).get().exists:
                print("Incorrect username")
            else:
                break

        storedPassword = db.collection("Accounts").document(accountName).get().to_dict().get("Password")
        enteredPassword = survey.routines.conceal('Password: ')

        if enteredPassword == storedPassword:
            print("Login successful")
        else:
            print("Incorrect password.")

    elif index == 2:
        accountName = "test"
        db.collection("Accounts").document(accountName)
        print("Login successful")
    
    return accountName

accountName = login(db)

def getBalance(accountName):
    balance = db.collection("Accounts").document(accountName).get().to_dict().get("Balance")
    return int(balance)

balance = getBalance(accountName)

def updateBalance(accountName, balance):
    if db.collection("Accounts").document(accountName) is not None:
        db.collection("Accounts").document(accountName).update({"Balance": balance})

def introduction():
    getBalance(accountName)
    print(f"Your current balance: {balance}")

def startGame(gameFunction, balance):
    while True:
        betAmount = input(f"Bet amount? Your balance: {balance} ('Back' to return): ")
        if betAmount.lower() == "back":
            print("\nGoing back to menu\n")
            print("------------------")
            break
        
        elif int(betAmount) > balance:
            print("Bet amount cannot exceed current balance")
        
        elif int(betAmount) <= balance:
            balance = gameFunction(betAmount, balance)
            updateBalance(accountName, balance)

def leaderboard():
    accounts = []

    for doc in db.collection("Accounts").get():
        accounts.append((doc.id, doc.to_dict()["Balance"]))
    
    leaderboard = sorted(accounts, reverse=True, key=lambda x: x[1])
    
    print("Rank\tAccount\t\tBalance\n")
    for i, (account, balance) in enumerate(leaderboard, start=1):
        print(f"{i}\t{account}\t\t{balance}")

tprint("Cash Cruise")
print("A pay to win service\n")
introduction()

mainloop = True
while mainloop:

    updateBalance(accountName, balance)

    print()
    mainloopActions = ("Display balance", "Reset balance", "Start coinflip", "Leaderboard", "Save", "Logout")
    index = survey.routines.select('Choose mainloop action ', options = mainloopActions)
    print()

    if index == 0:
        print(balance)
    
    elif index == 1:
        balance = 100
    
    elif index == 2:
        startGame(coinflip, balance)

    elif index == 3:
        leaderboard()
    
    elif index == 4:
        updateBalance(accountName, balance)
    
    elif index == 5:
        login(db)
        mainloop = False