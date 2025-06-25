import tkinter as tk
import random

# Konfigurasi global
card_values = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 11, "Q": 12, "K": 13, "A": 14
}
ranks = list(card_values.keys())
suits = ['♠', '♥', '♦', '♣']
bg_color = "#1e1e2f"  # default bg

# Setup window
root = tk.Tk()
root.title("War Card Game")
root.geometry("600x500")
root.resizable(False, False)

# Global state
current_mode = "menu"
player_score = 0
player2_score = 0
round_number = 1
deck = []

# ---------- GUI Pages ----------
frames = {}

def show_frame(name):
    for f in frames.values():
        f.pack_forget()
    frames[name].pack(fill='both', expand=True)

# ---------- Menu ----------
def build_main_menu():
    frame = tk.Frame(root, bg=bg_color)
    frames["menu"] = frame

    tk.Label(frame, text="WAR CARD GAME", font=("Helvetica", 24, "bold"), bg=bg_color, fg="white").pack(pady=30)

    tk.Button(frame, text="VS CPU", width=20, font=("Arial", 14), command=start_vs_cpu).pack(pady=10)
    tk.Button(frame, text="VS Player", width=20, font=("Arial", 14), command=start_vs_player).pack(pady=10)
    tk.Button(frame, text="Settings", width=20, font=("Arial", 14), command=show_settings).pack(pady=10)
    tk.Button(frame, text="Quit Game", width=20, font=("Arial", 14), command=root.quit).pack(pady=10)

# ---------- Settings ----------
def show_settings():
    frame = frames["settings"]
    show_frame("settings")

def set_bg(color):
    global bg_color
    bg_color = color
    root.config(bg=bg_color)
    for frame in frames.values():
        frame.config(bg=bg_color)
    build_main_menu()
    show_frame("menu")

def build_settings():
    frame = tk.Frame(root, bg=bg_color)
    frames["settings"] = frame

    tk.Label(frame, text="Settings - Background Color", font=("Helvetica", 20, "bold"), bg=bg_color, fg="white").pack(pady=20)

    tk.Button(frame, text="Dark", width=15, command=lambda: set_bg("#1e1e2f")).pack(pady=10)
    tk.Button(frame, text="Blue", width=15, command=lambda: set_bg("#001f3f")).pack(pady=10)
    tk.Button(frame, text="Green", width=15, command=lambda: set_bg("#014421")).pack(pady=10)
    tk.Button(frame, text="Back", command=lambda: show_frame("menu")).pack(pady=20)

# ---------- Game Logic ----------
def draw_cards(mode):
    global player_score, player2_score, round_number, deck

    if round_number > 26:
        end_game(mode)
        return

    p1 = deck.pop()
    p2 = deck.pop()

    card1 = p1
    card2 = p2

    val1 = card_values[card1[:-1]]
    val2 = card_values[card2[:-1]]

    card1_label.config(text=card1)
    card2_label.config(text=card2)

    if val1 > val2:
        player_score += 1
        result = "Player 1 wins the round!"
    elif val1 < val2:
        player2_score += 1
        result = "Player 2 wins!" if mode == "pvp" else "Computer wins!"
    else:
        result = "It's a tie!"

    round_label.config(text="Drawing cards...")
    draw_button.config(state="disabled")
    root.after(1000, lambda: resolve_turn(mode))  # Delay 1 detik
    result_label.config(text=result)
    score_label.config(text=f"P1: {player_score} | P2: {player2_score}")
    round_number += 1

    if round_number > 26:
        draw_button.config(state="disabled")

def resolve_turn(mode):
    global player_score, player2_score, round_number, deck

    p1 = deck.pop()
    p2 = deck.pop()

    val1 = card_values[p1[:-1]]
    val2 = card_values[p2[:-1]]

    card1_label.config(text=p1)
    card2_label.config(text=p2)

    if val1 > val2:
        player_score += 1
        result = "Player 1 wins the round!"
    elif val1 < val2:
        player2_score += 1
        result = "Player 2 wins!" if mode == "pvp" else "Computer wins!"
    else:
        result = "It's a tie!"

    round_label.config(text=f"Round {round_number}/26")
    result_label.config(text=result)
    score_label.config(text=f"P1: {player_score} | P2: {player2_score}")
    round_number += 1

    if round_number > 26:
        draw_button.config(state="disabled")
        save_highscore(mode)
    else:
        draw_button.config(state="normal")

def save_highscore(mode):
    try:
        with open("highscores.txt", "a") as f:
            if mode == "cpu":
                f.write(f"P1: {player_score} - CPU: {player2_score}\n")
            else:
                f.write(f"P1: {player_score} - P2: {player2_score}\n")
    except Exception as e:
        print(f"Gagal menyimpan skor: {e}")

def end_game(mode):
    if player_score > player2_score:
        final = "🎉 Player 1 Wins the Game!"
    elif player_score < player2_score:
        final = "🎉 Player 2 Wins!" if mode == "pvp" else "💻 Computer Wins!"
    else:
        final = "🤝 It's a Draw!"
    result_label.config(text=final)

# ---------- Game UI ----------
def build_game_ui():
    frame = tk.Frame(root, bg=bg_color)
    frames["game"] = frame

    global round_label, card1_label, card2_label, result_label, score_label, draw_button

    tk.Label(frame, text="War Card Battle", font=("Helvetica", 20, "bold"), bg=bg_color, fg="white").pack(pady=10)

    round_label = tk.Label(frame, text="Round 1/26", font=("Arial", 12), bg=bg_color, fg="lightgray")
    round_label.pack()

    cards_frame = tk.Frame(frame, bg=bg_color)
    cards_frame.pack(pady=20)

    card1_label = tk.Label(cards_frame, text="❔", font=("Courier", 36), fg="lightgreen", bg=bg_color)
    card1_label.grid(row=0, column=0, padx=50)

    tk.Label(cards_frame, text="VS", font=("Helvetica", 20), bg=bg_color, fg="white").grid(row=0, column=1)

    card2_label = tk.Label(cards_frame, text="❔", font=("Courier", 36), fg="tomato", bg=bg_color)
    card2_label.grid(row=0, column=2, padx=50)

    result_label = tk.Label(frame, text="", font=("Arial", 12), fg="yellow", bg=bg_color)
    result_label.pack()

    score_label = tk.Label(frame, text="P1: 0 | P2: 0", font=("Arial", 14), bg=bg_color, fg="white")
    score_label.pack(pady=5)

    draw_button = tk.Button(frame, text="Draw Cards", font=("Arial", 14), bg="dodgerblue", fg="white")
    draw_button.pack(pady=20)

    tk.Button(frame, text="Back to Menu", command=lambda: show_frame("menu")).pack(pady=5)

# ---------- Game Starters ----------
def start_vs_cpu():
    start_game("cpu")

def start_vs_player():
    start_game("pvp")

def start_game(mode):
    global player_score, player2_score, round_number, deck
    player_score = 0
    player2_score = 0
    round_number = 1
    deck = [rank + suit for suit in suits for rank in ranks]
    random.shuffle(deck)

    draw_button.config(state="normal")
    draw_button.config(command=lambda: draw_cards(mode))
    show_frame("game")

# ---------- Init ----------
build_main_menu()
build_settings()
build_game_ui()
show_frame("menu")
root.config(bg=bg_color)
root.mainloop()
