import random
from copy import deepcopy

class Utils:
    @staticmethod
    def genInitBoard(row_count, col_count, mine_count):
        #Generate Board
        dataBoard = [[0] * col_count for i in range(row_count)]

        #Generate and plant mines
        minesloc = []
        for i in range(mine_count):
            tempRow = random.randrange(row_count)
            tempCol = random.randrange (col_count)
            while [tempRow, tempCol] in minesloc:
                tempRow = random.randrange(row_count)
                tempCol = random.randrange (col_count)
            minesloc.append([tempRow, tempCol])
            dataBoard[tempRow][tempCol] = 'X'

        #Generate and plant indicators
            for x in range(-1, 2):
                for y in range(-1, 2):
                    tempIndRow = tempRow + x
                    tempIndCol = tempCol + y
                    if x == 0 and y ==0:
                        continue
                    elif (tempIndRow < 0 or tempIndRow >=row_count):
                        continue
                    elif (tempIndCol < 0 or tempIndCol >=col_count):
                        continue
                    elif dataBoard[tempIndRow][tempIndCol] == 'X':
                        continue
                    elif dataBoard[tempIndRow][tempIndCol] >= 0:
                        dataBoard[tempIndRow][tempIndCol] += 1
        return dataBoard
                        
    @staticmethod
    def equalized(origin: list, target: list, compareLoc: list[int]) -> list:
        _target = deepcopy(target)
        row = compareLoc[0]
        col = compareLoc[1]
        _target[row][col] = origin[row][col]
        return _target

class Board:
    instance = None

    @classmethod
    def accessInstance(cls):
        return cls.instance
    
    @staticmethod
    def createBoard(row_count, col_count, mine_count):
        return Board(row_count, col_count, mine_count)


    def __new__(cls, row_count, col_count, mine_count):
        # this will limit the created object to 1, but we still can overwrite obj property when creating a new one.
        if not cls.instance:
            cls.instance = super(Board, cls).__new__(cls)
        cls.instance.__init__(row_count, col_count, mine_count)
        return cls.instance

    def __init__(self, row_count, col_count, mine_count):
        self.row_count = row_count
        self.col_count = col_count
        self.mine_count = mine_count
        self.dataBoard = []
        self.displayBoard = [["."] * self.col_count for i in range(self.row_count)]
        self.displayed = []
        self.mineRevealed = False
    
    def getData(self, row, col): #Getter from self.dataBoard for given row and col
        try:
            return self.dataBoard[row][col]
        except IndexError as e:
            print(f'{row, col} is out of bounds')
            return []
        
    def getDisplay(self, row, col):
        return self.displayBoard[row][col]

    def initGame(self):
        self.resetState()
        generated = Utils.genInitBoard(self.row_count, self.col_count,  self.mine_count)
        self.dataBoard = generated

    def reveal(self, row, col, displayBuffer: list): #For revealing display board based on row and col of self.dataBoard
            newDisplay = Utils.equalized(self.dataBoard, self.displayBoard, [row,col])
            self.displayed.append([row, col])
            self.displayBoard = newDisplay
            displayBuffer.append([row, col])
            
    # def cascade(self, row, col):
    #     displayBuffer = []
    #     for x in range(-1,2):
    #         for y in range(-1,2):
    #             trow = row + x
    #             tcol = col + y
    #             if x == 0 and y == 0:
    #                 continue
    #             elif trow not in range(self.row_count) or tcol not in range(self.col_count):
    #                 continue
    #             elif [trow, tcol] in self.displayed:
    #                 continue
    #             elif self.getData(trow, tcol) == 'X':
    #                 continue
    #             elif self.getData(trow, tcol) in  range(1, 9) and self.getData not in self.displayed:
    #                 self.reveal(trow, tcol, displayBuffer)
    #             elif self.getData(trow, tcol) == 0:
    #                 self.reveal(trow, tcol, displayBuffer)
    #                 tBuffer = self.cascade(trow, tcol)
    #                 displayBuffer.extend(tBuffer)
    #         return displayBuffer
    
    def cascade(self, row, col, displayBuffer=[]): #For auto-revealing when user reveal a 0
        if not displayBuffer:
            displayBuffer = []
            displayBuffer.append([row, col])

        for x in range(-1, 2):
            for y in range(-1, 2):
                tempRow = row + x
                tempCol = col + y
                loc = [tempRow, tempCol]
                if x == 0 and y == 0:
                    continue
                elif tempRow not in range(0, self.row_count) or tempCol not in range(0, self.col_count):
                    continue
                locValue = self.getData(tempRow, tempCol)
                if loc in self.displayed or loc in displayBuffer:
                    continue
                elif locValue == 'X':
                    continue
                elif locValue in range(1, 9):
                    self.reveal(tempRow, tempCol, displayBuffer)
                elif locValue == 0:
                    self.reveal(tempRow, tempCol, displayBuffer)
                    print(f'cascading on:{loc} \n displayBuffer:{displayBuffer}')
                    self.cascade(tempRow, tempCol, displayBuffer)
        return displayBuffer
                    
    def inputReciever(self, action, row, col):
        if action == "reveal":
            return self.revealProcessor(row,col)

    def revealProcessor(self, row, col):
        displayBuffer = []
        if [row, col] in self.displayed:
            print("This cell has been revealed before")
            return displayBuffer

        elif self.getData(row, col) != 0:

            if self.getData(row, col) == 'X':
                self.displayBoard = self.dataBoard
                self.mineRevealed = True

            elif self.getData(row, col) in range(1, 9):
                self.reveal(row, col, displayBuffer)
        
        elif self.getData(row, col) == 0:
                self.reveal(row, col, displayBuffer)
                tempBuffer = self.cascade(row, col)
                displayBuffer.extend(tempBuffer)

        print(self.displayBoard)
        return displayBuffer

    def resetState(self): #for resetting board property and the game overall
        self.dataBoard = []
        self.displayBoard = [["."] * self.col_count for i in range(self.row_count)]
        self.mineRevealed = False
        self.displayed = []
        remainingCell = self.row_count * self.col_count - self.mine_count - len(self.displayed)
        return remainingCell

        
    def getRemainingCell(self): #for getting
        remainingCell = self.row_count * self.col_count - self.mine_count - len(self.displayed)
        return remainingCell
    
    def gameStatus(self):
        #code based return; 
        # 0 = game running; 1 = game over, lose; 2  = game over, win

        if self.mineRevealed:
            return 1
        if self.getRemainingCell() == 0 and not self.mineRevealed: #Winninng Conditions
            return 2
        return 0


    def cliPlay(self):
        inputRowCol = ((input("Reveal (row, col) = ")).replace(" ", "")).split(",")
        row = int(inputRowCol[0])
        col = int(inputRowCol[1])

        self.inputReciever(row, col)


if __name__ == '__main__':
    b = Board(10, 10, 3)
    print(Board.instance)
    print(b.row_count)
    # Board.createBoard(9, 10, 1)
    Board(8, 9, 1)
    print(Board.instance)
    b = Board.accesInstance()
    b.initGame()
    print(b.row_count)
    # print(Board.instance)
