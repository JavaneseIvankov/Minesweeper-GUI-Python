from os import stat
import customtkinter as ctk
import Controller as ctrl
from pathlib import Path
from PIL import Image

class Refs:
    cellSize = 30

    @staticmethod
    def imgWrapper(path, cellSize):
        img = Image.open(path)
        return ctk.CTkImage(light_image=img, dark_image=img, size=(cellSize, cellSize))

    buttonRef = {}

    ROOT_DIR = Path(__file__).parent.parent

    THEME_PATH = f"{ROOT_DIR}/assets/color_theme.json"

    imgDefault = imgWrapper(f"{ROOT_DIR}/assets/default.png", cellSize)
    img0 = imgWrapper(f"{ROOT_DIR}/assets/empty0.png", cellSize)
    img1 = imgWrapper(f"{ROOT_DIR}/assets/empty1.png", cellSize)
    img2 = imgWrapper(f"{ROOT_DIR}/assets/empty2.png", cellSize)
    img3 = imgWrapper(f"{ROOT_DIR}/assets/empty3.png", cellSize)
    img4 = imgWrapper(f"{ROOT_DIR}/assets/empty4.png", cellSize)
    img5 = imgWrapper(f"{ROOT_DIR}/assets/empty5.png", cellSize)
    img6 = imgWrapper(f"{ROOT_DIR}/assets/empty6.png", cellSize)
    img7 = imgWrapper(f"{ROOT_DIR}/assets/empty7.png", cellSize)
    img8 = imgWrapper(f"{ROOT_DIR}/assets/empty8.png", cellSize)
    imgMine = imgWrapper(f"{ROOT_DIR}/assets/mine.png", cellSize)

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

class fullFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        ctk.CTkFrame.__init__(*args, **kwargs)
        self.pack(fill='both', expand=True)


class App(ctk.CTk):
    instance = None

    @classmethod
    def accessInstance(cls):
        return cls.instance

    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        ve = 1000
        ho = 1000
        self.geometry(f"{ve}x{ho}")
        self.frames = {}
        self.__class__.instance = self

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme(Refs.THEME_PATH)

        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)

        for F in (Menu, RunningGame, Blank, Dialogue):
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=1, relheight=1)

        self.showFrame(Menu)

    def showFrame(self, page):
        self.reInitFrame(page)
        frame = self.frames[page]
        frame.tkraise()

    def reInitFrame(self, page):
        if page == RunningGame or page == Dialogue:
            frame = self.frames[page]
            frame.reInit()


class Blank(ctk.CTkFrame):  # A filler frame
    def __init__(self, parent, router):
        ctk.CTkFrame.__init__(self, parent)
        self.pack(fill="both", expand=True)
        self.place(in_=parent, relx=0.5, rely=0.5, relwidth=1, relheight=1)


class PackBlank(ctk.CTkFrame):
    def __init__(self, parent, size):
        ctk.CTkFrame.__init__(self, parent)
        self.pack(fill="both", expand=True)
        self.configure(width=size, height=size, fg_color='transparent')


class Menu(ctk.CTkFrame):
    def __init__(self, parent, router: App):
        ctk.CTkFrame.__init__(self, parent)

        self.inner = ctk.CTkFrame(master=self)
        self.inner.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5, anchor='center')
        # self.innerFg = '#0000ff' # TODO: CHANGE THIS TO PROPER COLOR
        # self.inner.configure(fg_color=self.innerFg)

        self.chosen = ctk.StringVar()  #we will use 3 consecutive numbers (as String, separated by -) as a way to store chosen difficulty
        self.generateButtons(router)

    def validator(self, chosenList):
        falseReturn = (False, 0, 0, 0)

        print("chosenList: ", chosenList)
        try:
            r = int(chosenList[0])
            c = int(chosenList[1])
            m = int(chosenList[2])
        except ValueError:
            print(f"{chosenList} -----")
            return falseReturn
        for i in (r, c, m):
            if i == 0:
                return falseReturn
    
        return (True, r, c, m)

    def startGame(self, router):
        chosen = self.chosen.get()
        chosenList = chosen.split("-")   

        result = self.validator(chosenList)
        isValid = result[0]
        r = result[1]
        c = result[2]
        m = result[3]
        
        if isValid:
            print(r, c, m)

            ctrl.createBoard(r, c, m)
            router.showFrame(RunningGame)

    def generateButtons(self, router: App):  # FIX LAYOUT ERROR
        start = ctk.CTkButton(self.inner, text='start', command=lambda router=router: self.startGame(router))
        start.pack(side='bottom', pady=30)

        # spacer = ctk.CTkFrame(self, height=30, fg_color=self.innerFg, bg_color=self.innerFg)
        # spacer.pack(in_=self.inner, side='top')
        optionFrame = ctk.CTkFrame(self.inner)
        # optionFrame.configure(corner_radius=0, border_width=10)
        optionFrame.configure(fg_color='transparent')
        optionFrame.pack(in_=self.inner, pady=20, padx=20)

        DiffOptionPack(optionFrame, self.chosen, "Beginner", 9, 9, 10)
        DiffOptionPack(optionFrame, self.chosen, "Intermediate", 16, 16, 40)
        DiffOptionPack(optionFrame, self.chosen, "Expert", 30, 16, 99)
        CustomOptionPack(self.inner, self.chosen)

        errLabel = ctk.CTkLabel(self.inner, text="row, col, and mine cannot be 0")
        tipLabel = ctk.CTkLabel(self.inner, text="*Press circle button after filling entry to play with custom difficulty")
        tipLabel.pack(side='top')
        errLabel.pack(side='top')


