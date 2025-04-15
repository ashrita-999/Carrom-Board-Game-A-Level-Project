import tkinter
from tkinter.ttk import *
from PIL import ImageTk, Image

from Rules import Rules

from NewGame import NewGame

from LoadGame import LoadGame

from Leaderboard import Leaderboard



class GameWindow:
    def __init__(self, database, game):

        # creating an attribute with the database
        self.database = database
        self.game = game
        self.window = tkinter.Tk()

    def show_main_window(self):
        self.window.title("Carrom Board")

        # initialise tkinter window with dimensions
        self.window.geometry("1920x1080")

        # window colour
        self.window['background'] = '#E88C60'


        # initialising the grid
        self.window.columnconfigure(0, weight=1, minsize=100) # weight=1 for dynamic cells, minsize for minimum size of cell
        self.window.columnconfigure(1, weight=1, minsize=100) # weight=1 for dynamic cells, minsize for minimum size of cell
        s = Style()
        s.configure('My.TFrame', background='#E88C60')
        for i in range(6):
            self.window.rowconfigure(i, weight=1, minsize=100)
            for j in range(2):
                frame = tkinter.Frame(
                    master=self.window,
                    relief=tkinter.RAISED,
                    borderwidth=1


                )
                frame.grid(row=i, column=j)  # allows every 'frame' to be attached to the window


        # creating buttons
        btn_rules = tkinter.Button(self.window, text="Rules", width=100, command=self.rules, highlightbackground='#E88C60') #when clicked, opens Rules
        btn_loadgame = tkinter.Button(self.window, text="Load Game", width=100, command=self.loadgame, highlightbackground='#E88C60')
        btn_newgame = tkinter.Button(self.window, text="New Game", width=100, command=self.newgame, highlightbackground='#E88C60')
        btn_leaderboard = tkinter.Button(self.window, text="Leaderboard", width=100, command=self.leaderboard, highlightbackground='#E88C60')

        # positioning buttons
        btn_rules.grid(row=2, column=0, pady=40, sticky="ns")
        btn_loadgame.grid(row=3, column=0, pady=40, sticky="ns")
        btn_newgame.grid(row=4, column=0, pady=40, sticky="ns")
        btn_leaderboard.grid(row=5, column=0, pady=40, sticky="ns")


        # carrom image
        img_raw = Image.open("/Users/ashri/IdeaProjects/game/src/assets/vector-carrom-board.png")
        img_dims = img_raw.resize((500, 500))  # resize the image
        carrom_img = ImageTk.PhotoImage(img_dims)
        my_label = tkinter.Label(image=carrom_img, bg='#E88C60')
        my_label.grid(row=1, column=1, pady=2, rowspan=4, sticky="nsew" )

        # creating the title
        lbl_title = tkinter.Label(master=self.window, text="Play Carrom!", font=("Marker Felt", 80, "bold"), highlightthickness=0,
                                  bg='#E88C60', fg='#481B05')
        # positioning the title
        lbl_title.grid(row=0, column=0, columnspan=2)
        self.window.mainloop()


# methods for opening windows when buttons are clicked
    def rules(self):
        self.rules = Rules()

    def newgame(self):
        self.new_game = NewGame(self.database, self)

    def loadgame(self):
        self.new_game = LoadGame(self.database, self)

    def leaderboard(self):
        self.leaderboard = Leaderboard(self.database, self)
