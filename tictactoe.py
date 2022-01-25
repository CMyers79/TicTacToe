class TicTacToe:
    """Implements a game of Tic Tac Toe with an automatic second player that does not lose the game.
    """
    def __init__(self):
        """Initalizes a TicTacToe object with an empty board, draw and turn flags"""
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.turn = False
        self.draw = False

    def is_draw(self):
        """Returns bool for self.draw"""
        return self.draw

    def move(self):
        """Calls playerMove() if self.turn is False, else calls AIMove()"""
        if not self.turn:
            self.player_move()
        else:
            self.AI_move()

    def is_won(self):
        """Returns True if the AI has won the game, False if the game has not been won"""
        for r in range(3):  # check horizontal win
            if self.board[r].count("X") == 3:
                return  # these are unreachable because the player can't win
            elif self.board[r].count("O") == 3:
                return True

        for c in range(3):  # check vertical win
            column = self.board[0][c] + self.board[1][c] + self.board[2][c]
            if column.count("X") == 3:
                return
            elif column.count("O") == 3:
                return True

        for d in range(-1, 2, 2):  # check diagonal win
            diag = self.board[1 + d][0] + self.board[1][1] + self.board[1 - d][2]
            if diag.count("X") == 3:
                return
            elif diag.count("O") == 3:
                return True

        return False

    def player_move(self):
        """Prompts for y and x coordinates of player move, stores the move if valid, else prints error and restarts"""
        move = [input("enter y-coord"), input("enter x-coord")]
        if move[0] in "012" and move[1] in "012" and self.board[int(move[0])][int(move[1])] == " ":
            self.board[int(move[0])][int(move[1])] = "X"
            self.turn = 1
            return
        else:
            print("invalid move, try again")
            self.player_move()

    def AI_move(self):
        """Updates the board with a move so that the player will not win, or reports a draw when the board is full.
        The AI priority is first to win, second to prevent a loss, and third to prevent a fork by the player.  Forks
        are prevented by forcing the player to block an AI win with a move that does not create a fork."""

        total_moves = 9 - self.board[0].count(" ") - self.board[1].count(" ") - self.board[2].count(" ")
        if total_moves == 9:
            self.draw = 1
            return
        # first move is scripted to occupy the center
        if total_moves == 1 and self.board[1][1] == "X":  # if player has first taken the center, mark upper left
            self.board[0][0] = "O"
            self.turn = 0
            return
        elif total_moves == 1:  # otherwise, take the center
            self.board[1][1] = "O"
            self.turn = 0
            return

        if self.AI_win():
            return

        if self.AI_block():
            return

        self.AI_prevent_fork()

    def AI_win(self):
        """If there is a winning move, make that move, return Bool"""
        for r in range(3):  # horizontal win
            if self.board[r].count("O") == 2 and self.board[r].count(" ") == 1:
                self.board[r][self.board[r].index(" ")] = "O"
                self.turn = 0
                return True

        for c in range(3):  # vertical win
            column = self.board[0][c] + self.board[1][c] + self.board[2][c]
            if column.count("O") == 2 and column.count(" ") == 1:
                self.board[column.index(" ")][c] = "O"
                self.turn = 0
                return True

        for d in range(-1, 2, 2):  # diagonal win - d is used to get the row indices for each diagonal
            diag = self.board[1 + d][0] + self.board[1][1] + self.board[1 - d][2]
            if diag.count("O") == 2 and diag.count(" ") == 1:
                self.board[-d * (diag.index(" ") - 1) + 1][diag.index(" ")] = "O"
                self.turn = 0
                return True
        return False

    def AI_block(self):
        """If the player can win on their next turn, block the win and return 1, else return 0"""
        for r in range(3):  # block horizontal win
            if self.board[r].count("X") == 2 and self.board[r].count(" ") == 1:
                self.board[r][self.board[r].index(" ")] = "O"
                self.turn = 0
                return True

        for c in range(3):  # block vertical win
            column = self.board[0][c] + self.board[1][c] + self.board[2][c]
            if column.count("X") == 2 and column.count(" ") == 1:
                self.board[column.index(" ")][c] = "O"
                self.turn = 0
                return True

        for d in range(-1, 2, 2):  # block diagonal win
            diag = self.board[1 + d][0] + self.board[1][1] + self.board[1 - d][2]
            if diag.count("X") == 2 and diag.count(" ") == 1:
                self.board[-d * (diag.index(" ") - 1) + 1][diag.index(" ")] = "O"
                self.turn = 0
                return True
        return False

    def AI_prevent_fork(self):
        """Check the board for spaces where two player win conditions can be created with their next move.  If one
        or more are present, make a move that creates an AI win condition that must be blocked by a move that does not
        create a player fork."""
        possible_moves = {}
        for r in range(3):  # initialize dict of empty spaces to count fork halves
            for c in range(3):
                if self.board[r][c] == " ":
                    possible_moves[r, c] = 0

        for r in range(3):  # count horizontal fork halves
            if self.board[r].count("X") == 1 and self.board[r].count(" ") == 2:
                for c in range(3):
                    if (r, c) in possible_moves:
                        possible_moves[r, c] += 1

        for c in range(3):  # count vertical fork halves
            column = self.board[0][c] + self.board[1][c] + self.board[2][c]
            if column.count("X") == 1 and column.count(" ") == 2:
                for r in range(3):
                    if (r, c) in possible_moves:
                        possible_moves[r, c] += 1

        for d in range(-1, 2, 2):  # count diagonal fork halves
            diag = self.board[1 + d][0] + self.board[1][1] + self.board[1 - d][2]
            if diag.count("X") == 1 and diag.count(" ") == 2:
                for space in [(1 + d, 0), (1, 1), (1 - d, 2)]:
                    if space in possible_moves:
                        possible_moves[space] += 1

        player_forks = [key for key, value in possible_moves.items() if value == max(possible_moves.values())]
        targets = [move for move in possible_moves if move not in player_forks]

        for r in range(3):  # look for horizontal attack
            if self.board[r].count("O") == 1 and self.board[r].count(" ") == 2:
                for c in range(3):
                    if (r, c) in possible_moves and [(r, x) for x in range(3) if x != c and self.board[r][x] == " "][0] in targets:
                        self.board[r][c] = "O"
                        self.turn = 0
                        return

        for c in range(3):  # look for vertical attack
            column = self.board[0][c] + self.board[1][c] + self.board[2][c]
            if column.count("O") == 1 and column.count(" ") == 2:
                for r in range(3):
                    if (r, c) in possible_moves and [(x, c) for x in range(3) if x != r and self.board[x][c] == " "][0] in targets:
                        self.board[r][c] = "O"
                        self.turn = 0
                        return

        for d in range(-1, 2, 2):  # look for diagonal attack
            diag = self.board[1 + d][0] + self.board[1][1] + self.board[1 - d][2]
            if diag.count("O") == 1 and diag.count(" ") == 2:
                for space in [(1 + d, 0), (1 - d, 2)]:  # the center is always occupied when this runs
                    if space in possible_moves and [coord for coord in [(1 + d, 0), (1 - d, 2)] if coord != space][0] in targets:
                        self.board[space[0]][space[1]] = "O"
                        self.turn = 0
                        return

        # if there are no possible forks or attacks, make the first move in the dict
        move = [space for space in possible_moves][0]
        self.board[move[0]][move[1]] = "O"
        self.turn = 0
        return


game = TicTacToe()
while not (game.is_won() or game.is_draw()):  # only check for AI win because it can't be defeated
    game.move()
    print(game.board[0])
    print(game.board[1])
    print(game.board[2])

if not game.is_draw():
    print("The AI won")
else:
    print("The game has ended in a draw")
