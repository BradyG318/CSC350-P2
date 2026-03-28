import random
import copy
 
 
class ConnectFourPlayer:
    def get_move(self):
        # Must return a value between 0 and 6 (inclusive), where 0 is the left-most column and 6 is the right-most column.
        raise NotImplementedError('Must be implemented by subclass')
 
    def is_automated(self):
        # AI players should return True, human players should return False
        return True
 
 
class ConnectFourHumanPlayer(ConnectFourPlayer):
    def __init__(self, model):
        self.model = model
 
    def is_automated(self):
        return False
 
    def get_move(self):
        valid_input = False
        valid_columns = self.model.get_valid_moves()
 
        while not valid_input:
            try:
                column = int(input('Enter column (1-7): '))
                if column < 1 or column > 7:
                    raise ValueError()
                else:
                    valid_input = True
 
                if valid_columns[column-1]:
                    return column-1
                else:
                    print('That column is full. Pick again.')
                    valid_input = False
            except ValueError:
                print('Invalid input.')
 
        # Should not get here
        return -1
 
 
class ConnectFourRandomPlayer(ConnectFourPlayer):
    def __init__(self, model):
        self.model = model
 
    def get_move(self):
        moves = self.model.get_valid_moves()
        m = random.randrange(7)
        while not moves[m]:
            m = random.randrange(7)
        return m
 
 
