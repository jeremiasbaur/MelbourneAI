# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion
import heapq

from .utils import render_board
from .coordinate_system import CoordinateSystem

def search(input: dict[tuple, tuple]) -> list[tuple]:
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
    
    q = [] # heap
    explored = set()
    backtracking = dict()

    cs = CoordinateSystem() # initial state
    cs.import_state(input)
    heapq.heappush(q, (0,cs)) # q.put((0,cs))
    explored.add(hash(cs))
    counter = 0

    start_state = hash(cs)
    final_state = None
    while len(q) != 0: # q.empty() is False:
        new_item = heapq.heappop(q)
        current_state = new_item[1] # q.get()[1]
        non_empty_cells = current_state.find_non_empty_cells()

        # TODO: add final state reached check
        if len(non_empty_cells['b'])==0:
            final_state = hash(current_state)
            # print("reached final state!")
            break

        for red_cell in non_empty_cells['r']:
            for spread_dir in [(-1,1),(0,1),(1,0),(1,-1),(0,-1),(-1,0)]:
                new_state = CoordinateSystem()
                new_state.import_state_list(current_state.export_state_list())

                new_state.apply_spread(red_cell[0],red_cell[1], spread_dir[0],spread_dir[1])
                nec = new_state.find_non_empty_cells()
                
                move = (red_cell[0],red_cell[1], spread_dir[0],spread_dir[1])

                if hash(new_state) not in explored:
                    # item = (len(nec['b']), new_state, hash(current_state), move)
                    item = (new_item[0]+1, new_state, hash(current_state), move)
                    heapq.heappush(q, item) # q.put((len(nec['b']), new_state))
                    explored.add(hash(new_state))
                    backtracking[hash(new_state)] = item

    moves = []
    current_state = final_state
    while current_state!=start_state:
        move = backtracking[current_state]
        moves.append(move[3])
        current_state = move[2]

    """while len(q)!=0:
        state = heapq.heappop(q)[1]
        print(state)"""
    
    """for i in range(20):
        print(q[-i][1])"""

    #print(render_board(input, ansi=False))

    moves.reverse()

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    return moves