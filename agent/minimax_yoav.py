# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent
from referee.game import \
    PlayerColor, SpawnAction, BOARD_N, HexPos, SpreadAction, HexDir, Action

from agent.OurBoard import OurBoard


def power_dict(board, color):
    d = {}

    for power in range(1, 7):
        d[power] = 0

    d['number_of_cells'] = 0

    for cell in board._state:
        if board[cell].player == color:
            d[board[cell].power] += 1
            d['number_of_cells'] += 1

    return d


def evaluate_board(board, maximizing_player_color):
    """
    Evaluate the board and return a score.
    """

    minimizing_player_color = PlayerColor.RED if maximizing_player_color == PlayerColor.BLUE else PlayerColor.BLUE
    total_power = board._color_power(maximizing_player_color) - board._color_power(minimizing_player_color)

    maximizing_power_dict = power_dict(board, maximizing_player_color)
    minimizing_power_dict = power_dict(board, minimizing_player_color)

    power_6_diff = maximizing_power_dict[6] - minimizing_power_dict[6]
    power_5_diff = maximizing_power_dict[5] - minimizing_power_dict[5]
    power_4_diff = maximizing_power_dict[4] - minimizing_power_dict[4]
    power_3_diff = maximizing_power_dict[3] - minimizing_power_dict[3]
    power_2_diff = maximizing_power_dict[2] - minimizing_power_dict[2]
    power_1_diff = maximizing_power_dict[1] - minimizing_power_dict[1]
    number_of_cells = maximizing_power_dict['number_of_cells'] - minimizing_power_dict['number_of_cells']

    a1 = 2
    a2 = 1.5
    a3 = 1
    a4 = 0.75
    a5 = 0.5
    a6 = 0.3
    a7 = 0.1
    a8 = 1

    return a1 * total_power + a2 * power_6_diff + a3 * power_5_diff + a4 * power_4_diff + a5 * power_3_diff + \
              a6 * power_2_diff + a7 * power_1_diff + a8 * number_of_cells



def generate_valid_spawn_actions(board) -> list[Action]:
    """
    Generate a list of valid spawn actions. Defined as all cells not currently occupied.
    """
    if board._total_power >= BOARD_N ** 2:
        return []

    all_cells = [HexPos(r, q) for q in range(BOARD_N) for r in range(BOARD_N)]
    available_cells = [cell for cell in all_cells if not board._cell_occupied(cell)]
    return [SpawnAction(cell) for cell in available_cells]


def generate_valid_spread_actions(board, player_color) -> list[Action]:
    """
    Generate a list of valid spread actions. Defined all 6 directions for every cell owned by the player.
    """
    all_cells = [HexPos(r, q) for q in range(BOARD_N) for r in range(BOARD_N)]
    colored_cells = [cell for cell in all_cells if board[cell].player == player_color]
    return [SpreadAction(cell, direction) for cell in colored_cells for direction in HexDir]


def generate_valid_child_boards(parent_board, maximizer_player_color, max_turn) -> list[(OurBoard, Action)]:
    """
    Generate a list of valid child boards.
    """

    if max_turn:
        player_color = maximizer_player_color
    else:
        player_color = PlayerColor.RED if maximizer_player_color == PlayerColor.BLUE else PlayerColor.BLUE

    spawn_actions = generate_valid_spawn_actions(parent_board)
    spread_actions = generate_valid_spread_actions(parent_board, player_color)
    actions = [*spawn_actions, *spread_actions]

    children = []
    for action in actions:
        child_board = parent_board.copy()
        child_board.apply_action(action)
        children.append((child_board, action))

    return children


def minimax(curr_board, curr_depth, target_depth, maximizing_player_color, max_turn, alpha, beta):
    """
    Minimax algorithm with alpha-beta pruning.
    """

    # If we can't explore further on or the game state is already over!
    if curr_depth == target_depth or curr_board.game_over:
        return evaluate_board(curr_board, maximizing_player_color), None

    # If we are the maximizing player
    if max_turn:
        best = float('-inf')
        best_action = None

        for child_board, child_action in generate_valid_child_boards(curr_board, maximizing_player_color, max_turn):
            child_value, _ = minimax(child_board, curr_depth + 1, target_depth, maximizing_player_color, False,
                                     alpha, beta)
            if child_value > best:
                best = child_value
                best_action = child_action

            alpha = max(alpha, best)
            if beta <= alpha:
                break

        return best, best_action

    # If we are the minimizing player
    else:
        best = float('inf')
        best_action = None

        for child_board, child_action in generate_valid_child_boards(curr_board, maximizing_player_color, max_turn):
            child_value, _ = minimax(child_board, curr_depth + 1, target_depth, maximizing_player_color, True,
                                     alpha, beta)

            if child_value < best:
                best = child_value
                best_action = child_action

            beta = min(beta, best)
            if beta <= alpha:
                break

        return best, best_action