# Constants matching c4model
PLAYER1 = 1
PLAYER2 = 2
EMPTY = -1
NUMROWS = 6
NUMCOLS = 7
 
 
class ConnectFourAIPlayer(ConnectFourPlayer):
    """
    Question 1: AI Player Class
    Subclass of ConnectFourPlayer that uses Minimax with Alpha-Beta Pruning.
    """
 
    def __init__(self, model, max_depth = 4):
        self.model = model
        #Added for Q5
        self.max_depth = max_depth
 
    def is_automated(self):
        return True
 
    def get_move(self):
        """
        Question 1 (basic move for now):
        Returns a legal move (integer 0-6). Currently picks the valid column
        closest to the center for a slight strategic advantage.
        This will be replaced with alpha_beta_search by a teammate for Q5.
        """
        #state = self.model.get_grid()
        #Question 5 Alpha-Beta replacement:
        state = copy.deepcopy(self.model.get_grid())

        valid = self.actions(state)
 
        # Pick the valid column closest to center (column 3)
        best_col = valid[0]
        best_dist = abs(valid[0] - 3)
        for col in valid:
            dist = abs(col - 3)
            if dist < best_dist:
                best_dist = dist
                best_col = col
 
        #return best_col
        #Question 5 Alpha-Beta replacement:
        return self.alpha_beta_search(state)
 
    # ------------------------------------------------------------------
    # Question 2: Terminal Test
    # ------------------------------------------------------------------
    def terminal_test(self, state):
        """
        Takes a board state (2D list indexed as state[col][row]) and returns
        True if the game is over — either a player has won or the board is full.
        """
        # Check for a winner
        if self._get_winner(state) > 0:
            return True
 
        # Check for draw (board full)
        return self._is_draw(state)
 
    # ------------------------------------------------------------------
    # Question 3: Actions
    # ------------------------------------------------------------------
    def actions(self, state):
        """
        Takes a board state and returns a list of valid column numbers (0-6).
        A column is valid if its top row (row 0) is EMPTY.
        """
        moves = []
        for col in range(NUMCOLS):
            if state[col][0] == EMPTY:
                moves.append(col)
        return moves
 
    # ------------------------------------------------------------------
    # Question 4: Result
    # ------------------------------------------------------------------
    def result(self, state, action):
        """
        Takes a board state and an action (column 0-6). Returns a new board
        state with the appropriate player's piece dropped into that column.
        Uses deep copy so the original state is not modified.
        """
        newstate = copy.deepcopy(state)
        turn = self._get_turn(state)
 
        # Find the lowest empty row in the chosen column (highest index)
        row = NUMROWS - 1
        while row >= 0 and newstate[action][row] != EMPTY:
            row -= 1
 
        newstate[action][row] = turn
        return newstate
 
    # ------------------------------------------------------------------
    # Helper functions
    # ------------------------------------------------------------------
    def _get_turn(self, state):
        """
        Deduces whose turn it is by counting filled cells.
        Player 1 always goes first, so if the number of filled cells is even,
        it's Player 1's turn; if odd, it's Player 2's turn.
        """
        filled = 0
        for col in range(NUMCOLS):
            for row in range(NUMROWS):
                if state[col][row] != EMPTY:
                    filled += 1
 
        if filled % 2 == 0:
            return PLAYER1
        else:
            return PLAYER2
 
    def _is_draw(self, state):
        """Returns True if every cell on the board is filled."""
        for col in range(NUMCOLS):
            for row in range(NUMROWS):
                if state[col][row] == EMPTY:
                    return False
        return True
 
    def _get_winner(self, state):
        """
        Returns PLAYER1 or PLAYER2 if that player has four in a row,
        or -1 if there is no winner.
        Checks horizontal, vertical, and both diagonal directions.
        """
        # Horizontal check (4 consecutive columns in the same row)
        for row in range(NUMROWS):
            for col in range(NUMCOLS - 3):
                if state[col][row] != EMPTY:
                    if (state[col][row] == state[col + 1][row] and
                            state[col][row] == state[col + 2][row] and
                            state[col][row] == state[col + 3][row]):
                        return state[col][row]
 
        # Vertical check (4 consecutive rows in the same column)
        for col in range(NUMCOLS):
            for row in range(NUMROWS - 3):
                if state[col][row] != EMPTY:
                    if (state[col][row] == state[col][row + 1] and
                            state[col][row] == state[col][row + 2] and
                            state[col][row] == state[col][row + 3]):
                        return state[col][row]
 
        # Negative diagonal (\) check
        for col in range(NUMCOLS - 3):
            for row in range(NUMROWS - 3):
                if state[col][row] != EMPTY:
                    if (state[col][row] == state[col + 1][row + 1] and
                            state[col][row] == state[col + 2][row + 2] and
                            state[col][row] == state[col + 3][row + 3]):
                        return state[col][row]
 
        # Positive diagonal (/) check
        for col in range(3, NUMCOLS):
            for row in range(NUMROWS - 3):
                if state[col][row] != EMPTY:
                    if (state[col][row] == state[col - 1][row + 1] and
                            state[col][row] == state[col - 2][row + 2] and
                            state[col][row] == state[col - 3][row + 3]):
                        return state[col][row]
 
        return -1
 
    def utility(self, state, my_player):
        """
        Returns the utility of a terminal state.
        +1000 if this player wins, -1000 if the opponent wins, 0 for a draw.
        Uses the model's turn to determine which player this agent is.
        """
        winner = self._get_winner(state)
        #Commented for Q6:
        #my_player = self.model.get_turn()
        opponent = PLAYER1 if my_player == PLAYER2 else PLAYER2
 
        if winner == my_player:
            return 1000
        elif winner == opponent:
            return -1000
        elif (self._is_draw(state)): #Draw
            return 0
        
        score = 0

        #Heuristic function, based on controlling center of board
        centerCol = 3
        for r in range(NUMROWS):
            if (state[centerCol[r] == my_player]):
                score += 3
            elif (state[centerCol][row] == opponent):
                score -= 3
        
        #Check every possible 4 piece combination
        ##Horizontally
        for r in range(NUMROWS):
            for c in range(CUMCOLS-3):
                window = [state[c+i][r] for i in range(4)]
                score += self._score_window(window, my_player, opponent)
        ##Vertically
        for c in range(NUMCOLS):
            for r in range(NUMROWS-3):
                window = [state[c][r+i] for i in range(4)]
                score += self._score_window(window, my_player, opponent)
        ##Down & Right Diagonal
        for c in range(3, NUMCOLS):
            for r in range(NUMROWS-3):
                window = [state[c+i][r+i] for i in range(4)]
                score += self._score_window(window, my_player, opponent)
        ##Up & Right Diagonal
        for c in range(3, NUMCOLS):
            for r in range(NUMROWS-3):
                window = [state[c-i][r+i] for i in range(4)]
                score += self._score_window(window, my_player, opponent)
        return score
                


    def _score_window(self, window, my_player, opponent):
        myCount = window.count(my_player)
        oppCount = window.count(opponent)
        emptyCount = window.count(EMPTY)

        # Block mixed windows
        if myCount > 0 and oppCount > 0:
            return 0

        # Favor my threats
        if myCount == 4:
            return 1000
        if myCount == 3 and emptyCount == 1:
            return 50
        if myCount == 2 and emptyCount == 2:
            return 10
        if myCount == 1 and emptyCount == 3:
            return 1

        # Penalize opponent threats
        if oppCount == 4:
            return -1000
        if oppCount == 3 and emptyCount == 1:
            return -80
        if oppCount == 2 and emptyCount == 2:
            return -12
        if oppCount == 1 and emptyCount == 3:
            return -1

        return 0
        

