from MinesweeperCLI import Board

def accessInstance() -> Board:
    return Board.accessInstance()

def createBoard(row_count, col_count, mine_count):
     return Board(row_count, col_count, mine_count)


def gatherOpenCell(board: Board, row, col) -> list:  # Is it necessary to injenct the board here?
        return board.inputReciever("reveal", row, col)

def checkGameStatus():
    return accessInstance().gameStatus()

def resetGame():
    return accessInstance().resetState()
