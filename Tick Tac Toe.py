import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random

# ---------- Theme Colors ----------
themes = {
    "Lavender": "#e6e6fa",
    "Pink": "#ffe4e1",
    "Yellow": "#fffacd",
    "Green": "#d0f0c0",
    "Blue": "#add8e6"
}
current_theme = "Lavender"

# ---------- Main Window ----------
root = tk.Tk()
root.title("Tic Tac Toe!")
root.geometry("500x500")
root.configure(bg=themes[current_theme])

# ---------- Frames ----------
welcome_frame = tk.Frame(root, bg=themes[current_theme])
menu_frame = tk.Frame(root, bg=themes[current_theme])
settings_frame = tk.Frame(root, bg=themes[current_theme])
game_frame = tk.Frame(root, bg=themes[current_theme])
two_player_frame = tk.Frame(root, bg=themes["Pink"])

def show_frame(frame):
    for f in [welcome_frame, menu_frame, settings_frame, game_frame, two_player_frame]:
        f.pack_forget()
    frame.pack(fill="both", expand=True)

# ---------- Theme Switcher ----------
def apply_theme(theme_name):
    global current_theme
    current_theme = theme_name
    for frame in [welcome_frame, menu_frame, settings_frame, game_frame, two_player_frame]:
        frame.configure(bg=themes[theme_name])
    root.configure(bg=themes[theme_name])
    score_label.config(bg=themes[theme_name])
    two_player_score_label.config(bg=themes[theme_name])

# ---------- Welcome Frame ----------
tk.Label(welcome_frame, text="Welcome to Tic Tac Toe!", font=("Arial", 24, "bold"),
         bg=themes[current_theme], fg="#4b0082").pack(pady=50)
ttk.Button(welcome_frame, text="Start Game", command=lambda: show_frame(menu_frame)).pack()

# ---------- Menu Frame ----------
tk.Label(menu_frame, text="Choose Game Mode", font=("Arial", 20, "bold"),
         bg=themes[current_theme], fg="#4b0082").pack(pady=20)

def choose_difficulty():
    diff_win = tk.Toplevel(root)
    diff_win.title("Difficulty")
    diff_win.geometry("250x150")
    diff_win.grab_set()

    def select(diff):
        global difficulty
        difficulty = diff
        diff_win.destroy()
        start_game_vs_computer()

    tk.Label(diff_win, text="Select Difficulty", font=("Arial", 14)).pack(pady=10)
    ttk.Button(diff_win, text="Easy", command=lambda: select("easy")).pack(pady=5)
    ttk.Button(diff_win, text="Hard", command=lambda: select("hard")).pack(pady=5)

ttk.Button(menu_frame, text="Play with Me (Computer)", command=choose_difficulty).pack(pady=10)
ttk.Button(menu_frame, text="Play with a Friend", command=lambda: start_two_player_game()).pack(pady=10)
ttk.Button(menu_frame, text="Settings", command=lambda: show_frame(settings_frame)).pack(pady=10)

# ---------- Settings Frame ----------
tk.Label(settings_frame, text="Choose Theme", font=("Arial", 20, "bold"),
         bg=themes[current_theme], fg="#4b0082").pack(pady=20)
for name in themes:
    ttk.Button(settings_frame, text=name, command=lambda n=name: apply_theme(n)).pack(pady=5)
ttk.Button(settings_frame, text="Back to Menu", command=lambda: show_frame(menu_frame)).pack(pady=20)

# ---------- Game vs Computer ----------
board_buttons = [[None]*3 for _ in range(3)]
board_state = [[""]*3 for _ in range(3)]
player_score = computer_score = round_count = 0
MAX_ROUNDS = 10

def reset_board():
    for i in range(3):
        for j in range(3):
            board_state[i][j] = ""
            board_buttons[i][j].config(text="", state="normal")

def update_scoreboard():
    score_label.config(text=f"Score - You: {player_score} | Computer: {computer_score} | Round {round_count}/{MAX_ROUNDS}")

