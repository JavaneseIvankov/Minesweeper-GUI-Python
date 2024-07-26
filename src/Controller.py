from src.MinesweeperLogic import Board

def accessInstance() -> Board | None:
    return Board.accessInstance()

def createBoard(row_count, col_count, mine_count):
     return Board(row_count, col_count, mine_count)


def gatherOpenCell(board: Board, row, col) -> list | None:
        return board.inputReciever("reveal", row, col)

def checkGameStatus():
    if accessInstance():
        return accessInstance().gameStatus()

def resetGame():
    if accessInstance():
        return accessInstance().resetState()
