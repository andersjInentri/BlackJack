import tkinter as tk
from tkinter import ttk, messagebox
import random

root = tk.Tk()
root.title("BlackJack")
root.geometry("500x200")

#Gjorde det så här INNAN jag lärde att jag kunde göra både random.shuffle() och pop() på listor.
#Ser dock lite coolt ut med nästade listor
colors = [["H", "♥"], ["D", "♦"], ["S", "♠"], ["C", "♣"]]
card_no = list(range(1, 14))

#Tillverka kortleken och blanda. "deck" är lista där varje kort är [color["H,D,S,C", "<tecken>"], visat nummer, vikt (klätt-kort har vikt=10 och ess är 11)]
deck = [[color,number,(10 if number > 10 else 11 if number == 1 else number)] for color in colors for number in card_no]
random.shuffle(deck)

#Listor for dealer och player. Appen poppar från deck och lägger kort hos dealer resp. player
dealer_cards = []
player_cards = []

#Dynamiska label som används för att visa kort-represenationer
player_cards_label = tk.StringVar()
dealer_cards_label = tk.StringVar()

#Värden för summan av dealer och players kort
dealer_score_label = tk.StringVar()
player_score_label = tk.StringVar()

#Centrera fönstret
def center_on_screen(win, w=None, h=None):
    win.update_idletasks()
    if w is None or h is None:
        w = win.winfo_width()
        h = win.winfo_height()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

#Initialisering av korten vid spelstart
def init_draw():
    #Lika enkelt som en loop när det bara är 2 kort var....
    dealer_cards.append(deck.pop())
    dealer_cards.append(deck.pop())
    player_cards.append(deck.pop())
    player_cards.append(deck.pop())

#Detta återställer spelet, med resultat och GUI
def game_reset():
    global dealer_cards, player_cards, deck
    dealer_cards = []
    player_cards = []
    deck = [[color,number,(10 if number > 10 else 11 if number == 1 else number)] for color in colors for number in card_no]
    random.shuffle(deck)
    stop_btn.state(["!disabled"])
    draw_btn.state(["!disabled"])
    init_draw()
    refresh_dealer_cards_label()
    refresh_player_cards_label()
    calc_dealer_score(False)
    calc_player_score()
    
#Hämtar info från korten för GUI.
#Lätt att ändra här, på 1 ställe, om man vill ha annan presentation i GUI
def visible_card(card):
    symbol = card[0][1]
    number = card[1]
    return f"{symbol} {number}"

#Funktionen räknar ess som 1 eller 11 beroende på totalen.
def calc_aces(cards):
    total = sum([v[2] for v in cards])
    aces = sum(1 for c in cards if c[1] in (1,1))
    while total > 21 and aces:
        total -= 10
        aces -= 1

    return total


#Summera dealer-poäng. Notera att player_score är global variabel för GUI och eftersom den är global vill 
#jag inte använda den lokalt mer än att sätta den.
def calc_dealer_score(show_all_cards):
    global dealer_score
    if show_all_cards:
        s = calc_aces(dealer_cards)
    else:
        #"Summera" bara första kortet för att inte visa total poäng utan att kortet visas
        s=dealer_cards[0][2]
    dealer_score = s
    dealer_score_label.set(f"Dealer Score: {s}")
    return s

#Summera player-poäng. Notera att player_score är global variabel för GUI och eftersom den är global vill 
#jag inte använda den lokalt mer än att sätta den.
def calc_player_score():
    global player_score
    s = calc_aces(player_cards)
    player_score = s
    player_score_label.set(f"Player Score: {s}")
    if s == 21:
        messagebox.showinfo("You have 21!", "Your score is perfect and you won!")
        draw_btn.state(["disabled"])
        stop_btn.state(["disabled"])
    elif s > 21:
        messagebox.showerror("You are fat!", f"Your score is {s} and max is 21")
        draw_btn.state(["disabled"])
        stop_btn.state(["disabled"])
    return s

