# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from .game_state import GameState

# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

class RandomAgent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        self._state = GameState()
        self._game_turns = 0

        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        if self._game_turns == 0:
            return SpawnAction(HexPos(3, 3)) # doesn't matter where we spawn, every pos is the same
        
        moves = self.find_possible_moves(self._state, self._color)

        return random.choice(moves)
    
    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the  with the last player's action.
        """
        self._state.apply_action(action, self.color2char(color))
        self._game_turns += 1

        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                pass
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                pass

    def color2char(self, color: PlayerColor):
        if color.BLUE: return 'b'
        if color.RED: return 'r'


    def find_possible_moves(self, state, color):
        cells = state.find_non_empty_cells()
        opponent_color = 'r' if color==PlayerColor.BLUE else 'b'
        our_color = 'r' if color==PlayerColor.RED else 'b'

        non_empty_cells = set()
        possible_moves = []
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