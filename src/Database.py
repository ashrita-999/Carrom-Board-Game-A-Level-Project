import json
import sqlite3


class Database:
    def __init__(self):
        #creating a connection
        self.conn = sqlite3.connect('carrom-board-db')

    def create_user(self, user_name):
        #creating a user
        self.conn.execute("INSERT INTO user (user_id, user_name,score) \
                           VALUES (?, ?)", (user_name, 0 ))
        self.conn.commit()

    def create_game(self, game_name, no_of_players, striker_color, game_difficulty, player_names):
        # Insert into game table
        cursor = self.conn.execute("INSERT INTO game (game_name, no_of_players, striker_color, difficulty ) \
                           VALUES (?, ?, ?, ?)", (game_name , no_of_players, striker_color, game_difficulty ))
        # get game record primary key (game_id)
        game_id = cursor.lastrowid
        # Loop through users to create user record and game user record
        for user in player_names:
            # Select user using user_name
            cursor = self.conn.execute("select * from user where user_name = '" + user + "'")
            records = cursor.fetchall()
            print(records)

            # Check if the user already exists
            if len(records) == 0:
                # If user not exists then insert into user table
                cursor = self.conn.execute("INSERT INTO user (user_name,score) \
                           VALUES ( '" + user + "', 0 )")
                user_id = cursor.lastrowid
            else:
                # If user exists then get user_id
                user_id = records[0][0]

            # Insert into game_user table for each user
            self.conn.execute("INSERT INTO game_user (game_id, user_id ) \
                               VALUES (" + str(game_id) + ", " + str(user_id) + ") ")

        self.conn.commit()
        return game_id

    def save_game(self, game):
        # Update game table with game details
        self.conn.execute("update game set game_details = ? where game_id = ?", (json.dumps(game),
                                                                                 game["game_properties"]["game_id"]))
        self.conn.commit()
        self.save_user_score(game["game_properties"]["players"][0])
        self.save_user_score(game["game_properties"]["players"][1])
        if game["game_properties"]["no_of_players"] == 4:
            self.save_user_score(game["game_properties"]["players"][2])
            self.save_user_score(game["game_properties"]["players"][3])

    def save_user_score(self, user):
        #saves user score to database if score in game_properties more than score already in database
        cursor = self.conn.execute("select score from user where user_name = ?", (user["name"],))
        records = cursor.fetchone()
        if not user["score"] == "":
            if records[0] < user["score"]:
                self.conn.execute("update user set score = ? where user_name = ?", (user["score"], user["name"]))

        self.conn.commit()

    def get_game_names(self):
        cursor = self.conn.execute("select game_id, game_name from game where game_details is not null")
        return cursor.fetchall()

    def get_user_names(self):
        cursor = self.conn.execute("select user_name from user ")
        return cursor.fetchall()

    def get_game_data(self, game_id):
        cursor = self.conn.execute("select game_details from game where game_id = ?", (game_id,))
        data = cursor.fetchone()
        return data[0]

    def get_leader_board(self):
        #gets top 10 players and their scores in descending order
        cursor = self.conn.execute("select user_name, score from user order by score desc  limit 10")
        return cursor.fetchall()
