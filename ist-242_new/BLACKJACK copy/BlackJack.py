import random
import os
from tkinter import *
from PIL import ImageTk, Image, ImageDraw

CARD_DECK_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "CardDeckSmall"
)

# One value per numbered PNG file.
# 1-4 = 10s; 5-36 = 2s through 9s; 37-40 = Aces;
# 41-52 = Jacks, Kings, Queens.
CARD_VALUES = (
    [10] * 4
    + [value for value in range(2, 10) for _ in range(4)]
    + [11] * 4
    + [10] * 12
)

ACE_CARDS = {37, 38, 39, 40}

deck = []
playerHand = []
dealerHand = []
playerImg = []
dealerImg = []

game_over = False
dealer_card_hidden = True


def createDeckofCards():
    global deck
    deck = list(range(1, 53))


def draw_card(hand, image_list):
    selected_index = random.randrange(len(deck))
    card_number = deck.pop(selected_index)

    hand.append(card_number)
    image_list.append(NewCard(card_number))


def Deal(dealCount, hand, image_list):
    for _ in range(dealCount):
        draw_card(hand, image_list)


def NewCard(card_number):
    image_path = os.path.join(CARD_DECK_DIR, f"{card_number}.png")
    return ImageTk.PhotoImage(Image.open(image_path))


def hand_value(hand):
    total = sum(CARD_VALUES[card - 1] for card in hand)
    ace_count = sum(1 for card in hand if card in ACE_CARDS)

    # An Ace starts as 11. Change it to 1 if the hand would bust.
    while total > 21 and ace_count > 0:
        total -= 10
        ace_count -= 1

    return total


def update_scores():
    player_score.set(f"Player: {hand_value(playerHand)}")

    if dealer_card_hidden:
        dealer_score.set(f"Dealer: {CARD_VALUES[dealerHand[0] - 1]}")
    else:
        dealer_score.set(f"Dealer: {hand_value(dealerHand)}")

    deck_count.set(f"Cards left: {len(deck)}")


def clear_cards():
    for widget in dealer_frame.winfo_children():
        widget.destroy()

    for widget in player_frame.winfo_children():
        widget.destroy()


def display_cards():
    clear_cards()

    # Dealer: second card is a blue card back until the player stands.
    for index, image in enumerate(dealerImg):
        if index == 1 and dealer_card_hidden:
            Label(dealer_frame, image=card_back_img, bg="green").grid(
                row=0, column=index, padx=5
            )
        else:
            card_label = Label(dealer_frame, image=image, bg="green")
            card_label.image = image
            card_label.grid(row=0, column=index, padx=5)

    # Player: always show every card.
    for index, image in enumerate(playerImg):
        card_label = Label(player_frame, image=image, bg="green")
        card_label.image = image
        card_label.grid(row=0, column=index, padx=5)

    update_scores()


def finish_game():
    global game_over

    player_total = hand_value(playerHand)
    dealer_total = hand_value(dealerHand)

    if player_total > 21:
        result.set("Bust! Dealer wins.")
    elif dealer_total > 21:
        result.set("Dealer busts — you win!")
    elif player_total > dealer_total:
        result.set("You win!")
    elif dealer_total > player_total:
        result.set("Dealer wins.")
    else:
        result.set("Push — tie game.")

    game_over = True
    hit_button.config(state=DISABLED)
    stand_button.config(state=DISABLED)


def PlayerDeal():
    global game_over

    if game_over:
        return

    draw_card(playerHand, playerImg)
    display_cards()

    if hand_value(playerHand) > 21:
        dealer_card_hidden = False
        display_cards()
        finish_game()


def Stand():
    global dealer_card_hidden

    if game_over:
        return

    dealer_card_hidden = False

    # Dealer must draw until reaching 17 or more.
    while hand_value(dealerHand) < 17:
        draw_card(dealerHand, dealerImg)

    display_cards()
    finish_game()


def NewGame():
    global playerHand, dealerHand, playerImg, dealerImg
    global game_over, dealer_card_hidden

    createDeckofCards()

    playerHand = []
    dealerHand = []
    playerImg = []
    dealerImg = []

    game_over = False
    dealer_card_hidden = True

    Deal(2, dealerHand, dealerImg)
    Deal(2, playerHand, playerImg)

    result.set("")
    hit_button.config(state=NORMAL)
    stand_button.config(state=NORMAL)

    display_cards()

    # A player blackjack should end the round immediately.
    if hand_value(playerHand) == 21:
        dealer_card_hidden = False
        display_cards()
        finish_game()


window = Tk()
window.title("Black Jack Game")
window.geometry("850x600")
window.configure(background="green")

# A program-created blue card back, since no card-back PNG was attached.
back_image = Image.new("RGB", (57, 100), "#1666c5")
back_draw = ImageDraw.Draw(back_image)
back_draw.rectangle((3, 3, 53, 96), outline="white", width=2)
card_back_img = ImageTk.PhotoImage(back_image)

player_score = StringVar()
dealer_score = StringVar()
deck_count = StringVar()
result = StringVar()

Label(window, text="BLACK JACK", bg="green", font=("Arial", 20, "bold")).place(
    relx=0.5, rely=0.03, anchor=N
)

Label(window, textvariable=dealer_score, bg="green", font=("Arial", 13)).place(
    relx=0.1, rely=0.16, anchor=NW
)

dealer_frame = Frame(window, bg="green")
dealer_frame.place(relx=0.12, rely=0.22, anchor=NW)

Label(window, textvariable=player_score, bg="green", font=("Arial", 13)).place(
    relx=0.1, rely=0.53, anchor=NW
)

player_frame = Frame(window, bg="green")
player_frame.place(relx=0.12, rely=0.59, anchor=NW)

Label(window, textvariable=deck_count, bg="green").place(
    relx=0.75, rely=0.84, anchor=SW
)

Label(window, textvariable=result, bg="green", font=("Arial", 16, "bold")).place(
    relx=0.5, rely=0.78, anchor=CENTER
)

hit_button = Button(window, text="HIT", command=PlayerDeal)
hit_button.place(relheight=0.08, relwidth=0.18, relx=0.38, rely=0.92, anchor=S)

stand_button = Button(window, text="STAND", command=Stand)
stand_button.place(relheight=0.08, relwidth=0.18, relx=0.58, rely=0.92, anchor=S)

Button(window, text="NEW GAME", command=NewGame).place(
    relheight=0.06, relwidth=0.14, relx=0.82, rely=0.92, anchor=S
)

NewGame()
window.mainloop()