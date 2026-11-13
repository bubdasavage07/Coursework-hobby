import random
import os
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

#create a deck loop (array list) to remove duplicates
#create a common function for appending player's cards
    ## basically creating the player's hand of cards.

Xpos = 100
deck = []
playerHand = []
dealerHand = []
playerImg = []
dealerImg = []
cardcounter = 2
CARD_DECK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CardDeckSmall")

#popping the int values from the deck array should
  # handle the need to check for repeating card values
#def checkRepeat():
    #code

#place the 'popped' cards after each round in this function
#def discardPile():
    #code

def countDeck():
    return ("Number of cards left: ", len(deck))

#function to create a 52 card deck of integers
def createDeckofCards(): 
    for i in range(1, 53):
        deck.append(i)
    #print(deck)


#general deal function (# of cards desired, to which hand)
def Deal(dealCount, hand, img): 
    for i in range(dealCount):
        selectedCardInt = random.randrange(len(deck))
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
    cardImage = ImageTk.PhotoImage(Image.open(os.path.join(CARD_DECK_DIR, str(x)+'.png')))
    return cardImage

def NewDeal():
    global Xpos
    global playerImg, dealerImg
            
    dealer1 = Label(window, image=dealerImg[0]).place(anchor='n',x=100, y=150)
    dealer2 = Label(window, image=dealerImg[1]).place(anchor='n',x=175, y=150)
        
    player1 = Label(window, image=playerImg[0]).place(anchor='n', x=Xpos, y=340)
    Xpos = Xpos + 75
    player2 = Label(window, image=playerImg[1]).place(anchor='n', x=Xpos, y=340)

def PlayerDeal():
    global Xpos, playerHand, playerImg, cardcounter
    Xpos = Xpos + 75
    Deal(1, playerHand, playerImg)
    Label(window, image=playerImg[cardcounter]).place(anchor='n', x=Xpos, y=340)
    Label(window, text=countDeck()).place(relx=0.7, rely=0.85, anchor=SW)
    cardcounter += 1
    
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
