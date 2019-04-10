from connectfour.agents.computer_player import RandomAgent
import random

# need to implement alpha beta pruning

class StudentAgent(RandomAgent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 4

    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.
        Returns:
            A tuple of two integers, (row, col)
        """

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            next_state = board.next_state(self.id, move[1])
            moves.append( move )
            # vals.append( self.alphabeta(next_state, self.MaxDepth, -100000, 100000))
            vals.append( self.dfMiniMax(next_state, self.MaxDepth) )

        print(vals)
        bestMove = moves[vals.index( max(vals) )]
        return bestMove

    def dfMiniMax(self, board, depth):
        # Goal return column with maximized scores of all possible next states
        # Number of possible states is the number of columns
        # Alpha beta pruning

        if depth == self.MaxDepth:
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            if depth % 2 == 1:
                next_state = board.next_state(self.id % 2 + 1, move[1])
            else:
                next_state = board.next_state(self.id, move[1])

            moves.append( move )
            vals.append( self.dfMiniMax(next_state, depth + 1) )


        if depth % 2 == 1:
            bestVal = min(vals)
        else:
            bestVal = max(vals)

        return bestVal
    
    def alphabeta(self, board, depth, alpha, beta):
        
        # Initial call call(origin, depth, -inf, +inf)
        # Alpha beta pruning

        if depth == self.MaxDepth:
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()

        for move in valid_moves:
            if depth % 2 == 1:  # Maximizing
                value = alpha
                next_state = board.next_state(self.id % 2 + 1, move[1])
                value = max(value, self.alphabeta(next_state, depth + 1, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            else:  # Minimizing
                value = beta
                next_state = board.next_state(self.id, move[1])
                value = min(value, self.alphabeta(next_state, depth + 1, alpha, beta))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    def evaluateBoardState(self, board):
        # Heuristics ideas, check for fours, threes and twos.
        # Threes worth more than two.
        # center columns have more alignments. explore center first.
        """
        Your evaluation function should look at the current state and return a score for it. 
        As an example, the random agent provided works as follows:
            If the opponent has won this game, return -1.
            If we have won the game, return 1.
            If neither of the players has won, return a random number.
        """
        
        """
        These are the variables and functions for board objects which may be helpful when creating your Agent.
        Look into board.py for more information/descriptions of each, or to look for any other definitions which may help you.
        Board Variables:
            board.width 
            board.height
            board.last_move
            board.num_to_connect
            board.winning_zones
            board.score_array 
            board.current_player_score
        Board Functions:
            get_cell_value(row, col)
            try_move(col)
            valid_move(row, col)
            valid_moves()
            terminal(self)
            legal_moves()
            next_state(turn)
            winner()
        """
        score = self.scoreBoard(board, 1)

        if score == 0:
            score = random.randint(1,9)

        return score

    def scoreValues(self, coor_values = [], player_no = 1):

        if player_no == 1:
            enemy = 2
        else:
            enemy = 1
            player_no = 2
        score = 0

        if coor_values.count(player_no) == 4:
            score += 100
        elif coor_values.count(player_no) == 3 and coor_values.count(0) == 1:
            score += 10
        elif coor_values.count(player_no) == 2 and coor_values.count(0) == 2:
            score += 5

        if coor_values.count(enemy) == 3 and coor_values.count(0) == 1:
            score -= 100  # Blocks if enemy wins.

        return score


    def scoreBoard(self, board, player_no=1):

        score = 0
        coor_values = []  # Saves 4 coordinate values.
        count = 0

        # Horizontal
        for row in range(board.height):
            for col in range(board.width - 3):
                for i in range(4):
                    coor_values.append(board.get_cell_value(row, col + i))

                score += self.scoreValues(coor_values, player_no)
                del coor_values[:]

        # Vertical
        for col in range(board.width):
            for row in range(board.height - 3):
                for i in range(4):
                    coor_values.append(board.get_cell_value(row + 3 - i, col))

                score += self.scoreValues(coor_values, player_no)
                del coor_values[:]

        # Diagonals
        # Left right upward
        for row in range(board.height - 3):
            for col in range(board.width - 3):
                for i in range(4):
                    coor_values.append(board.get_cell_value(row + 3 - i, col + i))

                score += self.scoreValues(coor_values, player_no)
                del coor_values[:]


        # Left right downward
        for row in range(board.height - 3):
            for col in range(board.width - 3):
                for i in range(4):
                    coor_values.append(board.get_cell_value(row + i, col + i))

                score += self.scoreValues(coor_values, player_no)
                del coor_values[:]

        return score

