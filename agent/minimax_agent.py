# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent
import random

from agent.minimax_yoav import minimax, generate_valid_spawn_actions
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction
from agent.OurBoard import OurBoard


class MiniMaxAgent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        self.board = OurBoard()
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")

        self.target_minimax_depth = 3

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take. Runs minimax to find the best action.
        """
        if self.board._color_power(self._color) == 0:
            return random.choice(generate_valid_spawn_actions(self.board))

        if self.board.game_over:
            print('Game is already over!')
            return None

        _, best_action = minimax(
            self.board,
            0,
            self.target_minimax_depth,
            self._color,
            True,
            float('-inf'),
            float('inf')
        )

        print(best_action)

        return best_action

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                self.board.apply_action(action)
                pass
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                self.board.apply_action(action)
                pass
