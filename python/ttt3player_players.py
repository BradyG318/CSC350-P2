import copy


class TTT3PlayerHumanPlayer:
    def __init__(self, model, symbol):
        self.model = model
        self.symbol = symbol

    def is_automated(self):
        return False

    def get_move(self):
        #Commented out for Question 8:
        # valid_input = False
        # valid_moves = self.model.get_valid_moves()

        # while not valid_input:
        #     try:
        #         move = int(input('Enter move (1-16): '))
        #         if move < 1 or move > 16:
        #             raise ValueError()
        #         else:
        #             valid_input = True

        #         if move in valid_moves:
        #             return move
        #         else:
        #             print('That spot is full. Pick again.')
        #             valid_input = False
        #     except ValueError:
        #         print('Invalid input.')

        # # Should not get here
        # return -1

        #Question 8:
        state = copy.deepcopy(self.model.get_grid())
        bestMove = None
        bestVector = None
        myIndex = self.playerIndex(self.symbol)

        for action in self.actions(state):
            nextState = self.result(state, action)
            valueVector = self.maxN(nextState, depth=1)

            if bestVector is None or valueVector[myIndex] > bestVector[myIndex]:
                bestVector = valueVector
                bestMove = action

        return bestMove
    def maxN(self, state, depth, maxDepth=5):
        if self.terminal_test(state) or depth >= maxDepth:
            return self.utilityVector(state)

        turn = self._get_turn(state)
        turnIndex = self.playerIndex(turn)
        bestVector = None

        for action in self.actions(state):
            childState = self.result(state, action)
            valueVector = self.maxN(childState, depth + 1, maxDepth)

            if bestVector is None or valueVector[turnIndex] > bestVector[turnIndex]:
                bestVector = valueVector

        return bestVector

    def utilityVector(self, state):
        winner = self._get_winner(state)

        if winner == 'X':
            return [1000, -1000, -1000]
        elif winner == 'O':
            return [-1000, 1000, -1000]
        elif winner == '+':
            return [-1000, -1000, 1000]
        elif self._is_draw(state):
            return [0, 0, 0]

        return self.evaluateNonTerminal(state)

    def evaluateNonTerminal(self, state):
        scores = {'X': 0, 'O': 0, '+': 0}
        lines = []

        # Horizontal 3-cell lines
        for row in range(4):
            for startCol in range(2):
                lines.append([
                    state[row][startCol],
                    state[row][startCol + 1],
                    state[row][startCol + 2]
                ])

        # Vertical 3-cell lines
        for col in range(4):
            for startRow in range(2):
                lines.append([
                    state[startRow][col],
                    state[startRow + 1][col],
                    state[startRow + 2][col]
                ])

        # Diagonal \ lines
        for startRow in range(2):
            for startCol in range(2):
                lines.append([
                    state[startRow][startCol],
                    state[startRow + 1][startCol + 1],
                    state[startRow + 2][startCol + 2]
                ])

        # Diagonal / lines
        for startRow in range(2, 4):
            for startCol in range(2):
                lines.append([
                    state[startRow][startCol],
                    state[startRow - 1][startCol + 1],
                    state[startRow - 2][startCol + 2]
                ])

        for line in lines:
            counts = {'X': 0, 'O': 0, '+': 0, None: 0}
            for cell in line:
                counts[cell] += 1

            playersPresent = []
            for player in ['X', 'O', '+']:
                if counts[player] > 0:
                    playersPresent.append(player)

            # Ignore blocked lines containing more than one player's marks
            if len(playersPresent) > 1:
                continue

            for player in ['X', 'O', '+']:
                if counts[player] == 2 and counts[None] == 1:
                    scores[player] += 20
                elif counts[player] == 1 and counts[None] == 2:
                    scores[player] += 4

        return [scores['X'], scores['O'], scores['+']]


    def player_index(self, player):
        if player == 'X':
            return 0
        elif player == 'O':
            return 1
        else:
            return 2


class TTT3PlayerAIPlayer:
    def __init__(self, model, symbol):
        self.model = model
        self.symbol = symbol

    def is_automated(self):
        return True

    # Assume actions are numbered 1-16
    def result(self, state, action):
        newstate = copy.deepcopy(state)
        turn = self._get_turn(state)

        action -= 1 # Adjustment of 1
        col = action % 4
        row = action // 4
        newstate[row][col] = turn

        return newstate

    def actions(self, state):
        moves = []
        for row in range(4):
            for col in range(4):
                if state[row][col] is None:
                    moves.append(row*4 + col + 1)
        return moves

    def terminal_test(self, state):
        # Check for horizontal win
        for row in range(4):
            for startcol in range(2):
                if state[row][startcol] is not None and state[row][startcol] == state[row][startcol+1] and state[row][startcol] == state[row][startcol+2]:
                    return True
        # Check for vertical win
        for col in range(4):
            for startrow in range(2):
                if state[startrow][col] is not None and state[startrow][col] == state[startrow+1][col] and state[startrow][col] == state[startrow+2][col]:
                    return True
        # Check for diagonal \ win
        for startrow in range(2):
            for startcol in range(2):
                if state[startrow][startcol] is not None and state[startrow][startcol] == state[startrow+1][startcol+1] and state[startrow][startcol] == state[startrow+2][startcol+2]:
                    return True
        # Check for diagonal / win
        for startrow in range(2,4):
            for startcol in range(2):
                if state[startrow][startcol] is not None and state[startrow][startcol] == state[startrow-1][startcol+1] and state[startrow][startcol] == state[startrow-2][startcol+2]:
                    return True
        
        return self._is_draw(state)

    def utility(self, state):
        if self._get_winner(state) == self.symbol:
            return 1000
        elif self._get_winner(state) is not None:
            return -1000
        if self._is_draw(state):
            return 0

        return 0 # Should not happen

    def _is_draw(self, state):
        all_filled = True
        for row in range(4):
            for col in range(4):
                if state[row][col] is None:
                    all_filled = False
        return all_filled

    def _get_winner(self, state):
        # Check for horizontal win
        for row in range(4):
            for startcol in range(2):
                if state[row][startcol] is not None and state[row][startcol] == state[row][startcol+1] and state[row][startcol] == state[row][startcol+2]:
                    return state[row][startcol]
        # Check for vertical win
        for col in range(4):
            for startrow in range(2):
                if state[startrow][col] is not None and state[startrow][col] == state[startrow+1][col] and state[startrow][col] == state[startrow+2][col]:
                    return state[0][col]
        # Check for diagonal \ win
        for startrow in range(2):
            for startcol in range(2):
                if state[startrow][startcol] is not None and state[startrow][startcol] == state[startrow+1][startcol+1] and state[startrow][startcol] == state[startrow+2][startcol+2]:
                    return state[startrow][startcol]
        # Check for diagonal / win
        for startrow in range(2,4):
            for startcol in range(2):
                if state[startrow][startcol] is not None and state[startrow][startcol] == state[startrow-1][startcol+1] and state[startrow][startcol] == state[startrow-2][startcol+2]:
                    return state[startrow][startcol]

        return None # Uh-oh

    def _get_turn(self, state):
        empties = 0
        for row in range(4):
            for col in range(4):
                if state[row][col] is None:
                    empties += 1

        if empties % 3 == 1:
            return 'X'
        elif empties % 3 == 0:
            return 'O'
        else:
            return '+'

    def get_move(self):
        """INSERT YOUR CODE HERE -- Should return an integer between 1-16"""
        pass


