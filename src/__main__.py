import MinesweeperCLI as ms
import asyncio

def printList(list):
    for row in list:
        print(row)

board: ms.Board = ms.Board(4, 3, 1)
board.initGame()
# board.inputReciever(0,0)
from Renderer import root

async def main():
    print(board.dataBoard)
    await asyncio.sleep(0)  # Allow other tasks to run
    root.mainloop()

asyncio.run(main())
