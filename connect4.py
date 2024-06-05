import os
import curses

def print_board(stdscr, board, selected_column, winning_sequence):
    stdscr.clear()
    stdscr.addstr("Connect Four\n", curses.A_BOLD)
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if (i, j) == selected_column:
                stdscr.addstr(f"[{cell}]", curses.A_REVERSE)
            elif (i, j) in winning_sequence:
                stdscr.addstr(f" {cell} ", curses.color_pair(4))
            else:
                stdscr.addstr(f" {cell} ")
            if j < len(row) - 1:
                stdscr.addstr("|")
        stdscr.addstr("\n")
        if i < len(board) - 1:
            stdscr.addstr("-" * (len(row) * 4 - 1) + "\n")
    stdscr.addstr("\n")
    stdscr.addstr("Instructions:\n")
    stdscr.addstr(" - Use arrow keys to select column\n")
    stdscr.addstr(" - Press ENTER to drop disc\n")
    stdscr.addstr(" - Press Q to quit\n")
    stdscr.refresh()

def check_winner(board, player):
    # Check horizontally
    for row in range(len(board)):
        for i in range(len(board[0]) - 3):
            if all(board[row][j] == player for j in range(i, i+4)):
                return [(row, j) for j in range(i, i+4)]

    # Check vertically
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if all(board[row][col] == player for row in range(i, i+4)):
                return [(row, col) for row in range(i, i+4)]

    # Check diagonally (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return [(row + i, col + i) for i in range(4)]

    # Check diagonally (top-right to bottom-left)
    for row in range(len(board) - 3):
        for col in range(3, len(board[0])):
            if all(board[row + i][col - i] == player for i in range(4)):
                return [(row + i, col - i) for i in range(4)]

    return []

def drop_disc(board, column, player):
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = player
            return True
    return False

def round_robin_schedule(players):
    schedule = []
    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            schedule.append((players[i], players[j]))
    return schedule

def connect_four(stdscr):
    curses.curs_set(0)  # Hide the cursor
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    
    players = ['S', 'U', 'M', 'N']  # Using initials for simplicity
    player_names = {'S': 'Simra', 'U': 'Sumayya', 'M': 'Mariam', 'N': 'Mahnoor'}
    player_colors = {'S': curses.color_pair(1), 'U': curses.color_pair(2), 'M': curses.color_pair(3), 'N': curses.color_pair(4)}
    schedule = round_robin_schedule(players)
    scores = {player: 0 for player in players}

    for match in schedule:
        player1, player2 = match
        board = [[" " for _ in range(7)] for _ in range(6)]
        selected_column = (0, 0)
        winning_sequence = []
        current_player = player1

        while True:
            print_board(stdscr, board, selected_column, winning_sequence)
            stdscr.addstr(f"{player_names[current_player]}'s turn\n", player_colors[current_player])
            stdscr.refresh()
            key = stdscr.getch()

            if key == ord('q') or key == ord('Q'):
                return
            elif key == curses.KEY_LEFT:
                selected_column = (selected_column[0], max(selected_column[1] - 1, 0))
            elif key == curses.KEY_RIGHT:
                selected_column = (selected_column[0], min(selected_column[1] + 1, 6))
            elif key == curses.KEY_ENTER or key == 10 or key == 13:
                column = selected_column[1]
                if drop_disc(board, column, current_player):
                    winning_sequence = check_winner(board, current_player)
                    if winning_sequence:
                        print_board(stdscr, board, selected_column, winning_sequence)
                        stdscr.addstr(f"Player {player_names[current_player]} wins!\n", player_colors[current_player])
                        stdscr.refresh()
                        stdscr.getch()
                        scores[current_player] += 1
                        break
                    elif all(board[row][column] != " " for row in range(len(board))):
                        print_board(stdscr, board, selected_column, [])
                        stdscr.addstr("It's a draw!\n")
                        stdscr.refresh()
                        stdscr.getch()
                        break
                    current_player = player2 if current_player == player1 else player1
                else:
                    stdscr.addstr("Column is full. Try again.\n")
                    stdscr.refresh()

    stdscr.clear()
    stdscr.addstr("Tournament Results:\n", curses.A_BOLD)
    for player, score in scores.items():
        stdscr.addstr(f"{player_names[player]}: {score} wins\n")
    stdscr.addstr("\nPress any key to exit.")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(connect_four)
