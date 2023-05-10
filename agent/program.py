# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent
import random 

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from .min_max import MiniMax
from .game_state import GameState

# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

output = False

class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        self._state = GameState()
        self._game_turns = 0

        if output:
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

        minimax = MiniMax(self._color)
        
        if self._game_turns > 10:
            depth = 2
        else:
            depth = 3

        while(True):
            move = minimax.minimax_value(self._state, self._color, depth,float('-inf'),float('inf'), self._game_turns)
            if move[1] is not None or move[1]!=0:
                break
            print(self._color, move)
            return random.choice(minimax.find_possible_moves(self._state, self._color))

        self._game_turns+=1
        return move[1]

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        self._state.apply_action(action, self.color2char(color))
        self._game_turns += 1

        if output:
            match action:
                case SpawnAction(cell):
                    print(f"Testing: {color} SPAWN at {cell}")
                    pass
                case SpreadAction(cell, direction):
                    print(f"Testing: {color} SPREAD from {cell}, {direction}")
                    pass

    def color2char(self, color):
        if color == PlayerColor.BLUE: return 'b'
        if color == PlayerColor.RED: return 'r'

class RandomAgent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        self._state = GameState()
        self._game_turns = 0

        if output:
            match color:
                case PlayerColor.RED:
                    print(f"Testing: I am playing as red {self._color}")
                case PlayerColor.BLUE:
                    print(f"Testing: I am playing as blue {self._color}")

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        if self._game_turns == 0:
            return SpawnAction(HexPos(3, 3)) # doesn't matter where we spawn, every pos is the same

        minimax = MiniMax(self._color)

        moves = minimax.find_possible_moves(self._state, self._color)
        return random.choice(moves)

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        self._state.apply_action(action, self.color2char(color))
        self._game_turns += 1
        if output:
            match action:
                case SpawnAction(cell):
                    print(f"Testing: {color} SPAWN at {cell}")
                    pass
                case SpreadAction(cell, direction):
                    print(f"Testing: {color} SPREAD from {cell}, {direction}")
                    pass

    def color2char(self, color):
        if color == PlayerColor.BLUE: return 'b'
        if color == PlayerColor.RED: return 'r'