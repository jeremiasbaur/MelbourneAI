from copy import copy, deepcopy

from .utils import render_board

class CoordinateSystem():
    """
    This is the state class of the game board.
    The board is stored in a 2D array of lists.
    """
    _coordinate_system = ""

    def __init__(self) -> None:
        self._coordinate_system = list()
        for i in range(7):
            self._coordinate_system.append(list())
            for j in range(7):
                self._coordinate_system[i].append(('e', 0 ))
    
    def __str__(self) -> str:
        return render_board(self.convert_to_dict(), ansi=True)

    def __hash__(self) -> int:
        cs_hash = list()
        for i in range(7):
            cs_hash.append(tuple(self._coordinate_system[i]))
        return hash(tuple(cs_hash))

    def __lt__(self, other):
        return self.find_non_empty_cells()['r'] < other.find_non_empty_cells()['r']

    
    def __le__(self, other):
        return self.find_non_empty_cells()['r'] <= other.find_non_empty_cells()['r']


    def __copy__(self):
        pass

    def convert_to_dict(self) -> dict:
        coord_dict = dict()

        for i in range(7):
            for j in range(7):
                if self.at(i,j) != ('e', 0):
                    coord_dict[(i,j)] = self.at(i,j)
        return coord_dict

    def at(self, r, q) -> tuple:
        return self._coordinate_system[r%7][q%7]
    
    def set(self, r, q, color, power):
        if color not in ['r','b','e']:
            raise Exception("Impossible color!")
        self._coordinate_system[r%7][q%7] = (color, power)
    
    def import_state(self, given_state):
        """
        loads the given state into the CoordinateSystem

        given_state: dict of state in the format of the class
        """
        for key, value in given_state.items():
            self._coordinate_system[key[0]][key[1]] = value # r is first coordinate and q is second coordinate

    def import_state_list(self, given_state_list):
        self._coordinate_system = deepcopy(given_state_list)

    def export_state_list(self) -> list:
        return self._coordinate_system

    def find_non_empty_cells(self) -> dict:
        cells = dict()
        cells['r'] = []
        cells['b'] = []

        for i in range(7):
            for j in range(7):
                if self.at(i,j)[0] != 'e':
                    cells[self.at(i,j)[0]].append((i,j,self.at(i,j)[1]))
        return cells
    
    def apply_spread(self,r,q,d_r,d_q):
        """
        given a cell, apply a spread from (r,q) into the d_r and d_q direction
        """
        if (d_r,d_q) not in [(-1,1),(0,1),(1,0),(1,-1),(0,-1),(-1,0)]:
            raise Exception(f'Invalid spread direction!\n{(d_r,d_q)} is not possible!')

        current_cell = self.at(r,q)

        if current_cell[0] == 'e':
            raise Exception("Not possible to spread because empty cell!!")

        for i in range(current_cell[1]+1): # get the power of cell and spread into the direction according to given power
            new_cell = (r + d_r*i, q + d_q*i) 

            new_cell_state = self.at(new_cell[0],new_cell[1])

            self.set(new_cell[0], new_cell[1], current_cell[0], new_cell_state[1]+1)

        self.set(r, q, 'e', 0)