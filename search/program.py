# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion
import heapq, time
from copy import deepcopy


from .utils import render_board
from .coordinate_system import CoordinateSystem

def search(input: dict[tuple, tuple], print_moves=False, heuristic=True, sixdiv=True, bluecounts=False, perc=True) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary
    of board cell states, where the keys are tuples of (r, q) coordinates, and
    the values are tuples of (p, k) cell states. The output should be a list of 
    actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    See the specification document for more details.
    """

    # The render_board function is useful for debugging -- it will print out a 
    # board state in a human-readable format. Try changing the ansi argument 
    # to True to see a colour-coded version (if your terminal supports it).
    
    t1 = time.time()
    q = [] # heap
    explored = dict()
    backtracking = dict()

    cs = CoordinateSystem() # initial state
    cs.import_state(input)
    start_state = hash(cs)
    final_state = None

    heapq.heappush(q, (0,cs, 0, 0, 0, start_state)) # q.put((0,cs))
    explored[hash(cs)] = 0
    counter = 0
    if print_moves: print(cs)
    
    while len(q) != 0:
        new_item = heapq.heappop(q)
        current_state = new_item[1]
        non_empty_cells = current_state.find_non_empty_cells()
       
        counter += 1

        if len(non_empty_cells['b'])==0:
            final_state = new_item[5]
            print("reached final state!", new_item[4],'after',time.time()-t1)
            break
        
        for red_cell in non_empty_cells['r']:
            for spread_dir in [(-1,1),(0,1),(1,0),(1,-1),(0,-1),(-1,0)]:
                new_state = CoordinateSystem()
                new_state = deepcopy(current_state) # new_state.import_state_list(current_state.export_state_list())

                new_state.apply_spread(red_cell[0],red_cell[1], spread_dir[0],spread_dir[1])
                move = (red_cell[0],red_cell[1], spread_dir[0],spread_dir[1])
                
                new_hash = hash(new_state)
                if new_hash not in explored:
                    h = new_state.heuristic(blue_count=False)
                    p = new_state.percentage_heuristic()
                    
                    steps = new_item[4]+1
                    h = max(h,p) if heuristic else 0
                    cost = steps + h
                    #if len(nec['b'])==0:
                    #print(cost, steps, (h, p, blue),"\n", new_state,"\nend")
                    item = (cost, new_state, new_item[5], move, steps, new_hash)
                    heapq.heappush(q, item)
                    
                    backtracking[item[5]] = item
                    explored[item[5]] = item[4]
            
    moves = []
    moves_states = []
    current_state = final_state
    while current_state!=start_state:
        move = backtracking[current_state]
        moves.append(move[3])
        moves_states.append(move[1])
        current_state = move[2]

    moves.reverse()
    moves_states.reverse()
    if False:
        for i in moves_states:
            if print_moves:
                print(i)

    return moves