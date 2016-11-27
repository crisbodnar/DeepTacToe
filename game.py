from random import randint

class Game:

	def __init__(self, no_of_rows, no_of_columns, winning_length):
		"""
		
		The game will be played on a board with dimensions no_of_rows * no_of_columns

		The players will need to complete winning_length signs in a row on either a row, 
		column or diagonal in order to win. winning_length should be less than or equal
		to the minimum of no_of_rows and no_of_columns
		
		"""	
		if not isinstance(no_of_rows, int):
			raise TypeError("no_of_rows must be an int")
		if not isinstance(no_of_columns, int):
			raise TypeError("no_of_columns must be an int")
		if not isinstance(winning_length, int):
			raise TypeError("winning_length must be an int")
		if not winning_length <= min_between(no_of_rows, no_of_columns):
			raise TypeError("winning_length must be lower than or equal to no_of_rows and no_of_columns")

		#initialize the sizes with the given parameters
		self.no_of_rows = no_of_rows
		self.no_of_columns = no_of_columns
		self.winning_length = winning_length
		#Initialize a board of the given size
		self.board = initialize_board(no_of_rows, no_of_columns)
		#encode the states as base 3 values
		self.powers_of_3 = initialize_powers_of_3(no_of_rows * no_of_columns)


	def get_number_of_rows(self):
		return self.no_of_rows

	def get_number_of_columns(self):
		return self.no_of_columns

	def get_winning_length(self):
		return self.winning_length

	def get_board(self):
		return board

	def get_visited(self):
		return visited

	def get_powers_of_3(self):
		return powers_of_3

	def print_board(self):
		for i in range(self.no_of_rows):
			for j in range(self.no_of_columns):
				print(self.board[i][j], end = '')
			print()

	def print_powers_of_3(self):
		for i in range(self.no_of_rows * self.no_of_columns):
			print(self.powers_of_3[i])

	def print_benefit(self):
		for i in range(100):
			print(self.benefit[i])

	# choose a random position to start
	def start_game(self):
		#initialize the arrays
		#benefit is high if the configuration is good for player 1
		#and low if the configuration is good for player 2
		self.benefit = [0 for x in range(100000)]
		#visited is one if the configuration has been computed
		self.visited = [0 for x in range(100000)]

		play_game(self, 1, 0)

	#respond to server request
	def choose_next_move(self, config_array):
		current_state = matrix_from_array(config_array)
		configuration = configuration_from_array(config_array)
		best_configuration = 19682
		best_value = 10

		for i in range(3):
			for j in range(3):
				if (current_state[i][j] == 0):
					new_configuration = configuration + 2 * self.powers_of_3[i * 3 + j]
					print(self.benefit[new_configuration])
					if (self.benefit[new_configuration] <= best_value):
						best_configuration = new_configuration
						best_value = self.benefit[new_configuration]
		return best_configuration
		

def matrix_from_array(config_array):
	Matrix = [[0 for x in range(3)] for y in range(3)]
	array_index = 0
	for i in range(3):
		for j in range(3):
			Matrix[i][j] = config_array[array_index]
			array_index += 1
			print(Matrix[i][j], end = "")
		print()
	print()
	return Matrix

def configuration_from_array(config_array):
	configuration = 0
	pow_of_3 = 1
	for i in range(9):
		configuration = configuration + config_array[i] * pow_of_3
		pow_of_3 *= 3
	return configuration

def matrix_from_configuration(configuration):
	Matrix = [[0 for x in range(3)] for y in range(3)]
	for i in range(3):
		for j in range(3):
			Matrix[i][j] = configuration % 3
			configuration = configuration // 3
			print(Matrix[i][j], end = "")
		print()
	return Matrix


def min_between(a, b):
	if a < b:
		return a
	else:
		return b

def max_between(a, b):
	if a > b:
		return a
	else:
		return b

def initialize_board(no_of_rows, no_of_columns): 
	Matrix = [[0 for x in range(no_of_columns)] for y in range(no_of_rows)]
	return Matrix

def initialize_powers_of_3(maximum):
	pow3 = [0 for x in range(maximum)]
	pow3[0] = 1
	for i in range(1, maximum):
		pow3[i] = pow3[i-1] * 3
	return pow3

#fill the benefit array
def play_game(current_game, move, configuration):	
	current_game.visited[configuration] = 1

	if (detect_player(move) == 1):
		current_game.benefit[configuration] = -1
	else:
		current_game.benefit[configuration] = 1

	if is_end_of_game(current_game):
		return

	if (move == 10):
		current_game.benefit[configuration] = 0 #equality
		return

	#go through all states which derive from the current one
	#and update the value of benefit
	for i in range(current_game.no_of_rows):
		for j in range(current_game.no_of_columns):
			if (current_game.board[i][j] == 0):
				if (detect_player(move) == 1):
					current_game.board[i][j] = 1
					new_configuration = configuration + current_game.powers_of_3[i * 3 + j]
					if current_game.visited[new_configuration] == 0:
						play_game(current_game, move + 1, new_configuration)
					#maximize the result
					current_game.benefit[configuration] = max_between(current_game.benefit[configuration], current_game.benefit[new_configuration])
					current_game.board[i][j] = 0
				else:
					current_game.board[i][j] = 2
					new_configuration = configuration + 2 * current_game.powers_of_3[i * 3 + j]
					if current_game.visited[new_configuration] == 0:
						play_game(current_game, move + 1, new_configuration)
					#minimize the result
					current_game.benefit[configuration] = min_between(current_game.benefit[configuration], current_game.benefit[new_configuration])
					current_game.board[i][j] = 0

def detect_player(move):
	if move % 2 == 1:
		return 1
	else:
		return 2

def is_end_of_game(current_game):
	#works for 3*3 board

	if (current_game.board[0][0] == 1 and current_game.board[1][1] == 1 and current_game.board[2][2] == 1):
		return True
	if (current_game.board[2][0] == 1 and current_game.board[1][1] == 1 and current_game.board[0][2] == 1):
		return True
	if (current_game.board[0][0] == 2 and current_game.board[1][1] == 2 and current_game.board[2][2] == 2):
		return True
	if (current_game.board[2][0] == 2 and current_game.board[1][1] == 2 and current_game.board[0][2] == 2):
		return True

	for i in range(3):
		if(current_game.board[i][0] == 1 and current_game.board[i][1] == 1 and current_game.board[i][2] == 1):
			return True
		if(current_game.board[0][i] == 1 and current_game.board[1][i] == 1 and current_game.board[2][i] == 1): 
			return True
		if(current_game.board[i][0] == 2 and current_game.board[i][1] == 2 and current_game.board[i][2] == 2): 
			return True
		if(current_game.board[0][i] == 2 and current_game.board[1][i] == 2 and current_game.board[2][i] == 2): 
			return True

	return False


c1 = Game(3, 3, 3)
c1.start_game()

"""
matrix_from_configuration(c1.choose_next_move([1, 2, 0,
											   1, 0, 0, 
											   0, 0, 0]))
print()

matrix_from_configuration(c1.choose_next_move([1, 2, 1,
											   1, 2, 0, 
											   0, 0, 0]))
print()
matrix_from_configuration(c1.choose_next_move([1, 0, 2,
											   0, 0, 0, 
											   1, 1, 2]))
print()
matrix_from_configuration(c1.choose_next_move([1, 0, 2,
											   0, 1, 0, 
											   0, 1, 2]))
"""