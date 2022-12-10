
# Author: Michael Hrenko
# GitHub username: mhrenko
# Date: 2/24/2022
# Description: This program is a game like Battleship, where two players place
#   ships on their own 10x10 grid and take turns trying to sink the other players 
#   ships with torpedoes. 

# Game rules:
#   (1) Two players.
#   (2) Each player has a 10x10 grid.
#   (3) Each player first loads ships on their grid.
#   (4) Ships must have a minimum length of 2, fit entirely on the grid, 
#       and not overlap any other ship.
#   (5) Once the players have added all their ships, they take turns firing
#       torpedoes at each other’s grid.
#   (6) After the first torpedo is fired, no more ships can be added.
#   (7) Players alternate turns, with player one ('first') going first.
#   (8) If the players attempt misses the ship, or hits the same coordinate again, 
#       they aren't penalized, but it still counts as a turn.
#   (9) A ship is sunk when all its coordinates have been hit. 
#   (10) The first player to sink all the opponents’ ships wins. 

# Assumptions for grading/testing (per ReadMe, ED posts, teacher announcements):
#   (1) No sunk ships are removed from the board.
#   (2) All [row][column] coordinates are in the range [A-J][1-10], and A-J are uppercase.
#   (3) No torpedoes are fired before ships are added. 
#   (4) The player is always firing at the opponent's board.  

class Player:
    """ Creates a player object. Will get parameter values from the ShipGame 
        class, update them, and pass them back to the ShipGame class. These values
        include the players grid, ship locations, ship count, and sunk ship count.
    """

    def __init__(self, player):
        """ Takes player as a parameter. Initializes the player and their
            grid, ship locations, ship count, and sunk ship count. 
        """
        self._player = player

        # Initialize a list with 10 sub lists, each of length 10.
        self._grid =  [[" "] * 10 for i in range(10)]

        self._ship_locations = {}
        self._ship_count = 0
        self._sunk_ship_count = 0

    def set_grid(self, grid):
        """ Updates the grid for this player.      
            Parameters:
            (1) grid = A copy of self._grid that's been updated by the
                ShipGame class.
            Returns: n/a
            Updates: The players grid.
        """
        self._grid = grid
    
    def get_grid(self):
        """ Returns the grid for this player.
            Parameters: none
            Returns: The players grid.
            Updates: n/a
        """
        return self._grid

    def add_ship_location(self, row_index, col_index, shipLength, orientation):
        """ Adds the ships location profile to a dictionary with all other ships
            for this player. This is used by the ShipGame class to see if all the
            coordinates have been hit by torpedos.
            
            Parameters:
            (1) row_index - value of the "row" which is actually the list index after 
                transforming A, B,... to 0, 1... in the ShipGame class.
            (2) col_index - value of the "column" which is actually the index in the list
                associated with row_index. Passed by user into the ShipGame class, then to here. 
            (3) shipLength - length of the ship as passed by user into the ShipGame class, then
                to here.
            (4) orientation - orientation ('C' - column, 'R' - row), passed by user into the
                ShipGame class then passed here.
                'C' means the coordinates occupy the same column. 
                'R' means the coordinates occupy the same row.
            
            Returns: n/a
            Updates: Dictionary of ship locations.
        """
        # The key is simply the count of ships: 1, 2,...
        self._ship_locations[self._ship_count] = [row_index, col_index, shipLength, orientation]

    def get_ship_locations(self):
        """ Returns the dictionary of all ship locations for this player.
            Parameters: None
            Returns: Players ship location dictionary
            Updates: n/a
        """
        return self._ship_locations

    def add_to_ship_count(self):
        """ Increments the count of ships for this player.
            Parameters: None
            Returns: n/a
            Updates: Players ship count.
        """
        self._ship_count += 1

    def get_ship_count(self):
        """ Returns the count of ships for this player. 
            Parameters: None
            Returns: Players ship count.
            Updates: n/a 
        """
        return self._ship_count
   
    def set_sunk_ship_count(self,sunk_ship_count):
        """ Updates the count of ships that were sunk for this player. 
            Parameters:
            (1) sunk_ship_count - The total count of ships that are sunk as 
                updated by the ShipGame class.
            Returns: n/a
            Updates: Players sunk ship count.      
        """
        self._sunk_ship_count = sunk_ship_count

    def get_sunk_ship_count(self):
        """ Returns the count of ships that were sunk for this player.
            Parameters: None
            Returns: Players sunk ship count.   
            Updates: n/a
        """  
        return self._sunk_ship_count