class DiffOptionPack(ctk.CTkFrame):
    def __init__(self, parent, optionVar, title, row_count, col_count, mine_count):
        ctk.CTkFrame.__init__(self, parent)
        # self.pack(expand=True, fill='both')
        self.pack(side='top', pady=5)
        self.configure(bg_color="transparent", border_width=2)

        chosen = f"{row_count}-{col_count}-{mine_count}"
        radio = ctk.CTkRadioButton(self, text=f"",
                                   variable=optionVar, value= chosen, width=0)

        label = ctk.CTkLabel(self, text=f"{title}", anchor='w', fg_color='transparent')

        desc = ctk.CTkLabel(self, text=f"Size : {row_count}x{col_count} | Mine Amount : {mine_count}", anchor='w', fg_color='transparent', bg_color='transparent')

        radio.pack(side='left', padx=20)
        desc.pack(side='left', padx=20, pady=3)
        label.pack(side="left", padx=20, pady=3)

class CustomOptionPack(ctk.CTkFrame):
    def __init__(self, parent, optionVar):
        ctk.CTkFrame.__init__(self, parent)
        self.pack(side='top', pady=5)
        self.configure(bg_color="transparent", border_width=2)

        def inputParser(data):  # We only need to strip  '-' because it can break the formatting system.
            for k, v in data.items():
                data[k] = v.strip(" ")
                if not data[k] or "-" in data[k]:
                    data[k] = 0

        def valueSetter():
            temp = {"row": row_count.get(), "col": col_count.get(), "mine": mine_count.get()}  # Store temporarily, passing by reference
            inputParser(temp)

            chosen = f"{temp["row"]}-{temp["col"]}-{temp["mine"]}"
            optionVar.set(chosen)

        row_count = ctk.StringVar()
        col_count = ctk.StringVar()
        mine_count = ctk.StringVar()

        rowEntry = ctk.CTkEntry(self, width=60, placeholder_text="rows",
                                textvariable=row_count)
        colEntry = ctk.CTkEntry(self, width=60, placeholder_text="columns",
                                textvariable=col_count)
        mineEntry = ctk.CTkEntry(self, width=60, placeholder_text="mine",
                                textvariable=mine_count)

        btn = ctk.CTkButton(self, width=15, height=15, corner_radius=10, text="", command=valueSetter)

        btn.pack(side='left', padx=30)
        rowEntry.pack(side='left', padx=15)
        colEntry.pack(side='left', padx=15)
        mineEntry.pack(side='left', padx=15)


class RunningGame(ctk.CTkFrame):

    def __init__(self, parent, router):
        ctk.CTkFrame.__init__(self, parent)
        self.inner = ctk.CTkFrame(master=self)
        self.inner.place(relx=0.5, rely=0.5, anchor='center')
        self.router = router
        # self.configure(fg_color="#000000")

    def reInit(self): 
        self.board = ctrl.accessInstance()
        self.board.initGame()
        self.generateButtons(self.board.row_count, self.board.col_count)

    def generateButtons(self, row_count, col_count):
        for i in range(row_count):
            for j in range(col_count):
                button = ctk.CTkButton(master=self.inner, text="",
                                       width=Refs.cellSize, height=Refs.cellSize,
                                       bg_color="transparent",  image=Refs.imgDefault,
                                       command=lambda row=i, col=j: self.clickHandler(self.board, row, col),
                                       border_spacing=0,
                                       corner_radius=0)

                button.grid(row=i, column=j, padx=0, pady=0)
                button.configure(fg_color="transparent", text_color="#000000")
                Refs.buttonRef[(i, j)] = button

    def clickHandler(self, board, row, col):
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
        status = ctrl.checkGameStatus()  # REVIEW - deep/hidden dependency

        if status == 0:
            print("RUNNING")
            print(board.getRemainingCell())
            pass
        elif status == 1:
            print("LOST")
            self.router.showFrame(Dialogue)
            pass
        elif status == 2:
            print("WINNING")
            self.router.showFrame(Dialogue)

class Dialogue(ctk.CTkFrame):
    def __init__(self, parent, router):
        ctk.CTkFrame.__init__(self, parent)
        self.inner = ctk.CTkFrame(master=self)
        self.inner.place(relx=0.5, rely=0.5, anchor='center')
        self.router = router
        self.widgetQueue = set()  # Set doesn't retain order, not really a queue, but who cares? lol

    def appendQueue(self, *args):
        for w in args:
            self.widgetQueue.add(w)

    def cleanQueue(self):
        for w in self.widgetQueue:
            w.pack_forget()

    def killSignal(self):
        print("kill")
        App.accessInstance().destroy()
        pass

    def backToMenu(self):
        self.router.showFrame(Menu)

    def reInit(self):
        status = ctrl.checkGameStatus()
        if status == 1:
            self.setLayout(status)
        elif status == 2:
            self.setLayout(status)

    def setLayout(self, status):
        self.cleanQueue()
        btns = ctk.CTkFrame(master=self.inner, width=300)

        label = ctk.CTkLabel(self.inner)
        if status == 1:
            label.configure(text="You've Revealed a Mine, You Lose!")
        elif status == 2:
            label.configure(text="Congratulations, You've Won the Game!")

        retry = ctk.CTkButton(self.inner, text="Retry", command=lambda page=RunningGame: self.router.showFrame(page))
        quit = ctk.CTkButton(self.inner, text="Quit", command=self.killSignal)
        back = ctk.CTkButton(self.inner, text="Menu", command=self.backToMenu)

        label.pack(side='top', pady= 50)
        retry.pack(in_=btns, side='left', padx=10, pady=10)
        quit.pack(in_=btns, side='left', padx=10, pady=10)
        back.pack(in_=btns, side='left', padx=10, pady=10)
        btns.pack(side='top')
        
        self.appendQueue(btns, label, retry, quit)


if __name__ == "__main__":
    _app = App()
    _app.mainloop()
