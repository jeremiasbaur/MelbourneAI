from referee.game import Board


class OurBoard(Board):
    def copy(self):
        copy_board = OurBoard(self._state.copy())
        copy_board._history = self._history.copy()
        copy_board._turn_color = self._turn_color
        return copy_board
