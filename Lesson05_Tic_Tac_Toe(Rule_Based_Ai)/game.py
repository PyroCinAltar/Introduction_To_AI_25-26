# Tic-Tac-Toe (Console) — Human (X) vs Rule-Based AI (O)
# Rules the AI follows (in order): win -> block -> center -> corners -> sides

# Arrays
WIN_LINES = [
    (0,1,2),(3,4,5),(6,7,8),      # rows
    (0,3,6),(1,4,7),(2,5,8),      # cols
    (0,4,8),(2,4,6)               # diagonals
]


def print_board(b):
    """Show the board; empty cells display their position number (1-9)."""
    def sym(i): return b[i] if b[i] != ' ' else str(i+1)
    rows = [
        f" {sym(0)} | {sym(1)} | {sym(2)} ",
        "-----------",
        f" {sym(3)} | {sym(4)} | {sym(5)} ",
        "-----------",
        f" {sym(6)} | {sym(7)} | {sym(8)} "
    ]
    print("\n".join(rows))

def winner(b):
    """Return 'X' or 'O' if someone won, 'Draw' if full, else None."""
    for a, c, d in WIN_LINES:
        if b[a] != ' ' and b[a] == b[c] == b[d]:
            return b[a]
    return 'Draw' if ' ' not in b else None

def winning_move(b, mark):
    """If 'mark' can win in one move, return the index; else None."""
    for i in range(9):
        if b[i] == ' ':
            t = b.copy()
            t[i] = mark
            if winner(t) == mark:
                return i
    return None

def ai_move(b, ai='O', human='X'):
    """Rule-based move chooser for the AI."""
    # 1) Win if possible
    m = winning_move(b, ai)
    if m is not None: return m
    # 2) Block opponent winning move
    m = winning_move(b, human)
    if m is not None: return m
    
    
    # 3 could be overridden or happen after the check for entire board state.
    
    # 3) Prefer center, then corners, then sides
    if b[4] == ' ': return 4
    for i in (0, 2, 6, 8):
        if b[i] == ' ': return i
    for i in (1, 3, 5, 7):
        if b[i] == ' ': return i
        
        
        
    # Fallback (shouldn't happen)
    return next(i for i,v in enumerate(b) if v == ' ')

def human_move(b):
    """Prompt human for a legal move 1-9; return index 0-8."""
    while True:
        try:
            s = input("Your move (1-9): ").strip()
            idx = int(s) - 1
            if idx not in range(9):
                print("Enter a number 1-9 that matches an empty cell.")
                continue
            if b[idx] != ' ':
                print("That cell is taken. Choose another.")
                continue
            return idx
        except ValueError:
            print("Please enter a number (1-9).")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            raise SystemExit

def play_one():
    """Play one game; returns 'X', 'O', or 'Draw'."""
    board = [' '] * 9
    turn = 'X'  # Human starts
    while True:
        print_board(board)
        w = winner(board)
        if w:
            print()
            print_board(board)
            return w
        if turn == 'X':
            idx = human_move(board)
            board[idx] = 'X'
        else:
            idx = ai_move(board, ai='O', human='X')
            board[idx] = 'O'
            print(f"AI plays at {idx+1}")
        turn = 'O' if turn == 'X' else 'X'

def main():
    print("Tic-Tac-Toe — You (X) vs AI (O)\n")
    while True:
        result = play_one()
        if result == 'Draw':
            print("\nResult: It's a draw.")
        else:
            print(f"\nResult: {result} wins!")
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != 'y' or again != "yes":
            print("Thanks for playing!")
            break
        print()

if __name__ == "__main__":
    main()
    
# Major issues: AI goes straight for the first possible prefered move instead of checking the entire board state
# Difficulty levels would be useful
