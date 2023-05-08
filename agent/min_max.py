from copy import copy, deepcopy
import random
import math

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

class MiniMax:
    def __init__(self, color: PlayerColor) -> None:
        self._all_cells = set((x, y) for x in range(7) for y in range(7))    
        self._directions = (HexDir.Down, HexDir.Up, HexDir.UpLeft, HexDir.DownLeft, HexDir.DownRight, HexDir.UpRight)
        self._memo = dict()
        self._color = color # true player color in PlayerColor
        self._depth = 0
        self.first = True

    def find_possible_moves(self, state, color: PlayerColor):
        cells = state.find_non_empty_cells()
        opponent_color = 'r' if color==PlayerColor.BLUE else 'b'
        our_color = 'b' if color==PlayerColor.BLUE else 'r'

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

        for empty in empty_cells: #random.choices(list(empty_cells), k=len(empty_cells)):
            possible_moves.append(SpawnAction(HexPos(empty[0],empty[1])))
        return possible_moves


    def minimax_decision(self, state, color: PlayerColor, depth, maximizing_player) -> list:
        possible_moves = self.find_possible_moves(state, color)
        #state_hash = hash(state)
        #self._memo[state_hash] 
        moves = []

        for move in random.choices(possible_moves, k=5):
            new_state = deepcopy(state)
            new_state.apply_action(move, color)
            moves.append((self.minimax_value(new_state, color, depth), move, depth))
        return moves


    def terminal_state_check(self, state, color: PlayerColor):
        # TODO add 343 check
        cells = state.find_non_empty_cells()
        opponent_color = 'r' if self._color==PlayerColor.BLUE else 'b'
        our_color = 'r' if self._color==PlayerColor.RED else 'b'

        total_sum = 0
        for blue in cells['b']:
            total_sum += blue[2]
        for red in cells['r']:
            total_sum += red[2]

        if total_sum>=49:
            if color == self._color:
                return -1000000000
            return 100000000

        if len(cells[opponent_color]) == 0:
            return 1000000000000
        elif len(cells[our_color])==0:
            return -100000000000
        return 0

    def utility_state_function(self, state, color: PlayerColor) -> float:
        """
        returns a eval value for a given state
        """
        cells = state.find_non_empty_cells()

        #parameters:
        a_1 = 1
        a_2 = -1.5
        b = 0.1
        power_value = 1.2
        diff_factor = 0.1

        blue_utilitiy_value_state = 0
        blue_value = 0
        red_utilitiy_value_state = 0
        red_value = 0
        blue_count = 1
        red_count = 1

        for value in cells['b']:
            blue_utilitiy_value_state += value[2]**power_value
            blue_value+=value[2]
            blue_count +=1

        for value in cells['r']:
            red_utilitiy_value_state += value[2]**power_value
            red_value += value[2]
            red_count += 1

        final_steps = state.heuristic('b' if color==PlayerColor.BLUE else 'r')

        if color == PlayerColor.BLUE:
            return a_1*blue_utilitiy_value_state + a_2 * red_utilitiy_value_state + b*(1/(-1 if final_steps==1 else final_steps)) + diff_factor*(blue_value/blue_count-red_value/red_count)
        else:
            return a_2*blue_utilitiy_value_state + a_1 * red_utilitiy_value_state + b*(1/(-1 if final_steps==1 else final_steps)) + diff_factor*(red_value/red_count-blue_value/blue_count)
    

    def minimax_value(self, state, color: PlayerColor, depth, alpha, beta, game_steps):
        #print(color, depth, alpha, beta)
        if depth==0:
            end_val = (self.utility_state_function(state, color),0)
            #print("reached depth end:", end_val,'\n', state)
            return end_val
        
        win = self.terminal_state_check(state, color)
        if win!=0 and not (game_steps==1 or game_steps==0):
            print("winner winner chicken dinner:",state)
            return (win,0)

        if color==self._color:
            max_val = -100000000000
            best_move = None
            possible_moves = self.find_possible_moves(state, color)
            
            for move in possible_moves: #random.choices(possible_moves, k=5):
                new_state = deepcopy(state)
                new_state.apply_action(move, self.color2char(color))
                eval = self.minimax_value(new_state, color.opponent, depth-1, alpha, beta,game_steps+1)[0]
                if max_val < eval:
                    best_move = move
                    max_val = max(max_val,eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return (max_val, best_move)
        else:
            min_val = 10000000000000
            best_move = None
            possible_moves = self.find_possible_moves(state, color)
            
            for move in possible_moves: #random.choices(possible_moves, k=10):
                new_state = deepcopy(state)
                new_state.apply_action(move, self.color2char(color))
                eval = self.minimax_value(new_state, color.opponent, depth-1, alpha, beta, game_steps+1)[0]
                if min_val > eval:
                    best_move = move
                    min_val = eval
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return (min_val, best_move)
        
        """res = self.minimax_decision(state, other_color, depth-1)
        if color == self._color:
            return min(res, key=lambda x:x[0])[0]
        else:
            return max(res, key=lambda x:x[0])[0]"""
        
    def color2char(self, color):
        if color == PlayerColor.BLUE: return 'b'
        if color == PlayerColor.RED: return 'r'