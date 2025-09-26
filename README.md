# BlackJack (Tkinter)

Ett enkelt Blackjack-spel byggt i **Python** med **Tkinter/ttk**. Programmet visar dealer- och spelarhänder, räknar poäng (med korrekt hantering av ess), och har knappar för att **dra (Hit)**, **stanna (Stand)** och **starta om (Reset)**.

## Förutsättningar
- **Python 3.10+** (Tkinter ingår vanligtvis i standardinstallationen)
- Ingen extern beroende krävs

## Kom igång
```bash
# Klona eller kopiera projektet
git clone https://github.com/andersjInentri/BlackJack.git
cd BlackJack

# Kör applikationen
python app.py
# eller
# py app.py      # Windows
# python3 app.py # macOS/Linux
```

## Så här fungerar spelet
- **Kortlek:** 52 kort skapas som `[färg, valör, vikt]`. Klädda kort (11(J), 12(Q), 13(K) ) väger **10**.
- **Ess:** räknas först som **11** men sänks till **1** (–10 i total) om handen överstiger 21.
- **Start:** vid ny omgång dras två kort till dealern (varav ett är dolt med ?, ?) och två till spelaren.
- **Spelare (Hit/Stand):**
  - **Hit**: spelaren drar ett nytt kort.
  - **Stand**: spelaren stannar; dealern visar dolt kort och drar tills totalen är **minst 17**.
- **Resultat:** spelet visar vinst/oavgjort/förlust (och bust om >21).

## Vanliga åtgärder i Tkinter (tips)
- **Pausa utan att frysa GUI:** använd `root.after(ms, func)` i stället för `time.sleep()`.
- **Enable/disable knapp (ttk):**
  ```python
  btn.configure(state="disabled")  # disable
  btn.configure(state="normal")    # enable
  ```
- **Centrera fönstret:**
  ```python
  root.update_idletasks()
  root.eval('tk::PlaceWindow . center')
  ```
- **Blanda inte** `pack()` och `grid()` i samma container.

## Projektstruktur
```
BlackJack/
├─ app.py      # huvudprogram (UI + logik)
└─ README.md   # denna fil
```

