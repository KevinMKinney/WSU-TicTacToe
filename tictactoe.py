"""TicTacToe. A module for playing a simple game.

Kevin Kinney

"""
import sys

def int_input(state, mover):
    """A move function that asks for input from stdin..."""

    print("%s's turn...(0..%d)" % (TicTacToe.Chrs[mover], len(state)-1))
    return int(input())


class TicTacToe():
    """A Class representing the game of TicTacToe.

    Each instance maintains the size of the board and it's current state.
    The instance also tracks whos turn it is.

    the move() method is used to manipulate the board state in a safe (legal)
    manner

    the show() method is used to display the board state in a human readable
    form

    the play() method is used to play a game with 'desired' moves supplied by
    an external function.
    """
    Column = 0
    Row = 1
    DiagonalRight = 2
    DiagonalLeft = 3
    StaleMate = 4
    Chrs = {0: ' ', 1: 'X', 2: 'O'}

    def __init__(self, n=3):
        """Create a n-by-n tic-tac-toe game. n=3 by default,
           but for full credit you should support arbitrary n>=2.

           If you need to use additional instance variables, you
           should initialize them here, and be sure to reinitialize
           them (if necessary) in reset()
        """

        self.n = n
        self.n2 = n**2
        self.reset()

    def reset(self, state=None):
        """Reset the game to the specified state, or to an empty board.
        A state is internally encoded as a list of elements in {0, 1, 2}.
        0 represents an empty space, 1 represents an 'X' (player 1), and 2
        represents an 'O' (player 2). The state is assumed to have an
        appropriate number of 'X's relative to the number of 'O's.

        The internal state has indicies 0...(n^2-1) which correspond to cells
        from the upper left corner (0) to the bottom right (n^2-1) running
        left-right and top-down
        """

        if state:
            n_x = sum([1 for i in state if i == 1])
            n_oh = sum([1 for i in state if i == 2])
            # ones (x's) go first

            assert n_x == n_oh or n_x == n_oh+1, "X's (1's) go first."
            assert len(state) == self.n2, "the specified state is not the correct length"
            # The game state is kept here as a list of values.
            # 0  indicates the space is unoccupied;
            # 1  indicates the space is occupied by Player 1 (X)
            # 2  indicates the space is occupied by Player 2 (O)
            self.board = list(state)
            self.turn = (n_x -  n_oh) + 1  # X's turn if moves are equal

        else:
            self.board = [0]*(self.n2)
            self.turn = 1

    def move(self, where):
        """_ Part 1: Implement This Method _

        Perform the current player's move at the specified location/index and
        change turns to the next player; where is an index into the board in
        the range 0..(n**2-1)

        If the specified index is a valid move, modify the board,
        change turns and return True.

        Return False if the specified index is unopen, or does not exist.

        Don't forget that for full credit, you need to deal with an
        arbitrary nxn size board, not simply 3x3.
        """

        # check if board location is a valid move
        if (self.board[where] != 0):
            return False

        # place X or O in location
        self.board[where] = 2 - self.turn % 2
        # update turn
        self.turn += 1
        return True

    def show(self):
        """_ Part 2: Implement This Method _

        Display the board on stdout (e.g., using print())

        Simply write a method that displays the board in a logical and
        human-readable manner."""

        # there's probably a better way to specify to not add a newline after every print
        for i in range(self.n2):
            print(" %c " %TicTacToe.Chrs[self.board[i]], end="")

            if (i % self.n == self.n - 1):
                print("\n", end="")
                if (i != self.n2 - 1):
                    for j in range(self.n):
                        print("----", end="")
                    print("\n", end="")
            else:
                print("|", end="")

    def is_win(self):
        """_ Part 3: Implement This Method _

        Determine if the current board configuration is an end game.
        For a board of size n, a win requires one player to have n tokens
        in a line (vertical, horizontal or diagonal).

        For full credit, comment your code to indicate what each code block
        is trying to do.

        Returns:

         (TicTacToe.Column, ?, player): if player wins in column c
         (TicTacToe.Row, ?, player): if player wins in row r
         (TicTacToe.DiagonalRight, ?, player): if player wins via
           a diagonal starting in the upper-left corner and proceeding
           down and to the right
         (TicTacToe.DiagonalLeft, ?, player): if player wins via a
           diagonal in the starting in the upper-right corner and proceeding
           down and to the left
         (TicTacToe.StaleMate, 0, 0): if the game is a stalemate
         False: if the end state is not yet determined

         ? in the tuples above indicates the lowest value cell index
         involved in the win. Cell indices range from 0...(n^2-1) and
         go from the top left of the board to the bottom right.
        """
        # there's probably a way to avoid this boolean with a keyword
        win = True

        # check for column win
        for col in range(self.n):
            firstVal = self.board[col]
            if (firstVal == 0):
                continue
            for row in range(1, self.n):
                if (firstVal != self.board[col + row * self.n]):
                    win = False
                    break
            if (win):
                return (TicTacToe.Column, col, firstVal)
            win = True

        # check for row win
        for row in range(self.n):
            firstVal = self.board[row * self.n]
            if (firstVal == 0):
                continue
            for col in range(1, self.n):
                if (firstVal != self.board[col + row * self.n]):
                    win = False
                    break
            if (win):
                return (TicTacToe.Row, row * self.n, firstVal)
            win = True

        # check for diagonal right win
        firstVal = self.board[0]
        if (firstVal != 0):
            for i in range(1, self.n):
                if (firstVal != self.board[self.n * i + i]):
                    win = False
                    break
            if (win):
                return (TicTacToe.DiagonalRight, 0, firstVal)
        win = True

        # check for diagonal left win
        firstVal = self.board[self.n - 1]
        if (firstVal != 0):
            for i in range(1, self.n):
                if (firstVal != self.board[(self.n - 1) * (i + 1)]):
                    win = False
                    break
            if (win):
                return (TicTacToe.DiagonalLeft, self.n - 1, firstVal)

        # check for any open spot/move
        for i in range(self.n2):
            if (self.board[i] == 0):
                return False

        return (TicTacToe.StaleMate, 0, 0)

    def describe_win(self, win):
        """Provides a text representation of an end-game state.

        win is a tuple:
         (reason code, cell location, player)
        """


        reason = {TicTacToe.Row: "Row", TicTacToe.Column: "Column",
                  TicTacToe.DiagonalLeft: "Diagonal Down and Left",
                  TicTacToe.DiagonalRight: "Diagonal Down and Right"}

        if win[0] == TicTacToe.StaleMate:
            return "StaleMate!"
        if win[0] == TicTacToe.DiagonalLeft:
            if win[1] == 0:
                where = "Upper Left"
            else:
                where = "Upper Right"
        else:
            where = "%d" % win[1]
        return "'%s' (%d) wins @ %s from cell %s" %(TicTacToe.Chrs[win[2]],
                                                    win[2], reason[win[0]],
                                                    win[1])

    def play(self, movefn=int_input, display=True, showwin=True):
        """_ Part 4: Implement This Method _

        Play the game of tictactoe!

        Arguments:
        movefn - a function that will provide possibly valid moves.
        display - show the game? (default: True)
        showwin - if True, explicitly indicate the game is over
                  and describe the win

        Play should work (roughly) as follows:
         - verify the game is not in an end state
         - display the game state (using show()) if the display flag is set
         - acquire the next 'intended' move from the movefn (see note below).
         - call the move method with 'intended' move
         - repeat steps above

         when an end state is reached:
         - print the state (if display flag is set) and
         - print 'Game Over!' along with a description of the win
           if showwin is True.

        the movefn should take two arguments:
          (1) the game state; and (2) the current player; because the internal
          state (self.board) is a list, you should pass a tuple to the movefn
          instead of directly passing self.board.  This ensures that the movefn
          can't actually manipulate the state of the board, it can only request
          that a move takes place -- it's up to the logic of the move() method to
          actually manipulate the game state/board.
        """

        # main game loop
        while(True):
            win = self.is_win()
            if (win != False):
                # board is at an end state
                if (display):
                    self.show()
                print("Game Over!")
                if (showwin):
                    print(self.describe_win(win))
                return
            else:
                # board is not in a end state
                if (display):
                    self.show()
                self.move(movefn(self.get_state(), 2 - self.turn % 2))

    def get_state(self):
        """Get the state of the board as an immutable tuple"""
        return tuple(self.board)


