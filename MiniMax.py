
from GameController import GameController
from StateClass import StateClass


class MiniMax:

    def __init__(self):
        '''
        0: Human (goes down)
        1: AI (AI goes up)
        '''

    def Alpha_Beta_Search(self, state):
        gameControl = GameController()
        best_val = float('-inf')
        beta = float('inf')
        resultingAction, resultingPiece, resultingInsertPos = None, None, None
        for (action, pieceId, insertPos) in gameControl.ACTIONS(state):
            child_node, piece_removed = state.RESULT(action, pieceId, insertPos)
            value = self.Min_Value(child_node, 8, best_val, beta)
            print("The action " + str(action) + " gives us eval value = " + str(value) + "after executing action.")
            if value > best_val:
                best_val = value
                resultingAction, resultingPiece, resultingInsertPos = action, pieceId, insertPos

        return resultingAction, resultingPiece, resultingInsertPos

    def Max_Value(self, state, depth, alpha, beta):
        if self.Cut_Off_Test(state, depth):
            return self.Eval(state)
        maxVal = float('-inf')
        gameControl = GameController()
        # TODO need to implement just switching of turns in case of no move available
        noMovesAvailable = True
        for (action, pieceId, insertPos) in gameControl.ACTIONS(state):
            noMovesAvailable = False
            nextState, pieceRemoved = state.RESULT(action, pieceId, insertPos)
            value = self.Min_Value(nextState, depth - 1, alpha, beta)
            maxVal = max(maxVal, value)
            alpha = max(alpha, value)
            if beta < alpha:
                # print('The node at depth = ' + str(depth))
                # nextState.printState()
                break
        if noMovesAvailable:
            nextState, pieceRemoved = state.changeTurnsOnlyAndGetNextState()
            value = self.Min_Value(nextState, depth - 1, alpha, beta)
            maxVal = max(maxVal, value)
        return maxVal

    def Min_Value(self, state, depth, alpha, beta):
        if self.Cut_Off_Test(state, depth):
            return self.Eval(state)
        minVal = float('inf')
        gameControl = GameController()
        noMovesAvailable = True
        for (action, pieceId, insertPos) in gameControl.ACTIONS(state):
            noMovesAvailable = False
            nextState, pieceRemoved = state.RESULT(action, pieceId, insertPos)
            value = self.Max_Value(nextState, depth - 1, alpha, beta)
            minVal = min(minVal, value)
            beta = min(beta, value)
            if beta <= alpha:
                break
        if noMovesAvailable:
            nextState, pieceRemoved = state.changeTurnsOnlyAndGetNextState()
            value = self.Max_Value(nextState, depth - 1, alpha, beta)
            minVal = min(minVal, value)
        return minVal

    # Returns True/False,Winner
    def Terminal_Test(self, state: StateClass):
        isTerminalState, winner = state.isTerminalState()
        return isTerminalState, winner

    def Utility(self, state):
        if state.score[1] == state.TerminalPoints:
            return 1000
        elif state.score[0] == state.TerminalPoints:
            return -1000

    def Eval(self, state: StateClass):
        isTerminalState, winner = self.Terminal_Test(state)
        if isTerminalState and winner == 1:
            return 1000
        elif isTerminalState and winner == 0:
            return -1000
        eval_val_ai, eval_val_human = 0, 0
        # AI
        eval_val_ai += state.score[1] * 100
        eval_val_human += state.score[0] * 100
        ## one step awy from scoring a point
        for piece in ['A1', 'A2', 'A3', 'A4']:
            piece_position = state.pieces[piece]
            if piece_position is not None:
                if piece_position[0] == 0:
                    eval_val_ai += 50
                    continue
                elif state.turn == 1 and piece_position[0] == 1:
                    if state.isPiecePossibleToMove('JumpOverOne', piece):
                        eval_val_ai += 50
                        continue
                elif state.turn == 1 and piece_position[0] == 2:
                    if state.isPiecePossibleToMove('JumpOverTwo', piece):
                        eval_val_ai += 50
                        continue
                elif state.turn == 1 and piece_position[0] == 3:
                    if state.isPiecePossibleToMove('JumpOverThree', piece):
                        eval_val_ai += 50
                        continue

        for piece in ['H1', 'H2', 'H3', 'H4']:
            piece_position = state.pieces[piece]
            if piece_position is not None:
                if piece_position[0] == 3:
                    eval_val_human += 50
                    continue
                elif state.turn == 0 and piece_position[0] == 2:
                    if state.isPiecePossibleToMove('JumpOverOne', piece):
                        eval_val_human += 50
                        continue
                elif state.turn == 0 and piece_position[0] == 1:
                    if state.isPiecePossibleToMove('JumpOverTwo', piece):
                        eval_val_human += 50
                        continue
                elif state.turn == 0 and piece_position[0] == 0:
                    if state.isPiecePossibleToMove('JumpOverThree', piece):
                        eval_val_human += 50
                        continue
        ## Attack
        if state.turn:
            for piece in ['A1', 'A2', 'A3', 'A4']:
                if state.isPiecePossibleToMove('Attack', piece):
                    eval_val_ai += 20
                    # we break here because only 1 attack is possible in the turn
                    break
        else:
            for piece in ['H1', 'H2', 'H3', 'H4']:
                if state.isPiecePossibleToMove('Attack', piece):
                    eval_val_human += 20
                    # we break here because only 1 attack is possible in the turn
                    break

        ## How far pieces are from scoring a point
        for piece in ['A1', 'A2', 'A3', 'A4']:
            piece_position = state.pieces[piece]
            if piece_position is not None and (
                    state.isPiecePossibleToMove('DiagonalLeft', piece) or state.isPiecePossibleToMove('DiagonalRight',
                                                                                                      piece)):
                if piece_position[0] == 1:
                    eval_val_ai += 5
                    continue
                elif piece_position[0] == 2:
                    eval_val_ai += 3
                    continue
                elif piece_position[0] == 3:
                    eval_val_ai += 1
                    continue

        for piece in ['H1', 'H2', 'H3', 'H4']:
            piece_position = state.pieces[piece]
            if piece_position is not None and (
                    state.isPiecePossibleToMove('DiagonalLeft', piece) or state.isPiecePossibleToMove('DiagonalRight',
                                                                                                      piece)):
                if piece_position[0] == 2:
                    eval_val_human += 5
                    continue
                elif piece_position[0] == 1:
                    eval_val_human += 3
                    continue
                elif piece_position[0] == 0:
                    eval_val_human += 1
                    continue
        return eval_val_ai - eval_val_human

    def Cut_Off_Test(self, state, depth):
        isTerminalState, winner = self.Terminal_Test(state)
        return depth == 0 or isTerminalState