def check_winner(symbol):
    for i in range(3):
        if all(board_state[i][j] == symbol for j in range(3)) or all(board_state[j][i] == symbol for j in range(3)):
            return True
    return all(board_state[i][i] == symbol for i in range(3)) or all(board_state[i][2 - i] == symbol for i in range(3))

def is_draw():
    return all(cell for row in board_state for cell in row)

def show_final_results():
    result = f"Final Score:\nYou: {player_score} | Computer: {computer_score}\n"
    if player_score > computer_score:
        result += "\n\U0001F3C6 You won the series!"
    elif computer_score > player_score:
        result += "\n\U0001F4BB Computer won the series!"
    else:
        result += "\n\U0001F91D It's a tie!"
    messagebox.showinfo("Final Results", result)

def player_move(row, col):
    global player_score, round_count
    if board_state[row][col] == "":
        board_state[row][col] = "X"
        board_buttons[row][col].config(text="X", state="disabled")

        if check_winner("X"):
            player_score += 1
            round_count += 1
            update_scoreboard()
            messagebox.showinfo("Game Over", "You Win!")
            if round_count >= MAX_ROUNDS:
                show_final_results()
            else:
                reset_board()
            return
        elif is_draw():
            round_count += 1
            update_scoreboard()
            messagebox.showinfo("Game Over", "It's a Draw!")
            if round_count >= MAX_ROUNDS:
                show_final_results()
            else:
                reset_board()
            return

        root.after(500, computer_move)

def computer_move():
    global computer_score, round_count
    for symbol in ["O", "X"]:
        for i in range(3):
            for j in range(3):
                if board_state[i][j] == "":
                    board_state[i][j] = symbol
                    if check_winner(symbol):
                        board_state[i][j] = "O"
                        board_buttons[i][j].config(text="O", state="disabled")
                        if symbol == "O":
                            computer_score += 1
                            round_count += 1
                            update_scoreboard()
                            messagebox.showinfo("Game Over", "Computer Wins!")
                            if round_count >= MAX_ROUNDS:
                                show_final_results()
                            else:
                                reset_board()
                        return
                    board_state[i][j] = ""

    empty = [(i, j) for i in range(3) for j in range(3) if board_state[i][j] == ""]
    if not empty:
        return
    row, col = random.choice(empty)
    board_state[row][col] = "O"
    board_buttons[row][col].config(text="O", state="disabled")

    if check_winner("O"):
        computer_score += 1
        round_count += 1
        update_scoreboard()
        messagebox.showinfo("Game Over", "Computer Wins!")
        if round_count >= MAX_ROUNDS:
            show_final_results()
        else:
            reset_board()
    elif is_draw():
        round_count += 1
        update_scoreboard()
        messagebox.showinfo("Game Over", "It's a Draw!")
        if round_count >= MAX_ROUNDS:
            show_final_results()
        else:
            reset_board()

def start_game_vs_computer():
    global player_score, computer_score, round_count
    player_score = computer_score = round_count = 0
    reset_board()
    update_scoreboard()
    show_frame(game_frame)

def reset_and_back_to_menu():
    global player_score, computer_score, round_count
    player_score = computer_score = round_count = 0
    reset_board()
    update_scoreboard()
    show_frame(menu_frame)

score_label = tk.Label(game_frame, text="", font=("Arial", 14, "bold"), bg=themes[current_theme])
score_label.grid(row=0, column=0, columnspan=3, pady=10)

for i in range(3):
    game_frame.grid_rowconfigure(i+1, weight=1)
    game_frame.grid_columnconfigure(i, weight=1)
    for j in range(3):
        btn = tk.Button(game_frame, text="", font=("Arial", 24), width=5, height=2,
                        command=lambda r=i, c=j: player_move(r, c), bg="white")
        btn.grid(row=i+1, column=j, padx=5, pady=5)
        board_buttons[i][j] = btn

