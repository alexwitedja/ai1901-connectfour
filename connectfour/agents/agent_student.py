from connectfour.agents.computer_player import RandomAgent
import random

#python -m connectfour.game --player-one HumanPlayer --player-two StudentAgent --fast
#python -m connectfour.game --player-one StudentAgent --player-two HumanPlayer --fast
#python -m connectfour.game --player-one RandomAgent --player-two StudentAgent --fast
#python -m connectfour.game --player-one StudentAgent --player-two RandomAgent --fast
#python -m connectfour.game --player-one StudentAgent --player-two MonteCarloAgent --fast
#python -m connectfour.game --player-one MonteCarloAgent --player-two RandomAgent --fast

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
            moves.append(move)
            vals.append( self.alphabeta(next_state, 1, float('-inf'), float('inf')))
            # vals.append(self.dfMiniMax(next_state, self.MaxDepth))
            # vals.append(self.executeAlphaBeta(next_state, 0, float('-inf'), float('inf'), move))


        print("Best Values: " + str(vals))
        bestMove = moves[vals.index(max(vals))]
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

            moves.append(move)
            vals.append(self.dfMiniMax(next_state, depth + 1))

        if depth % 2 == 1:
            bestVal = min(vals)
        else:
            bestVal = max(vals)

        return bestVal

    def alphabeta(self, board, depth, alpha, beta):

        # Initial call call(origin, depth, -inf, +inf)
        # Alpha beta pruning

        terminalCheck = self.terminalNode(board)
        if depth == self.MaxDepth or terminalCheck:
            if terminalCheck:  # Game over
                if board.winner() == self.id:  # agent wins
                    return 1000000000
                elif board.winner() == self.id % 2 + 1:  # opp wins
                    return -100000000
                else:  # draw
                    return 0
            else:  # if not terminal score it using function
                return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()

        for move in valid_moves:
            if depth % 2 == 1:  # Maximizing
                value = alpha
                next_state = board.next_state(self.id % 2 + 1, move[1])  # Pass in child move.
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

    def terminalNode(self, board):
        return board.winner() == 1 or board.winner() == 2 or len(list(board.valid_moves())) == 0

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

        score = self.scoreBoard(board)
        return score

    def scoring(self, agent, emptyagent, opp, emptyopp, agentrow, opprow):

        # Trying to implement Odd/Even strategy.

        score = 0
        if agent == 4:
            score += 80
        elif agent == 3 and emptyagent == 1:
            score += 20
            if self.id == 1:  # Check row threat for agent
                if agentrow % 2 == 0:
                    score += 15  # Beaten hard when this weighs 10.
            else:
                if agentrow % 2 == 1:
                    score += 15
        elif agent == 2 and emptyagent == 2:
            score += 8

        if opp == 4:
            score -= 200
        elif opp == 3 and emptyopp == 1:
            score -= 100
            if self.id % 2 + 1 == 1:  # Check row threat for opp.
                if opprow % 2 == 0:
                    score -= 5
            else:
                if opprow % 2 == 1:
                    score -= 5
        elif opp == 2 and emptyopp == 2:
            score -= 20

        return score

    def scoreBoard(self, board):

        agentPiece = 0
        emptyAgentPiece = 0
        oppPiece = 0
        emptyOppPiece = 0

        score = 0

        # First few moves should be center col. More possibilities in the center.
        # Center should be a preference
        center = []
        for i in range(board.height):
            center.append(board.get_cell_value(board.height - 1 - i, board.width // 2))
        score += center.count(self.id) * 11

        # Horizontal
        for row in range(board.height):
            for col in range(board.width - 3):
                rowA = 0
                rowOpp = 0
                for i in range(4):
                    value = board.get_cell_value(row, col + i)
                    if i == 0:
                        if value == 0:
                            if board.get_cell_value(row, col + 1) == self.id:
                                emptyAgentPiece += 1
                                rowA = row
                            else:
                                emptyOppPiece += 1
                                rowOpp = row
                    if value == self.id:
                        agentPiece += 1
                    if value == 0 and agentPiece > 0:
                        emptyAgentPiece += 1
                        rowA = row
                    if value == self.id % 2 + 1:
                        oppPiece += 1
                    if value == 0 and oppPiece > 0:
                        emptyOppPiece += 1
                        rowOpp = row

                score += self.scoring(agentPiece, emptyAgentPiece, oppPiece,
                                         emptyOppPiece, rowA, rowOpp)

                agentPiece = emptyAgentPiece = oppPiece = emptyOppPiece = 0

        # Vertical
        for col in range(board.width):
            for row in range(board.height - 3):
                rowA = 0
                rowOpp = 0
                for i in range(4):
                    value = board.get_cell_value(row + 3 - i, col)
                    if i == 0:
                        if value == 0:
                            if board.get_cell_value(row + 3 - 1, col) == self.id:
                                emptyAgentPiece += 1
                                rowA = row + 3
                            else:
                                emptyOppPiece += 1
                                rowOpp = row + 3
                    if value == self.id:
                        agentPiece += 1
                    if value == 0 and agentPiece > 0:
                        emptyAgentPiece += 1
                        rowA = row + 3 - i
                    if value == self.id % 2 + 1:
                        oppPiece += 1
                    if value == 0 and (oppPiece > 0):
                        emptyOppPiece += 1
                        rowOpp = row + 3 - i

                score += self.scoring(agentPiece, emptyAgentPiece, oppPiece,
                                         emptyOppPiece, rowA, rowOpp)

                agentPiece = emptyAgentPiece = oppPiece = emptyOppPiece = 0

        # Diagonals
        # Left right upward
        for row in range(board.height - 3):
            for col in range(board.width - 3):
                rowA = 0
                rowOpp = 0
                for i in range(4):
                    value = board.get_cell_value(row + 3 - i, col + i)
                    if i == 0:
                        if value == 0:
                            if board.get_cell_value(row + 3 - 1, col + 1) == self.id:
                                emptyAgentPiece += 1
                                rowA = row + 3
                            else:
                                emptyOppPiece += 1
                                rowOpp = row + 3
                    if value == self.id:
                        agentPiece += 1
                    if value == 0 and agentPiece > 0:
                        emptyAgentPiece += 1
                        rowA = row + 3 - i
                    if value == self.id % 2 + 1:
                        oppPiece += 1
                    if value == 0 and oppPiece > 0:
                        emptyOppPiece += 1
                        rowOpp = row + 3 - i

                score += self.scoring(agentPiece, emptyAgentPiece, oppPiece,
                                         emptyOppPiece, rowA, rowOpp)

                agentPiece = emptyAgentPiece = oppPiece = emptyOppPiece = 0

        # Left right downward
        for row in range(board.height - 3):
            for col in range(board.width - 3):
                rowA = 0
                rowOpp = 0
                for i in range(4):
                    value = board.get_cell_value(row + i, col + i)
                    if i == 0:
                        if value == 0:
                            if board.get_cell_value(row + 1, col + 1) == self.id:
                                emptyAgentPiece += 1
                                rowA = row + 1
                            else:
                                emptyOppPiece += 1
                                rowOpp = row + 1
                    if value == self.id:
                        agentPiece += 1
                    if value == 0 and agentPiece > 0:
                        emptyAgentPiece += 1
                        rowA = row + 1 + i
                    if value == self.id % 2 + 1:
                        oppPiece += 1
                    if value == 0 and oppPiece > 0:
                        emptyOppPiece += 1
                        rowOpp = row + 1 + i

                score += self.scoring(agentPiece, emptyAgentPiece, oppPiece,
                                         emptyOppPiece, rowA, rowOpp)

                agentPiece = emptyAgentPiece = oppPiece = emptyOppPiece = 0

        return score