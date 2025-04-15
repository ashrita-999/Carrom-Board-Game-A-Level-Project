import tkinter
from PIL import ImageTk, Image


class Rules:
    def __init__(self, master=None):
        # create window object
        self.window = tkinter.Tk()

        # initialise tkinter window with dimensions
        self.window.geometry("720x600")

        #window title
        self.window.title("Rules")

        # initialising the grid
        self.window.columnconfigure(0, weight=1, minsize=100)
        self.window.columnconfigure(1, weight=1, minsize=100)
        for i in range(6):
            self.window.rowconfigure(i, weight=1, minsize=100)
            for j in range(2):
                frame = tkinter.Frame(
                    master=self.window,
                    relief=tkinter.RAISED,
                    borderwidth=1
                )
                frame.grid(row=i, column=j)  # allows every 'frame' to be attached to the window




        body1 = tkinter.Text(self.window, height = 600, width = 600, bg='#E88C60' )
        body1.insert(tkinter.END, "Basic Rules: There are 18 coins at the centre of the board: 9 black and 9 "
                                  "white coins. Each player takes turns shooting the striker from the baseline, "
                                  "aiming to ‘hole’ their colour coins. When a player has holed a coin, "
                                  "they get another turn to strike. To hole the red coin, a player must hole "
                                  "their own piece straight after. A red coin is worth 5 points, any other coin is "
                                  "worth 1 point. A new round starts when a team/player has holed all their coins. "
                                  "The game ends when a team/player reaches 29 points, who then wins the game. "
                                  "2-Player Game: Player 1 aims to hole black coins and Player 2 aims to hole "
                                  "white coins. When a player has holed all their coins, the round ends, and "
                                  "their score is equivalent to the number of points they have gained plus the "
                                  "points of the other player. The game restarts until a player reaches 29 points, "
                                  "at which they have won the game. 4-Player Game: Works just like a 2-player game, "
                                  "but the players are split into teams. 2 players (Players 1 and 3) try to hole black "
                                  "coins and 2 players (Players 2 and 4) aim to hole white coins. Explaining the"
                                  "components in the game:")
        body1.grid(row=0, column=0, rowspan=6, columnspan=2)

        # explain image
        img_raw = Image.open("/Users/ashri/IdeaProjects/game/src/assets/explaining-components.png")
        img_dims = img_raw.resize((500, 500))  # resize the image
        explain_img = ImageTk.PhotoImage(img_dims)
        my_label = tkinter.Label(image=explain_img, bg='#E88C60')
        my_label.grid(row=6, column=0, columnspan=2, pady=2, rowspan=4, sticky="nsew" )


