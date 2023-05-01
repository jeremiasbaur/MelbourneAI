from copy import copy, deepcopy

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

class MiniMax:
    def __init__(self, color) -> None:
        self._all_cells = set((x, y) for x in range(7) for y in range(7))    
        self._directions = (HexDir.Down, HexDir.Up, HexDir.UpLeft, HexDir.DownLeft, HexDir.DownRight, HexDir.UpRight)
        self._memo = dict()
        self._color = color # true player color
        self._depth = 0


    def find_possible_moves(self, state, color):
        cells = state.find_non_empty_cells()
        opponent_color = 'r' if color==PlayerColor.BLUE else 'b'
        our_color = 'r' if color==PlayerColor.RED else 'b'

        non_empty_cells = set()
        possible_moves = []
        #print(state, f'our color: {our_color}')
        for cell in cells[our_color]:
            non_empty_cells.add((cell[0],cell[1]))
            for dir in self._directions:
                possible_moves.append(SpreadAction(HexPos(cell[0],cell[1]),dir))

        for cell in cells[opponent_color]:
            non_empty_cells.add((cell[0],cell[1]))
        
        empty_cells = self._all_cells - non_empty_cells

        for empty in empty_cells:
            possible_moves.append(SpawnAction(HexPos(empty[0],empty[1])))
        return possible_moves


    def minimax_decision(self, state, color) -> list:
        possible_moves = self.find_possible_moves(state, color)
        #state_hash = hash(state)
        #self._memo[state_hash] 
        moves = []
        new_state = deepcopy(state)

        for move in possible_moves:
            new_state.apply_action(move, color)
            moves.append((self.minimax_value(new_state, color), move))
        return moves        


    def terminal_state_check(self, state, color):
        # TODO add 343 check
        cells = state.find_non_empty_cells()
        opponent_color = 'r' if color==PlayerColor.BLUE else 'b'
        our_color = 'r' if color==PlayerColor.RED else 'b'

        if len(cells[opponent_color]) == 0:
            return (True, True)
        elif len(cells[our_color])==0:
            return (True, False)
        return (False, False)


    def utilty_state_function(self, state, color) -> float:
        """
        returns a utility value for a given state
        """
        cells = state.find_non_empty_cells()

        utiltiy_value_state = 0
        if color == PlayerColor.BLUE:
            for key, value in cells['b'].items():
                utiltiy_value_state += value[2]
        else:
            for key, value in cells['r'].items():
                utiltiy_value_state += value[2]
        return utiltiy_value_state
    

    def minimax_value(self, state, color):
        self._depth += 1
        over, winner = self.terminal_state_check(state, color)
        if over:
            if winner:
                return 100
            return -100
        
        other_color = 'r' if color=='b' else 'b'

        if color == self._color:
            max(self.minimax_decision(state, other_color))
        else:
            min(self.minimax_decision(state, other_color))