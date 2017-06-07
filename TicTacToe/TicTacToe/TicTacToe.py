# This code file was written using the lab example as the base

# import additional modules
import os
import random
import time

# normal AIPlayer class
class AIPlayer(object):
	# Sets of spaces needed to occupy to win
    WIN_SET = (
			    (0, 1, 2), (3, 4, 5), (6, 7, 8),
			    (0, 3, 6), (1, 4, 7), (2, 5, 8),
			    (0, 4, 8), (2, 4, 6)
			  )

	# initialize the AIPlayer object
    def __init__(self, board, sign):
		# Copy the reference to the game board to the AI memory
        self.board = board
		# Tells the AI which sign it uses
        self.sign = sign
		# Tells if this is the first move of the AI.
        self.first_turn = True

	#Have the AI observe the board and make a decision based on the current situation on the board
    def observe(self):
        board = self.board
		#Check if the opponent is about to complete a win set and complete it to either win or prevent the opponent from winning
        for row in self.WIN_SET:
            if board[row[0]] == board[row[1]] == self.sign:
                if board[row[2]] == ' ':
                    return row[2]
            elif board[row[0]] == board[row[2]] == self.sign:
                if board[row[1]] == ' ':
                    return row[1]
            elif board[row[1]] == board[row[2]] == self.sign:
                if board[row[0]] == ' ':
                    return row[0]  
            elif board[row[0]] == board[row[1]] != ' ' and board[row[0]] == board[row[1]] != self.sign:
                if board[row[2]] == ' ':
                    return row[2]
            elif board[row[0]] == board[row[2]] != ' ' and board[row[0]] == board[row[2]] != self.sign:
                if board[row[1]] == ' ':
                    return row[1]
            elif board[row[1]] == board[row[2]] != ' ' and board[row[1]] == board[row[2]] != self.sign:
                if board[row[0]] == ' ':
                    return row[0]

		# In the case that there is not set that is going to be completed, choose one square of a set that is  still possible to complete
        for row in self.WIN_SET:
            if board[row[0]] == self.sign and board[row[1]] == board[row[2]] == ' ':
                return random.choice((row[1], row[2]))
            elif board[row[1]] == self.sign and board[row[0]] == board[row[2]] == ' ':
                return random.choice((row[0], row[2]))
            elif board[row[2]] == self.sign and board[row[1]] == board[row[0]] == ' ':
                return random.choice((row[1], row[0])) 

		#Choose a random square among the remaining if the previous two conditions are both unfulfilled
        remaining_squares = list()
        for i in range(0,8):
            if board[i] == ' ':
                remaining_squares.append(i)
        return random.choice(remaining_squares)

	# Tells the AI to observe the board and the current situation then make a move
    def make_a_move(self):
		#The move in the first turn has a different strategy, in this case, it is to randomly choose of the open squares
        if self.first_turn is True:
            self.first_turn = False
            return random.randrange(9)
        else:
			#Get the AI to observe the board and return its decision
            return self.observe()
        
class HardAIPlayer(object):
  # Sets of spaces needed to occupy to win
    WIN_SET = (
			    (0, 1, 2), (3, 4, 5), (6, 7, 8),
			    (0, 3, 6), (1, 4, 7), (2, 5, 8),
			    (0, 4, 8), (2, 4, 6)
			  )

	# initialize the AIPlayer object
    def __init__(self, board, sign):
		# Copy the reference to the game board to the AI memory
        self.board = board
		# Tells the AI which sign it uses
        self.sign = sign
		# Tells if this is the first move of the AI.
        self.first_turn = True

	#Have the AI observe the board and make a decision based on the current situation on the board
    def observe(self):
        board = self.board
		#Check if the opponent is about to complete a win set and complete it to either win or prevent the opponent from winning
        for row in self.WIN_SET:
            if board[row[0]] == board[row[1]] == self.sign:
                if board[row[2]] == ' ':
                    return row[2]
            elif board[row[0]] == board[row[2]] == self.sign:
                if board[row[1]] == ' ':
                    return row[1]
            elif board[row[1]] == board[row[2]] == self.sign:
                if board[row[0]] == ' ':
                    return row[0]  
            elif board[row[0]] == board[row[1]] != ' ' and board[row[0]] == board[row[1]] != self.sign:
                if board[row[2]] == ' ':
                    return row[2]
            elif board[row[0]] == board[row[2]] != ' ' and board[row[0]] == board[row[2]] != self.sign:
                if board[row[1]] == ' ':
                    return row[1]
            elif board[row[1]] == board[row[2]] != ' ' and board[row[1]] == board[row[2]] != self.sign:
                if board[row[0]] == ' ':
                    return row[0]

		# In the case that there is not set that is going to be completed, choose one square of a set that is  still possible to complete
        for row in self.WIN_SET:
            if board[row[0]] == self.sign and board[row[1]] == board[row[2]] == ' ':
                return random.choice((row[1], row[2]))
            elif board[row[1]] == self.sign and board[row[0]] == board[row[2]] == ' ':
                return random.choice((row[0], row[2]))
            elif board[row[2]] == self.sign and board[row[1]] == board[row[0]] == ' ':
                return random.choice((row[1], row[0])) 

		#Choose a random square among the remaining if the previous two conditions are both unfulfilled
        remaining_squares = list()
        for i in range(0,8):
            if board[i] == ' ':
                remaining_squares.append(i)
        return random.choice(remaining_squares)
            
    # Run the algorithm for the AI to make a special decision for the first move depending on the situation on the board            
    def make_first_move(self):
        board = self.board
        for i in range(0,8):
            if board[i] != ' ' and board[i] != self.sign:
                if i != 4:
                    return 4
                else:
                    return 6

    # Tells the AI to observe the board and the current situation then make a move
    def make_a_move(self):
		#The move in the first turn has a different strategy, in this case, it is to tell the AI to run the algorithm to decide the first move
        if self.first_turn is True:
            self.first_turn = False
            return self.make_first_move()
        else:
			#Get the AI to observe the board and return its decision
            return self.observe()

