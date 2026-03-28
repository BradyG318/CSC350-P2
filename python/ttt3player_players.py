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
        best_move = None
        best_vector = None

        for action in self.actions(state):
            next_state = self.result(state, action)
            value = self.maxN(next_state, depth=1)

            if best_vector is None or value[self._player_index(self.symbol)] > best_vector[self._player_index(self.symbol)]:
                best_vector = value
                best_move = action

        return best_move

    #Helper Functions for Q8:
    def maxN(self, state, depth, max_depth=5):
        if self.terminal_test(state) or depth >= max_depth:
            return self._utility_vector(state)

        turn = self._get_turn(state)
        turn_index = self._player_index(turn)

        best_value = None

        for action in self.actions(state):
            child = self.result(state, action)
            value = self.maxN(child, depth + 1, max_depth)

            if best_value is None or value[turn_index] > best_value[turn_index]:
                best_value = value

        return best_value

    def _utility_vector(self, state):
        winner = self._get_winner(state)

        if winner == 'X':
            return [1000, -1000, -1000]
        elif winner == 'O':
            return [-1000, 1000, -1000]
        elif winner == '+':
            return [-1000, -1000, 1000]
        elif self._is_draw(state):
            return [0, 0, 0]

        # Non-terminal heuristic for cutoff states
        return self._evaluate_nonterminal(state)

    def _evaluate_nonterminal(self, state):
        scores = {'X': 0, 'O': 0, '+': 0}

        lines = []

        # Horizontal 3-cell lines
        for row in range(4):
            for startcol in range(2):
                lines.append([state[row][startcol], state[row][startcol+1], state[row][startcol+2]])

        # Vertical 3-cell lines
        for col in range(4):
            for startrow in range(2):
                lines.append([state[startrow][col], state[startrow+1][col], state[startrow+2][col]])

        # Diagonal \ lines
        for startrow in range(2):
            for startcol in range(2):
                lines.append([state[startrow][startcol], state[startrow+1][startcol+1], state[startrow+2][startcol+2]])

        # Diagonal / lines
        for startrow in range(2, 4):
            for startcol in range(2):
                lines.append([state[startrow][startcol], state[startrow-1][startcol+1], state[startrow-2][startcol+2]])

        for line in lines:
            counts = {'X': 0, 'O': 0, '+': 0, None: 0}
            for cell in line:
                counts[cell] += 1

            players_present = [p for p in ['X', 'O', '+'] if counts[p] > 0]

            # Ignore blocked lines with multiple players
            if len(players_present) > 1:
                continue

            # Reward unblocked progress
            for p in ['X', 'O', '+']:
                if counts[p] == 2 and counts[None] == 1:
                    scores[p] += 20
                elif counts[p] == 1 and counts[None] == 2:
                    scores[p] += 4

        return [scores['X'], scores['O'], scores['+']]

    def _player_index(self, player):
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


