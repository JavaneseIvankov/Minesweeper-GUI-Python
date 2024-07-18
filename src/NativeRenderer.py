import tkinter as tk
from PIL import Image, ImageTk
from MinesweeperCLI import Board
import Controller as ctrl
import os

root = tk.Tk()

class Refs:
    cellSize = 50

    # def imgWrapper(path, cellSize):
    #     img = Image.open(path)
    #     return ImageTk.PhotoImage(img.resize((cellSize, cellSize)))

    def getImg(master, name):

    
    def imgWrapper(master, path, cellSize):
        img_path = path
        img = Image.open(img_path)
        return ImageTk.PhotoImage(img, (cellSize, cellSize), master=)
    buttonRef = {}

    imgDefault = imgWrapper("assets/default.png", cellSize)
    img0 = imgWrapper("assets/empty0.png", cellSize)
    img1 = imgWrapper("assets/empty1.png", cellSize)
    img2 = imgWrapper("assets/empty2.png", cellSize)
    img3 = imgWrapper("assets/empty3.png", cellSize)
    img4 = imgWrapper("assets/empty4.png", cellSize)
    img5 = imgWrapper("assets/empty5.png", cellSize)
    img6 = imgWrapper("assets/empty6.png", cellSize)
    img7 = imgWrapper("assets/empty7.png", cellSize)
    img8 = imgWrapper("assets/empty8.png", cellSize)
    imgMine = imgWrapper("assets/mine.png", cellSize)

    imgRef = {"0": img0,
              "1": img1,
              "2": img2,
              "3": img3,
              "4": img4,
              "5": img5,
              "6": img6,
              "7": img7,
              "8": img8,
              "X": imgMine}

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1000x1000")

        self.frames = {}
        container = tk.Frame(self, height=1000, width=1000)
        container.pack(fill='both', expand=True)

        for F in (Menu, RunningGame, Dialogue):
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(relx=0.5, rely=0.5, anchor='center')

        self.showFrame(Menu)

    def showFrame(self, page):
        frame = self.frames[page]
        frame.tkraise()

class Menu(tk.Frame):
    def __init__(self, parent, router):
        tk.Frame.__init__(self, parent)
        self.configure(width=1000, height=1000)
        self.pack(fill='both', expand=True)
        self.chosenDiff = {"row_count": 0, "column_count": 0, "mine_count": 0}
        self.generateButtons(router)

    def generateButtons(self, router):
        start = tk.Button(self, text='start', command=lambda: router.showFrame(RunningGame))
        start.place(in_=self, relx=0.5, rely=0.5, anchor='center')

        DiffOptionTemplate(self, 0, 0, "Test", 3, 3, 1)
        DiffOptionTemplate(self, 1, 0, "Easy", 4, 4, 3)
        DiffOptionTemplate(self, 2, 0, "Medium", 5, 5, 5)

class DiffOptionTemplate(tk.Frame):
    def __init__(self, parent, posR, posC, title, row_count, col_count, mine_count):
        tk.Frame.__init__(self, parent)
        self.grid(row=posR, column=posC)
        self.configure(width=400, height=200)
        self.columnconfigure(index=0, weight=1)

        label = tk.Label(self, text=f"{title}")
        label.grid(in_=self, row=0, column=0)

        desc = tk.Label(self, text=f"Size : {row_count}x{col_count} | Mine Amount : {mine_count}")
        desc.grid(in_=self, row=1, column=0)

class RunningGame(tk.Frame):
    def __init__(self, parent, router):
        tk.Frame.__init__(self, parent)
        fm = tk.Frame()
        self.configure(background="black")

        self.board = ctrl.createBoard(4, 5, 2)
        self.board.initGame()
        self.generateButtons(self.board.row_count, self.board.col_count)

    def generateButtons(self, row_count, col_count):
        for i in range(row_count):
            for j in range(col_count):
                button = tk.Button(master=self, text="", width=Refs.cellSize, height=Refs.cellSize,
                                    bg="black", image=Refs.imgDefault,
                                    command=lambda row=i, col=j: self.clickHandler(self.board, row, col),
                                    borderwidth=0)

                button.grid(row=i, column=j, padx=0, pady=0)
                button.configure(foreground="black", text_color="#000000")
                Refs.buttonRef[(i, j)] = button

    def clickHandler(self, board: Board, row, col):
        impCell = ctrl.gatherOpenCell(board, row, col)  # impacted Cell
        for cell in impCell:
            loc = tuple(cell)
            inside = str(board.getData(loc[0], loc[1]))
            currButton = Refs.buttonRef[(loc[0], loc[1])]
            currButton.configure(image=Refs.imgRef[inside])
        print(f'impCell = {impCell}')
        print(f'displayedCount = {len(board.displayed)}')
        print(f'displayBoard = {board.displayBoard}')
        self.branch(board)

    def branch(self, board):
        status = ctrl.checkGameStatus(board)  # REVIEW - deep/hidden dependency
        if status == 0:
            print("RUNNING")
            print(board.getRemainingCell())
        elif status == 1:
            print("LOST")
        elif status == 2:
            print("WINNING")

class Dialogue(tk.Frame):
    def __init__(self, parent, router):
        tk.Frame.__init__(self, parent)
        self.router = router

if __name__ == "__main__":
    _app = App()
    _app.mainloop()