def mc(state, trials, n, debug=False):
    """_ Part 5 (Optional) : Implement This Method _

    Arguments:

     state   -- the initial state in which to start the game
     trials  -- the number of trials to run (games to play)
     n       -- the size of the board to make (n=3 in normal TicTacToe)
     debug   -- flag to enable more verbose printing


    Run a monte-carlo experiment in which we play the game using random
    moves. Here's how it should work:
      - create a function to generate with random moves (one that
         can be passed to the TicTacToe.play() method)
      - create a TicTacToe instance of board size n
      - loop for the number of trials and:
         - initialize the TicTacToe instance to the specified state
         - play the tictactoe game
         - track the outcome
      - return the distribution of outcomes as a tuple (see below).

    Monte-carlo experiments such as this are used to evaluate states in complex
    games such as chess and go.

    Return a 4-tuple of:
    (games played, % won by player-1, % won by player-2, % stalemates)


    """
    
    indexTuple = range(n*n)

    # closure for determining the random moves
    def randMove(game):
        # uses map() & filter() to get the indexes of valid moves to make
        # ex: map: 210100020 => {-1, -1, 2, -1, 4, 5, 6, -1, 8} => filter: {2, 4, 5, 6, 8}
        validLoc = list(filter(lambda x: x != -1 ,map(lambda x, y: y if (x == 0) else -1, t.get_state(), indexTuple)))

        if (debug):
            print("Valid moves: ", validLoc)

        # check if there are no valid locations (random.choice() does not work on empty sequence)
        if (not validLoc):
            return 0
        # get a raandom item from list (index of valid move)
        return random.choice(validLoc)

    t = TicTacToe(n)
    t.reset(state)

    if (debug):
        t.show()

    # check if board is already in a winning state
    win = t.is_win()
    if (win != False):
        if (win[2] == 0):
            return (1, 0, 0, 1)
        elif (win[2] == 1):
            return (1, 1, 0, 0)
        elif (win[2] == 2):
            return (1, 0, 1, 0)

    outcomes = [0, 0, 0, 0]

    for i in range(trials):
        # reset board state
        t.reset(state)
        outcomes[0] += 1

        if (debug):
            print("----Game %d!----" %outcomes[0])

        # play the game using random moves
        while (win == False):
            t.move(randMove(t)) # could probably pass in randMove() to t.play()
            if (debug):
                t.show()
            win = t.is_win()

        # game is finished, update outcomes
        if (win[2] == 0):
            outcomes[3] += 1
        elif (win[2] == 1):
            outcomes[1] += 1
        elif (win[2] == 2):
            outcomes[2] += 1
        win = False

        if (debug):
            print("Outcome update: ", outcomes)

    # dividing by trials here gets a more accurate number
    outcomes[1] = outcomes[1]/trials
    outcomes[2] = outcomes[2]/trials
    outcomes[3] = outcomes[3]/trials
    return tuple(outcomes)

if __name__ == "__main__":
    import argparse
    import random
    parser = argparse.ArgumentParser()
    parser.add_argument("--play", action='store_true')
    parser.add_argument("--state",
                        help="initial state comprised of values in {0,1,2}")
    parser.add_argument("--mc", type=int, default=1000,
                        help="monte carlo trials; default=%{default}")
    parser.add_argument("-n", type=int, default=3,
                        help="board length,width; default=%{default}")
    args = parser.parse_args()

    if args.state:
        # At the command line state will come in as a string drawn
        # from {0,1,2}.
        assert len(args.state) == args.n**2, \
            "Expected string with %d elements" % (args.n**2)

        state = [int(z) for z in args.state]
        stateset = set(state)
        assert stateset.issubset(set([0, 1, 2])), \
            "Expected string with elements 0,1,2"
        state = tuple(state)
        print("State is:", state)
    else:
        state = tuple([0]*(args.n**2))

    if args.play:
        t = TicTacToe(args.n)
        t.reset(state)
        t.play(display=True)

    elif args.mc:
        (games, one, two, stale) = mc(state, args.mc, args.n)
        print("%d trials: 1 wins %.2f, "
              "-1 wins %.2f, stalemates %.2f" % (games, one, two, stale))
