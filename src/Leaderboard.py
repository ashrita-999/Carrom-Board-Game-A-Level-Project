import tkinter
from src.Database import Database

class Leaderboard():
    def __init__(self,database: Database, master=None):
        # create window object
        self.window = tkinter.Tk()
        self.user_scores =  database.get_leader_board() # contains tuple of usernames and their scores

        # initialise tkinter window with dimensions
        self.window.geometry("720x600")
        self.window.title("Leaderboard")

        # initialising the grid
        self.window.columnconfigure(0, weight=1, minsize=100)
        self.window.columnconfigure(1, weight=1, minsize=100)
        # code for creating table
        total_rows = len(self.user_scores)
        total_columns = len(self.user_scores[0])

        # Adding titles
        self.e = tkinter.Entry(self.window, width=30, fg='blue',
                               font=('Arial',16,'bold'))
        self.e.grid(row=0, column=0)
        self.e.insert(tkinter.END, "Name")
        # self.disable_entry(self.e)


        self.e = tkinter.Entry(self.window, width=30, fg='blue',
                               font=('Arial',16,'bold'))
        self.e.grid(row=0, column=1)
        self.e.insert(tkinter.END, "Score")
        # self.disable_entry(self.e)

        # Displaying usernames and scores
        for i in range(0, total_rows):
            for j in range(0, total_columns):

                self.e = tkinter.Entry(self.window, width=30, fg='red',
                               font=('Arial',16,'bold'))
                self.e.grid(row=i+1, column=j)
                self.e.insert(tkinter.END, self.user_scores[i][j])
                # self.disable_entry(self.e)


    # def disable_entry(self, entry):
    #     entry.config(state="disabled")