#Sätter dealerns kort i label, visar inte kort 2...om det inte ska visas, dvs när player valt att stoppa
def refresh_dealer_cards_label(show_all_cards = False):
    if show_all_cards == False:
        dealer_cards_label.set(visible_card(dealer_cards[0]) + ", <?, ?>")
    else:
        dealer_cards_label.set(", ".join(visible_card(card) for card in dealer_cards))
    return

#Sätter players kort i label, loopar och sätter komma-tecken. Python gör det snyggt
def refresh_player_cards_label():
    player_cards_label.set(", ".join(visible_card(card) for card in player_cards))
    return

#Drar player kort och kallar method för att refresha player label.
def player_draw_card():
    player_cards.append(deck.pop())
    #print(player_cards)
    refresh_player_cards_label()
    calc_player_score()
    return

def dealer_draw_card():
    dealer_cards.append(deck.pop())
    return calc_dealer_score(True)

#Verkar behövs för att en sleep-funktion ska fungera
def dummy():
    return

#Första gången visa upp det dolda kortet, vänta 3 sekunder så player hinner se
#Dealer drar kort och kallar method för att refresha player label.
def dealer_draws():
    stop_btn.state(["disabled"])
    draw_btn.state(["disabled"])
    refresh_dealer_cards_label(True)
    init_sum = calc_dealer_score(True)
    sum = 0
    if (init_sum < 17):
        while sum < 17:
            root.update_idletasks()
            root.after(3000, dummy())
            sum = dealer_draw_card()
            refresh_dealer_cards_label(True)
    if max(sum, init_sum) > 21:
        messagebox.showinfo("Dealer is fat!", f"You won as you had score {calc_player_score()}!")
        draw_btn.state(["disabled"])
    elif max(sum, init_sum) == 21:
        messagebox.showerror("Dealer won!", f"Dealer hit 21 and must stop.")
        draw_btn.state(["disabled"])
    elif max(sum, init_sum) == calc_player_score():
        messagebox.showinfo("Draw!", f"You and dealer have same score {calc_player_score()}!")
        draw_btn.state(["disabled"])
    else:
        messagebox.showinfo("Dealer won!", f"You lost as you had score {calc_player_score()} and dealer {max(sum, init_sum)}!")
    return


init_draw()


#Bygg GUI
style = ttk.Style(root)
style.theme_use("clam")
frm = ttk.Frame(root, padding=10)
frm.grid(sticky="new")
frm2 = ttk.Frame(root, padding=20)
frm2.grid(sticky="sewn")
root.columnconfigure(0, weight=1); root.rowconfigure(0, weight=1)

ttk.Label(frm, text="Dealer Card:").grid(row=0, column=0, padx=6, pady=6, sticky="e")
ttk.Label(frm, textvariable=dealer_score_label).grid(row=1, column=0, padx=1, pady=1, sticky="e")
ttk.Label(frm, textvariable=dealer_cards_label).grid(row=0, column=2, columnspan=3, padx=6, pady=6, sticky="we")

ttk.Label(frm, text="Player Card:").grid(row=5, column=0, padx=6, pady=6, sticky="e")
ttk.Label(frm, textvariable=player_score_label).grid(row=6, column=0, padx=1, pady=1, sticky="e")
ttk.Label(frm, textvariable=player_cards_label).grid(row=5, column=2, columnspan=3, padx=6, pady=6, sticky="we")

draw_btn = ttk.Button(frm2, text="Hit", command=player_draw_card)
draw_btn.grid(row=8, column=1, padx=6, pady=6, sticky="nwe")
stop_btn = ttk.Button(frm2, text="Stand", command=dealer_draws)
stop_btn.grid(row=8, column=2, padx=6, pady=6, sticky="nwe")
reset_btn = ttk.Button(frm2, text="Reset", command=game_reset)
reset_btn.grid(row=8, column=3, padx=6, pady=6, sticky="nwe")

refresh_dealer_cards_label()
refresh_player_cards_label()
calc_dealer_score(False)
calc_player_score()

center_on_screen(root)
root.mainloop()