class ShipGame:
    """ Creates a ship game object. By communicating with the Player class, updates
        each players grid, ship locations, ship count, sunk ship count, and remaining
        ship count. Manages/updates a player dictionary with each player object, the 
        current game state, and which players turn it is.
    """
    def __init__(self):
        """ Takes no parameters. Initializes a player dictionary, player objects, 
            current game state, and player turn """
        
        # Create dictionary to hold both player objects.
        self._players = {}

        # Initialize the player object (via the Player class) for the first and second player.
        # These objects are stored in the self._players dictionary.
        self._players['first'] = Player('first')
        self._players['second'] = Player('second')        
        
        # Current states: 'FIRST_WON', 'SECOND_WON', 'UNFINISHED'.
        # Initialize to 'UNFINISHED' until a player wins.
        self._current_state = 'UNFINISHED'

        # Initialize the player turn to 'first' since they will go first. 
        self._player_turn = 'first'

    def place_ship(self, player, shipLength, location, orientation):
        """ Adds a ship to the players grid. Takes as parameters the player, 
            shipLength, location, orientation. Communicates with the Player class. 

            Parameters:
            (1) player - 'first' or 'second'.
            (2) shipLength - length of the ship as passed by user.
            (3) location - [row_index][col_index] passed as a string. This is the  
                ships coordinate that's closest to A1.
            (4) orientation - orientation ('C' - column, 'R' - row), passed by user.
                'C' means the coordinates occupy the same column. 
                'R' means the coordinates occupy the same row.

            Returns:
            (1) False if the ship's length is less than 2.
            (2) False if the ship doesn't fit on the players grid. 
            (3) False if the ships would overlap any previously placed ships on that 
                player's grid. 
            (4) True if the ship was added to the grid. 
            
            Updates:
            (1) The players grid via the Player class. 
            (2) The players added ship count via the Player class. 
            (3) The players added ship location dictionary via the Player class. 

        """

        # Create a dictionary for mapping the row labels (A, B,...) to a python
        #   index value of 0,1,2,... so we can easily search and update the lists.
        row_mapping = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9}

        # The location parameter is structed as a string with [row][column] so parse 
        #   each out using indexing.
       
        # As noted above, map the column value to a python index value. 
        row_index = row_mapping[location[0]]

        # Subtract 1 since the grid count is 1, 2, ..., but the python index is 0, 1, ...
        col_index = int(location[1]) - 1

        # Create a copy of the players grid to work with. 
        grid = self._players[player].get_grid()

        # If the ship size is < 2, return False.
        if shipLength < 2:
            return False      

        # When orientation is 'C' the ship is to be added to the column,
        #   starting with the first [row][column] value then down/away from A1.
        # The column index is static. Iterate though the row indices down/away from A1.
        
        elif orientation == 'C':

            # If the ship doesn't fit on the grid's column, return False.
            if row_index + shipLength > 10:
                return False

            # Check to see if ANY coordinates of the ship's desired location overlap any previously 
            #   placed ships on the player's grid. If so, return False.
            for row in range(shipLength):
                if grid[row_index][col_index] == 'x':
                    return False
                row_index += 1
            
            # Making it this far means all coordinates in the ship’s location are available.

            # Since we changed the value of row_index when checking that the ship would fit on the 
            #   players grid, reset it to the value passed by the user for the next step.
            row_index = row_mapping[location[0]]

            # Add 'x' to the grid for each coordinate in the ship.
            for row in range(shipLength):         
                grid[row_index][col_index] = 'x'
                row_index += 1

            # Like before, reset row_index to the value passed by the user for the next step.
            row_index = row_mapping[location[0]]

            # Update these items in this player's object.
            self._players[player].set_grid(grid)
            self._players[player].add_to_ship_count()
            self._players[player].add_ship_location(row_index, col_index, shipLength, orientation)

            # The ship was successfully added.
            return True

        # When orientation is 'R' the ship is to be added to the row, starting with the first 
        #   [row][column] value then right/away from A1.
        # The row index is static. Iterate through the column indices right/away from A1.  

        elif orientation == 'R':

            # If the ship doesn't fit on the grid's row, return False.
            if col_index + shipLength > 10:
                return False

            # Check to see if ANY coordinates of the ship desired location overlap any previously 
            #   placed ships on the player's grid. If so, return False.
            for column in range(shipLength):       
                if grid[row_index][col_index] == 'x':
                    return False
                col_index += 1

            # Making it this far means all coordinates in the ships location are available.

            # Since we changed the value of col_index when checking that the ship would fit on the 
            #   players grid, reset it to the value passed by the user for the next step.            
            col_index = int(location[1]) - 1

            # Add 'x' to the grid for each coordinate in the ship.
            for column in range(shipLength):                      
                grid[row_index][col_index] = 'x'
                col_index += 1

            # Like before, reset col_index to the value passed by the user for the next step.
            col_index = int(location[1]) - 1

            # Update these items in this player's object.
            self._players[player].set_grid(grid)
            self._players[player].add_to_ship_count()       
            self._players[player].add_ship_location(row_index, col_index, shipLength, orientation)

            # The ship was successfully added.
            return True

    def update_turn(self, player):
        """ Updates the turn to the other player. 
            Parameters: player ('first','second')
            Returns: none
            Updates: player turn
        """

        if player == 'first':
            self._player_turn = 'second'
        else:
            self._player_turn = 'first'
    
    def fire_torpedo(self, player, location):
        """ Fires a torpedo as the opponents grid. If it's a hit, updates the
            coordinate on the grid to 'o'. if it's a miss, updates the coordinate 
            on the grid to '.'. Checks to see if this sinks the ship and calculates 
            if all the opponents' ships are sunk. If they are, update the game status
            to the winner.
            
            Parameters:
            (1) player ('first','second')
            (2) location - [row_index][col_index] passed as a string

            Returns:
            (1) False if it's not the player's turn.
            (2) False if a player alreay won and the game is over.
            (3) True is the shot was a hit or a miss.
            
            Updates:
            (1) The opponents grid via the Player class. 
            (2) The opponents sunk ship count via the Player class. 
            (3) Player turn.
            (4) Game status to 'FIRST_WON' or 'SECOND_WON' when applicable.
                      
        """
        # Initialize sunk_ship_count to 0 each time this runs. 
        sunk_ship_count = 0

        # If it's not this players turn, return False.
        if self._player_turn != player:
            return False

        # If a player already won, return False.
        if self._current_state in ('FIRST_WON','SECOND_WON'):
            return False

        # The player is firing at the opponent so set the opponent value to 
        #   the other player.  
        if player == 'first':
            opponent = 'second'
        else:
            opponent = 'first'

        # Same row mapping dictionary from above.
        row_mapping = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9}

        # Same column and row index assignment/mapping as above.
        row_index = row_mapping[location[0]]
        col_index = int(location[1]) - 1

        # Create a copy of the OPPONENTS grid to work with.
        grid = self._players[opponent].get_grid()

        # If the shot's a hit, update the opponents grid for this coordinate 
        # to 'o' and update the player's turn.  
        if grid[row_index][col_index] == "x":
            grid[row_index][col_index] = 'o'
            self._players[opponent].set_grid(grid)
            self.update_turn(player)

        # If the shot's was already a hit, update the player's turn.
        elif grid[row_index][col_index] == "o":
            self.update_turn(player)
            
        # The shot's a miss; update the opponents grid for this coordinate 
        # to '.' and update the player's turn. 
        else:
            grid[row_index][col_index] = '.'
            self._players[opponent].set_grid(grid)
            self.update_turn(player)
            
        # Get the location of all the opponents ships.       
        ship_locations = self._players[opponent].get_ship_locations()

        # Iterate through each ship in the opponents’ ship dictionary, checking to see
        #   if all the coordinates in the ship are 'o'. If so, increase the count
        #   of sunk ships for the opponent. 
        # Check to see if all the opponents’ ships are sunk. If so, update the game state
        #   to the player who fired the torpedo denoting that they won. 
        # Note - this only checks the opponents grid since only it had the chance to 
        #   be updated.
         
        for ship in ship_locations.values():

            row_index = ship[0]
            col_index = ship[1]
            shipLength = ship[2]
            orientation = ship[3]

            # Initialize hit count to 0 for each iteration
            hit_count = 0

        # Like above, when orientation is 'C' the ship is the column, starting with the first 
        #   [row][column] value then down/away from A1.
        # The column index is static. Iterate though the row indices down/away from A1.

            if orientation == 'C':

                for row in range(shipLength):         
                    if grid[row_index][col_index] == 'o':
                        hit_count += 1
                    row_index += 1

                # If ship is sunk, increase the sunk ship count.
                if shipLength == hit_count:
                    sunk_ship_count += 1

        # Like above, when orientation is 'R' the ship is the row, starting with the first 
        #   [row][column] value then right/away from A1.  
        # The column index is static. Iterate though the column indices right/away from A1. 
                   
            elif orientation == 'R':
                for column in range(shipLength):         
                    if grid[row_index][col_index] == 'o':
                        hit_count += 1
                    col_index += 1
                
                # If ship is sunk, increase the sunk ship count.
                if shipLength == hit_count:
                     sunk_ship_count += 1

        # Update the opponents sunk ship count.
        self._players[opponent].set_sunk_ship_count(sunk_ship_count)

        # If all the opponents ships are sunk, update the game status to the player who fired this torpedo as the winner.
        if self._players[opponent].get_ship_count() == self._players[opponent].get_sunk_ship_count():
            if player == 'first':
                self._current_state = 'FIRST_WON'
            elif player == 'second':
                self._current_state = 'SECOND_WON'              

        # The torpedo was a hit or not.
        return True

    def get_current_state(self):
        """ Returns the current game state.
            Parameters: None
            Returns: Current game state. 
            Updates: n/a        
        """
        return self._current_state

    def get_num_ships_remaining(self, player):
        """ Returns the number of ships remaining (not sunk) for a player.
            Parameters: player ('first','second')
            Returns: Number of ships remaining for a player.
            Updates: n/a           
            """
        return self._players[player].get_ship_count() - self._players[player].get_sunk_ship_count()
