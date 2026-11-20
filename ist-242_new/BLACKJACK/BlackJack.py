#Blackjack for education, version: 20261119
import random
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image

#create a deck loop (array list) to remove duplicates
#create a common function for appending player's cards
    ## basically creating the player's hand of cards.

Xpos = 100
deck = [] #deck of cards, each card has an assigned integer number
playerHand = []
dealerHand = []
playerImg = []
dealerImg = []
cardcounter = 2
cv = 0
dealerCardValues = []
playerCardValues = []

cardValue = [10, 10, 10, 10, 2, 2, 2, 2, 3, 3, 3, 3,
             4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7,
             7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 11, 11, 11, 11,
             10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

#popping the int values from the deck array should
  # handle the need to check for repeating card values
#def checkRepeat():
    #code

#place the 'popped' cards after each round in this function
#def discardPile():
    #code

def countDeck():
    return ("Number of cards left: ", len(deck))

#Create a 52 card deck of integers
def createDeckofCards(): 
    for i in range(1, 53):
        deck.append(i)
    #print(deck)


#general deal function (# of cards desired, to which hand)
def Deal(dealCount, hand, img): 
    for i in range(dealCount):
        selectedCardInt = random.randint(0, len(deck))
        hand.append(deck[selectedCardInt])
        img.append(NewCard(deck[selectedCardInt]))
        deck.pop(selectedCardInt)
        
'''
def randomize():
    rand = random.randint(0, 52)
    ifzero = random.randint(0, 52)
    if rand == 0:
        rand = (rand + ifzero + 1)/2
    return int(rand)
'''

#use the card's int value to assign its proper image
def NewCard(x):
    global cardImage
    global cardValue
    cardImage = ImageTk.PhotoImage(Image.open('./CardDeckSmall/'+str(x)+'.png'))
    #print("card file # ", x)
    #print("card value ", cardValue[x-1])
    # #### global cv = cardValue[x-1]
    #print(cardcounter)
    #deckcount = countDeck()
    #print(deckcount)
    if len(deck) > 50:
        dealerCardValues.append(cardValue[x-1])
    else:
        playerCardValues.append(cardValue[x-1])
    return cardImage

def NewDeal():
    global Xpos
    global playerImg, dealerImg
    global dealerCardValues, playerCardValues
            
    dealer1 = Label(window, image=dealerImg[0]).place(anchor='n',x=100, y=150)
    dealer2 = Label(window, image=dealerImg[1]).place(anchor='n',x=175, y=150)
    print("Dealer card values: ", dealerCardValues)
    
    player1 = Label(window, image=playerImg[0]).place(anchor='n', x=Xpos, y=340)
    Xpos = Xpos + 75
    player2 = Label(window, image=playerImg[1]).place(anchor='n', x=Xpos, y=340)
    print("Player card values: ", playerCardValues)

def PlayerDeal():
    global Xpos, playerHand, playerImg, cardcounter
    Xpos = Xpos + 75
    Deal(1, playerHand, playerImg)
    Label(window, image=playerImg[cardcounter]).place(anchor='n', x=Xpos, y=340)
    Label(window, text=countDeck()).place(relx=0.7, rely=0.85, anchor=SW)
    cardcounter += 1
    print("Player selected to add cards: ", playerCardValues)
    plyrTotal = sum(playerCardValues)
    if plyrTotal > 21:
        messagebox.showwarning("BUSTED!!", "Your message here", parent=window, detail="Extra text")
        #messagebox.showinfo(title="Window Title", message="Your message here", **options)
    
'''--------------------------------------
  **NOTES:
  Array List to create cards instead of cardImage1,2,3,etc
  Code the DEAL button to add more cards to the player's screen.
  Better screen design
  Assign values to the card deck for scoring  
'''
#-------PROGRAM START-------------------
window = Tk() #constructor
window.title("Black Jack game")
window.geometry('850x600')
window.configure(background = "green")
createDeckofCards()

#frm = ttk.Frame(window, padding=50)
#frm.grid(column=2, row=2)
Label(window, text="BLACK JACK").place(relx=0.5, anchor=N)

Label(window, text="Dealer:").place(relx=0.1, rely=0.2, anchor=NW)
Deal(2, dealerHand, dealerImg)
#print(dealerHand)

Label(window, text="Player:").place(relx=0.1, rely=0.55, anchor=SW)
Deal(2, playerHand, playerImg)
#print(playerHand)
NewDeal()

Label(window, text=countDeck()).place(relx=0.7, rely=0.85, anchor=SW)

Button(
    window,
    text="DEAL",
    command=PlayerDeal).place(relheight=0.1, relwidth=0.3, relx=0.5, rely=0.9, anchor=S)

window.mainloop()


"""
def get_ai_suggestion(player_total: int, dealer_up: int, usable_ace: int) -> str:
    prediction = clf.predict([[player_total, dealer_up, usable_ace]])[0]
    probs = clf.predict_proba([[player_total, dealer_up, usable_ace]])[0]
    confidence = max(probs) * 100
    action = "HIT" if prediction == 1 else "STAND"
    return f"AI suggests: {action} ({confidence:.1f}% confidence)"
"""
