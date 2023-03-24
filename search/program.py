# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion
import heapq
from copy import deepcopy


from .utils import render_board
from .coordinate_system import CoordinateSystem, CoordinateSystem2

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
    explored = dict()
    backtracking = dict()

    cs = CoordinateSystem2() # initial state
    cs.import_state(input)
    heapq.heappush(q, (0,cs)) # q.put((0,cs))
    explored[hash(cs)] = 0
    counter = 0

    for i in range(7):
        for j in range(7):
            if i==3 and j==3:
                continue
            dis = cs.calculate_distance2(3,3,i,j)
            cs.set(i,j,'r',dis)
    print(cs)
    
    start_state = hash(cs)
    final_state = None
    while len(q) != 0: # q.empty() is False:
        new_item = heapq.heappop(q)
        # new_item = q.pop()
        current_state = new_item[1] # q.get()[1]
        non_empty_cells = current_state.find_non_empty_cells()
        counter += 1

        # TODO: add final state reached check
        if len(non_empty_cells['b'])==0:
            final_state = hash(current_state)
            print("reached final state!", counter)
            break
        
        red_cell = ""
        min_distance = -1
        for red in non_empty_cells['r']:
            for blue in non_empty_cells['b']:
                if min_distance==-1:
                    red_cell = (red[0],red[1])
                    min_distance = current_state.calculate_distance(red[0],red[1], blue[0], blue[1])
                else:
                    red_cell = (red[0],red[1])
                    min_distance = min(min_distance, current_state.calculate_distance(red[0],red[1], blue[0], blue[1]))

        #for red_cell in non_empty_cells['r']:
        for spread_dir in [(-1,1),(0,1),(1,0),(1,-1),(0,-1),(-1,0)]:
            new_state = CoordinateSystem2()
            new_state = deepcopy(current_state) # new_state.import_state_list(current_state.export_state_list())

            new_state.apply_spread(red_cell[0],red_cell[1], spread_dir[0],spread_dir[1])
            nec = new_state.find_non_empty_cells()
            
            move = (red_cell[0],red_cell[1], spread_dir[0],spread_dir[1])

            if hash(new_state) not in explored:
                min_distance = -1
                for red in nec['r']:
                    for blue in nec['b']:
                        if min_distance==-1: min_distance = new_state.calculate_distance(red[0],red[1], blue[0], blue[1])
                        else:
                            min_distance = min(min_distance, new_state.calculate_distance(red[0],red[1], blue[0], blue[1]))

                #cost = 0
                #if min_distance==1:
                #    cost = len(nec['b'])
                    #q.clear()
                #else:
                cost = new_item[0]+1 + min_distance
                
                # item = (len(nec['b']), new_state, hash(current_state), move)
                item = (cost, new_state, hash(current_state), move)
                heapq.heappush(q, item) # q.put((len(nec['b']), new_state))
                # q.append(item)
                explored[hash(new_state)] = new_item[0]+1
                backtracking[hash(new_state)] = item
            
    moves = []
    moves_states = []
    current_state = final_state
    while current_state!=start_state:
        move = backtracking[current_state]
        moves.append(move[3])
        moves_states.append(move[1])
        current_state = move[2]
        #print(move[1])

    """while len(q)!=0:
        state = heapq.heappop(q)[1]
        print(state)"""
    
    """for i in range(20):
        print(q[-i][1])"""

    #print(render_board(input, ansi=False))

    moves.reverse()
    moves_states.reverse()
    if True:
        for i in moves_states:
            print("")

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    return moves