# The game model class			
class TicTacToe(object):
    WIN_SET = (
			(0, 1, 2), (3, 4, 5), (6, 7, 8),
			(0, 3, 6), (1, 4, 7), (2, 5, 8),
			(0, 4, 8), (2, 4, 6)
			)
    
    HR = '-' * 40

	#Initialize the TicTacToe game object
    def __init__(self):
		# Initialize the board content, which consists of 9 blank spaces.
        self.board = [' '] * 9
		# Initialize the players dictionary with their respective signs
        self.players = {'x':'human', 'o':'AI' }
		# The move made in the current turn
        self.move = None
		# The winner of the current game
        self.winner = None
		# The message to display to the player
        self.message = ''
        #self.state_updated = False

		# Create an AI player object to join the game
        self.AI_Player_1 = HardAIPlayer(self.board, 'o')
        self.AI_Player_2 = AIPlayer(self.board, 'x')

		# Initilize the player for the current turn - set the X player to make the first move
        self.current_player = 'x'
    
	# Check the validity of the current move
    def _check_move(self):
        try:
			# Check if the move input is valid by trying to convert it to an integer value
            self.move = int(self.move)
			# check if the square chosen has been taken
            if self.board[self.move] == ' ':
                return True
            else:
                self.message = 'That position has already been taken!'
                return False
        except:
           self.message = ' >> %s is not a valid position! Must be int between 0 and 8.' % self.move
           return False
    
	# Check for the winner or whether the game result is a tie
    def _check_for_result(self):
        board = self.board
        for row in self.WIN_SET:
            if board[row[0]] == board[row[1]] == board[row[2]] != ' ':
                return board[row[0]]
        
        if ' ' not in board:
            return 'tie'

        return None
    
    # Get the human player input
    def get_human_move(self):
        result = input('[0-8] >> ')
        return result

	# Get the AI Player input
    def get_AI_move(self, AI_player):
    ##    return randrange(9)
        self.simulate_thinking_time(2.0)
        return AI_player.make_a_move()

	# Check which player is the one making the move in the current turn and get input from them accordingly
    def process_input(self):
        if self.current_player is 'x':
            self.move = self.get_AI_move(self.AI_Player_2)
            #self.move = self.get_human_move()
        if self.current_player is 'o':
            self.move = self.get_AI_move(self.AI_Player_1)

	# Update the current state of the game
    def update_model(self):
        if self._check_move():
            self.board[self.move] = self.current_player
            self.winner = self._check_for_result()
            if self.current_player is 'x':
                self.current_player = 'o'
            else:
                self.current_player = 'x'
        
	# Render the game to the console terminal
    def render_game(self):
        os.system('cls')
        board = self.board
        self.show_human_help()
        
        # Print the board information
        print ('    %s | %s | %s' % tuple(self.board[:3]))
        print ('   -----------')
        print ('    %s | %s | %s' % tuple(self.board[3:6]))
        print ('   -----------')
        print ('    %s | %s | %s' % tuple(self.board[6:])) 
        
        # Print the messages to the display
        if self.message != '':
            print (self.message)
            self.message = ''
        if self.winner is None:
            print ('The current player is: %s' % self.players[self.current_player])
        #self.state_updated = False
    
    # Display the guide for human player to know what to input 
    def show_human_help(self):
        tmp = '''
    To make a move enter a number between 0 - 8 and press enter.  
    The number corresponds to a board position as illustrated:
    
        0 | 1 | 2
        ---------
        3 | 4 | 5
        ---------
        6 | 7 | 8
        '''
        print (tmp)
        print (self.HR)
    
    # Print the result of the game to the display
    def show_game_result(self):
        #print (self.HR)
        if self.winner == 'tie':
            print ('Tie!')
        else:
            print ('%s has won!' % self.players[self.winner])
    
    def simulate_thinking_time(self, seconds):
        time.sleep(seconds)

        return None

            
if __name__ == '__main__':
    game = TicTacToe()
    # Generate a seed to create a pseudo-random number generator for when the AI needs to make random choices.
    random.seed(os.urandom(16))
    while game.winner is None:
        game.render_game()
        game.process_input()
        game.update_model()
    
    game.render_game()      
    game.show_game_result()
