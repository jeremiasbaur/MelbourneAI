from copy import copy, deepcopy
import random
import math, json

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
        with open('./agent/factors.json', 'r') as f:
            self.parameter_dict=json.load(f)[self.color2char(self._color)]

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
        random.shuffle(possible_moves)
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
                return -100000
            return 100000

        if len(cells[opponent_color]) == 0:
            return 100000
        elif len(cells[our_color])==0:
            return -100000
        return 0

    def spread_check(self, state, color, cells):
        # check where our cells are 
        same_colour_cells = 0

        # for each of our cells, check all neighbouring cells to see if they are the same colour
        if color == PlayerColor.BLUE: # if we are blue player
            for cell in cells['b']:
                    for dir in self._directions: #check each direction
                        check_colour = state.at(cell[0]+dir.r, cell[1]+dir.q) #(r,q)
                        if check_colour == 'b':
                            same_colour_cells += 1
        else: # if we are red player
            for cell in cells['r']:
                    for dir in self._directions: #check each direction
                        check_colour = state.at(cell[0]+dir.r, cell[1]+dir.q) #(r,q)
                        if check_colour == 'r':
                            same_colour_cells += 1

        return same_colour_cells

    def cell_powers(self, cells) -> dict:
        # this function counts the specific amount of power x cells for both blue and red. Index 0 of the list is the general amount of cells of the specific color
        power_counter_dict = {PlayerColor.RED: [0 for i in range(8)], PlayerColor.BLUE: [0 for i in range(8)]}
        for red in cells['r']:
            power_counter_dict[PlayerColor.RED][red[2]] += 1
            power_counter_dict[PlayerColor.RED][0] += 1
            power_counter_dict[PlayerColor.RED][7] += red[2]
        
        for blue in cells['b']:
            power_counter_dict[PlayerColor.BLUE][blue[2]] += 1
            power_counter_dict[PlayerColor.BLUE][0] += 1
            power_counter_dict[PlayerColor.BLUE][7] += blue[2]
        
        return power_counter_dict

    def utility_state_function(self, state, color: PlayerColor) -> float:
        """
        returns a eval value for a given state
        """
        cells = state.find_non_empty_cells()
        power_counter_dict = self.cell_powers(cells)

        #parameters:
        if True:
            a_1=self.parameter_dict['a_1']
            a_2 = self.parameter_dict['a_2']
            a_3=self.parameter_dict['a_3']
            a_4=self.parameter_dict['a_4']
            a_5=self.parameter_dict['a_5']
            a_6=self.parameter_dict['a_6']
            a_tot=self.parameter_dict['a_tot']
            b=self.parameter_dict['b']
            island_factor=self.parameter_dict['island_factor']
        else:
            a_1=0.5
            a_2=1.2
            a_3=1.2
            a_4=1.55
            a_5=1.7
            a_6=1.8
            a_tot = 3

            b = 0.1
            island_factor = 0.1

        island_value = self.spread_check(state, color, cells)
        final_steps = state.heuristic('b' if color==PlayerColor.BLUE else 'r')

        power_counter_value = a_1 * (power_counter_dict[color][1]-power_counter_dict[color.opponent][1]) + \
                                a_2 * (power_counter_dict[color][2]-power_counter_dict[color.opponent][2]) + \
                                a_3 * (power_counter_dict[color][3]-power_counter_dict[color.opponent][3]) + \
                                a_4 * (power_counter_dict[color][4]-power_counter_dict[color.opponent][4]) + \
                                a_5 * (power_counter_dict[color][5]-power_counter_dict[color.opponent][5]) + \
                                a_6 * (power_counter_dict[color][6]-power_counter_dict[color.opponent][6]) + \
                                a_tot * (power_counter_dict[color][0]-power_counter_dict[color.opponent][0])

        if color == PlayerColor.BLUE:
            return power_counter_value + \
                    b*(1/(1 if final_steps==1 else final_steps)) + \
                    island_value*island_factor
        else:
            return power_counter_value + \
                    b*(1/(1 if final_steps==1 else final_steps)) +\
                    island_value*island_factor
        

    def minimax_value(self, state, color: PlayerColor, depth, alpha, beta, game_steps):
        #print(color, depth, alpha, beta)
        if depth==0:
            end_val = (self.utility_state_function(state, color),0)
            #print("reached depth end:", end_val,'\n', state)
            return end_val
        
        win = self.terminal_state_check(state, color)
        if win!=0 and not (game_steps==1 or game_steps==0):
            #print("winner winner chicken dinner:\n", state, win, end='')
            return (win,0)

        if color==self._color:
            max_val = float('-inf')
            best_move = None
            possible_moves = self.find_possible_moves(state, color)
            
            for move in possible_moves: #random.choices(possible_moves, k=5):
                new_state = deepcopy(state)
                new_state.apply_action(move, self.color2char(color))
                eval = self.minimax_value(new_state, color.opponent, depth-1, alpha, beta,game_steps+1)[0]
                if max_val < eval:
                    best_move = move
                    max_val = eval
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return (max_val, best_move)
        else:
            min_val = float('inf')
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
        
    def color2char(self, color):
        if color == PlayerColor.BLUE: return 'b'
        if color == PlayerColor.RED: return 'r'
    

    def json2constants(self, json_string) -> dict:
        self.parameter_dict = json.loads(json_string)