ttk.Button(game_frame, text="Back to Menu", command=reset_and_back_to_menu).grid(row=4, column=0, columnspan=3, pady=10)

# ---------- Two Player Game ----------
two_player_board = [[None]*3 for _ in range(3)]
two_player_state = [[""]*3 for _ in range(3)]
two_player_score = {"X": 0, "O": 0}
two_player_round = 0
player_names = {"X": "Player 1", "O": "Player 2"}
current_turn = "X"


def start_two_player_game():
    global two_player_score, two_player_round, current_turn, player_names
    player_names["X"] = simpledialog.askstring("Player Name", "Enter name for Player 1 (X):") or "Player 1"
    player_names["O"] = simpledialog.askstring("Player Name", "Enter name for Player 2 (O):") or "Player 2"
    two_player_score = {"X": 0, "O": 0}
    two_player_round = 0
    current_turn = "X"
    reset_two_player_board()
    update_two_player_scoreboard()
    show_frame(two_player_frame)


def reset_two_player_board():
    for i in range(3):
        for j in range(3):
            two_player_state[i][j] = ""
            two_player_board[i][j].config(text="", state="normal")


def update_two_player_scoreboard():
    two_player_score_label.config(text=f"{player_names['X']}: {two_player_score['X']} | {player_names['O']}: {two_player_score['O']} | Round {two_player_round}/{MAX_ROUNDS}")


def two_player_move(row, col):
    global current_turn, two_player_round
    if two_player_state[row][col] == "":
        two_player_state[row][col] = current_turn
        two_player_board[row][col].config(text=current_turn, state="disabled")

        if check_two_player_winner(current_turn):
            two_player_score[current_turn] += 1
            two_player_round += 1
            update_two_player_scoreboard()
            messagebox.showinfo("Game Over", f"{player_names[current_turn]} Wins!")
            if two_player_round >= MAX_ROUNDS:
                messagebox.showinfo("Final Results", f"Final Score:\n{player_names['X']}: {two_player_score['X']}\n{player_names['O']}: {two_player_score['O']}")
            else:
                reset_two_player_board()
            return
        elif all(cell for row in two_player_state for cell in row):
            two_player_round += 1
            update_two_player_scoreboard()
            messagebox.showinfo("Game Over", "It's a Draw!")
            if two_player_round >= MAX_ROUNDS:
                messagebox.showinfo("Final Results", f"Final Score:\n{player_names['X']}: {two_player_score['X']}\n{player_names['O']}: {two_player_score['O']}")
            else:
                reset_two_player_board()
            return

        current_turn = "O" if current_turn == "X" else "X"


def check_two_player_winner(symbol):
    for i in range(3):
        if all(two_player_state[i][j] == symbol for j in range(3)) or all(two_player_state[j][i] == symbol for j in range(3)):
            return True
    return all(two_player_state[i][i] == symbol for i in range(3)) or all(two_player_state[i][2 - i] == symbol for i in range(3))


two_player_score_label = tk.Label(two_player_frame, text="", font=("Arial", 14, "bold"), bg=themes["Pink"])
two_player_score_label.grid(row=0, column=0, columnspan=3, pady=10)

for i in range(3):
    two_player_frame.grid_rowconfigure(i+1, weight=1)
    two_player_frame.grid_columnconfigure(i, weight=1)
    for j in range(3):
        btn = tk.Button(two_player_frame, text="", font=("Arial", 24), width=5, height=2,
                        command=lambda r=i, c=j: two_player_move(r, c), bg="white")
        btn.grid(row=i+1, column=j, padx=5, pady=5)
        two_player_board[i][j] = btn

ttk.Button(two_player_frame, text="Back to Menu", command=lambda: show_frame(menu_frame)).grid(row=4, column=0, columnspan=3, pady=10)

# ---------- Start GUI ----------
show_frame(welcome_frame)
root.mainloop()
