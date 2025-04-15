
class GameFunctions():
    def __init__(self, current_player, noofplayers, team_1_points, team_2_points, current_player_colour, current_team_points,
                 player_1_points, player_2_points, player_3_points, player_4_points, sliderpos, sliderforce,
                 directionslider, StrikerCoin, Gobutton,
                 game_properties, button_dimensions, circle_base_dims, CoinsMoving, space):
        self.space = space
        self.game_properties = game_properties
        self.button_dimensions = button_dimensions
        self.circle_base_dims = circle_base_dims
        self.CoinsMoving = CoinsMoving
        self.current_player = current_player # the player that has just struck
        self.noofplayers = noofplayers # total number of players
        self.team_1_points = team_1_points # points for team 1
        self.team_2_points = team_2_points # points for team 2
        self.current_player_colour = current_player_colour # coin colour of current player
        self.current_team_points = current_team_points # number of points for current team after most recent strike (holds temporary values)
        # player points below: total points for each individual player (only used when 4 players)
        self.player_1_points = player_1_points
        self.player_2_points = player_2_points
        self.player_3_points = player_3_points
        self.player_4_points = player_4_points
        self.sliderpos = sliderpos #position slider
        self.sliderforce = sliderforce #force slider
        self.directionslider = directionslider #circular direction slider
        self.StrikerCoin = StrikerCoin #striker
        self.Gobutton = Gobutton # button to strike
        self.red_hit = False # if a red coin has been hit or not
        self.noofcoinsonboard = 18 #total number of coins on board

    def player_change(self, current_player):
        self.current_player = current_player
        if self.noofplayers == 2 : # if there are 2 players
            if self.current_player == 1 : #if current player is 1 (bottommost)
                self.player_1_points = self.player_1_points + self.current_team_points
                self.team_1_points = self.team_1_points + self.current_team_points
                #^team 1 points increases by total number of points won after most recent strike
                self.current_player = 3 # current player goes to topmost player
                self.current_player_colour = "White" #current player colour is white
                self.current_team_points = 0 # current team points set to 0
            elif self.current_player ==3 : # if current player is 3 (topmost)
                self.player_2_points = self.player_2_points + self.current_team_points
                self.team_2_points = self.team_2_points + self.current_team_points
                #^team 2 points increases by total number of points won after most recent strike
                self.current_team_points = 0 # current team points set to 0
                self.current_player = 1 # current player goes to bottommost player
                self.current_player_colour = "Black"
            elif current_player == 0:
                self.current_player = 1
                self.current_team_points = 0
                self.current_player_colour = 'Black'

        #players alternate in a clockwise manner
        if self.noofplayers == 4:
            if self.current_player == 1 :
                self.team_1_points = self.team_1_points + self.current_team_points
                self.player_1_points = self.player_1_points + self.current_team_points
                self.current_team_points = 0
                self.current_player = 2
                self.current_player_colour = 'White'
            elif self.current_player == 2 :
                self.team_2_points = self.team_2_points + self.current_team_points
                self.player_2_points = self.player_2_points + self.current_team_points
                self.current_team_points = 0
                self.current_player = 3
                self.current_player_colour = 'Black'
            elif self.current_player == 3:
                self.team_1_points = self.team_1_points + self.current_team_points
                self.player_3_points = self.player_3_points + self.current_team_points
                self.current_team_points = 0
                self.current_player = 4
                self.current_player_colour = 'White'
            elif self.current_player == 4:
                self.team_2_points = self.team_2_points + self.current_team_points
                self.player_4_points = self.player_4_points + self.current_team_points
                self.current_team_points = 0
                self.current_player = 1
                self.current_player_colour = 'Black'
            elif current_player == 0:
                self.current_player = 1
                self.current_team_points = 0
                self.current_player_colour = 'Black'
        print(self.team_1_points, self.team_2_points)
        return(self.current_player)

    def perform_coin_in_hole(self, coins):
        for i in range (0, 19): #iterates through all coins on the board
            if coins[i].if_holed() == True and coins[i].get_holed() == False:
                #^checks if the coin is holed and not already removed
                coins[i].set_holed(True) #coin's holed attribute set to true
                coins[i].set_holed_temp(True)
                coins[i].remove(self.space) #coin removed from the board

    def end_round(self, coins):
        count1 = 0
        count2 = 0
        bool = False


        for i in range (0,9):
            if coins[i].get_holed() == True:
                count1 = count1 + 1
        for i in range(9,18):
            if coins[i].get_holed() == True:
                count2 = count2 + 1

        #if all white coins holed
        if count1 == 9:

            #team with higher points have other team's points added on
            if self.team_2_points > self.team_1_points:
                self.team_2_points = self.team_2_points + self.team_1_points
            elif self.team_1_points > self.team_2_points:
                self.team_1_points = self.team_1_points + self.team_2_points

            #resets coins
            for i in range(0,19):
                if coins[i].get_holed() == True:
                    coins[i].set_holed(False)
                    coins[i].set_holed_temp(False)
                    coins[i].resetPosition(self.game_properties[i][0], self.game_properties[i][1], self.space)
                else:
                    coins[i].remove(self.space)
                    coins[i].resetPosition(self.game_properties[i][0], self.game_properties[i][1], self.space)
                    coins[i].set_holed(False)
                    coins[i].set_holed_temp(False)

        #if all white coins holed
        if count2 == 9:

            #team with higher points have other team's points added on
            if self.team_2_points > self.team_1_points:
                self.team_2_points = self.team_2_points + self.team_1_points
            elif self.team_1_points > self.team_2_points:
                self.team_1_points = self.team_1_points + self.team_2_points

            #resets coins
            for i in range(0,19):
                if coins[i].get_holed() == True:
                    coins[i].set_holed(False)
                    coins[i].set_holed_temp(False)
                    coins[i].resetPosition(self.game_properties[i][0], self.game_properties[i][1], self.space)
                else:
                    coins[i].remove(self.space)
                    coins[i].resetPosition(self.game_properties[i][0], self.game_properties[i][1], self.space)
                    coins[i].set_holed(False)
                    coins[i].set_holed_temp(False)

    def end_game(self):

        #outputs different numbers based on who won the game, 0 if game hasn't ended
        output = 0
        if self.noofplayers == 4:
            if self.team_1_points == 29 or self.team_1_points > 29:
                output = 1
            elif self.team_2_points == 29 or self.team_2_points > 29:
                output = 2
        else:
            if self.team_1_points == 29 or self.team_1_points > 29:
                output = 3
            elif self.team_2_points == 29 or self.team_2_points > 29:
                output = 4
        return(output)


    def holed_check(self, coins, current_player):
        redcoins = 0 # number of red coins holed
        mycoins = 0 #number of current player coins holed
        othercoins = 0 # number of other team coins holed
        change_player = False # change player originally false
        self.current_player = current_player
        for i in range(0,19): # iterates through all 19 coins on board
            if self.red_hit == False: # if the red coin hasn't been holed in previous turn
                if coins[i].get_holed_temp() == True and coins[i].getColour() == self.current_player_colour:
                    # ^(for each coin) if coin has been holed and is the current player's colour
                    mycoins = mycoins + 1 # mycoins increases by 1
                    coins[i].set_holed_temp(False)
                elif coins[i].get_holed_temp() == True and coins[i].getColour() != self.current_player_colour and coins[i].getColour() != 'Red':
                    # ^ else if holed coin is not current player's coin and not red
                    othercoins = othercoins + 1 # othercoins increases by 1
                    coins[i].resetPosition(self.game_properties[i][0], self.game_properties[i][1], self.space) #coin is placed back on board
                    coins[i].set_holed(False) #holed property of coin set to false
                    coins[i].set_holed_temp(False)
                elif coins[i].getColour() == 'Red' and coins[i].get_holed_temp() == True: #else if red coin has been holed
                    redcoins = redcoins + 1 # redcoins increases by 1
                    coins[i].set_holed_temp(False)
            else: #else if the red coin had been holed in the previous turn
                if coins[i].get_holed_temp() == True and coins[i].getColour() == self.current_player_colour:
                    #^ if the holed coin is current player's colour
                    mycoins = mycoins + 1 # mycoins increases by 1
                    coins[i].set_holed_temp(False)
                elif coins[i].get_holed_temp() == True and coins[i].getColour() != self.current_player_colour and coins[i].getColour() != 'Red':
                    #^ else if holed coin is not current player's coin and not red
                    othercoins = othercoins + 1 #othercoins increases by 1
                    coins[i].resetPosition(self.game_properties[i][0], self.game_properties[i][1], self.space) #coin is placed back on board
                    coins[i].set_holed(False) #holed property of coin set to false
                    coins[i].set_holed_temp(False)
        if self.red_hit == False: #if red coin not holed in previous turn
            if redcoins > 0: #if red coin holed in this turn
                if mycoins >0: #if red coin and player's colour coin holed in this turn
                    self.current_team_points = self.current_team_points + 5 # player's points increase by 5
                    self.noofcoinsonboard = self.noofcoinsonboard - 1 - mycoins #number of coins on board decreases by number of coins holed
                    change_player = True # change player is true
                elif othercoins > 0: # else if red coin holed and other player's colour coin holed
                    coins[18].set_holed(False)
                    coins[18].set_holed_temp(False)
                    coins[18].resetPosition(self.game_properties[18][0], self.game_properties[18][1], self.space) #red coin placed back in the middle of the board
                    change_player = True # change player is true
                elif mycoins == 0 and othercoins == 0: #else if red coin holed and no other coins holed
                    change_player = False #change player false (current player gets another turn)
                    self.red_hit = True #self.red_hit set to true
            else: #else if red coin hasn't been holed this turn
                if mycoins >0: # if current player's coins holed
                    self.current_team_points = self.current_team_points + mycoins #current player's points increase by number of coins holed
                    change_player = False # player gets another turn
                    self.noofcoinsonboard = self.noofcoinsonboard - mycoins # number of coins on board decreased by number of coins holed
                elif othercoins > 0: # else if other player's coins holed
                    change_player = True #player changes
                elif othercoins == 0 and mycoins == 0: #if no coins have been holed
                    change_player = True # player changes
        else: # if red coin holed in previous turn
            if mycoins > 0: # if player's coin holed in this turn
                self.red_hit = False # self.red_hit set to false
                change_player = True # player changes
                self.current_team_points = self.current_team_points + 5 #player's points increase by 5
                self.noofcoinsonboard = self.noofcoinsonboard - 1 - mycoins #number of coins on board decreases by number of coins holed
            elif othercoins > 0: # if other player's coin holed in this turn
                self.red_hit = False #self.red_hit set to false
                change_player = True #player changes
                coins[18].set_holed(False)
                coins[18].set_holed_temp(False)
                coins[18].resetPosition(self.game_properties[18][0], self.game_properties[18][1], self.space) # red coin placed back on board
            elif mycoins == 0 and othercoins == 0: # if no coins have been holed
                self.red_hit = False #self.red_hit set to false
                change_player = True #player changes
                coins[18].set_holed(False)
                coins[18].set_holed_temp(False)
                coins[18].resetPosition(self.game_properties[18][0], self.game_properties[18][1], self.space) # red coin placed back on board

        return change_player #returns true if player changes, false if player stays the same



    def player_strike(self,  current_player, coins, strikercoin):
        self.sliderpos.move() #moves the position slider to where the mouse clicked
        self.sliderforce.move() #moves force slider to where the mouse clicked
        self.directionslider.move() #moves direction slider to where the mouse clicked
        self.current_player = current_player #self.current player = current player passed in
        # self.team_1_points = 9
        if self.CoinsMoving(coins, strikercoin ) == False: # if no coins are moving on the board
            self.StrikerCoin.changePos(self.sliderpos, self.current_player) # moves the striker coin to spcified position
        if self.Gobutton.CheckClicked(self.button_dimensions) == ('True') and self.CoinsMoving(coins, strikercoin ) == False :
            #^ if the strike button is clicked and no coins are moving
            self.StrikerCoin.moveStriker(self.sliderforce, self.directionslider, self.circle_base_dims) #striker is struck

    def get_player_1_points(self):
        return self.player_1_points
    def get_player_2_points(self):
        return self.player_2_points
    def get_player_3_points(self):
        return self.player_3_points
    def get_player_4_points(self):
        return self.player_4_points