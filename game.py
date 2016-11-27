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
				print(self.board[i][j], end='')
			print()

	def print_powers_of_3(self):
		for i in range(self.no_of_rows * self.no_of_columns):
			print(self.powers_of_3[i])

	def print_benefit(self):
		for i in range(100):
			print(self.benefit[i])

	def start_game(self):
		row = randint(0, self.no_of_rows - 1)
		column = randint(0, self.no_of_columns - 1)
		self.board[row][column] = 1

		self.benefit = [0 for x in range(100000000)]
		self.visited = [0 for x in range(100000000)]

		#self.powers_of_3[row * self.no_of_columns + column] is the current configuration
		play_game(self, 2, self.powers_of_3[row * self.no_of_columns + column])

	def choose_next_move(self, configuration):
		current_state = matrix_from_configuration(configuration)

def matrix_from_configuration(configuration):
	Matrix = [[0 for x in range(3)] for y in range(3)]
	row = 2
	column = 2
	while (configuration > 0):
		Matrix[row][column] = configuration % 10
		configuration /= 10
		column -= 1
		if (column == -1):
			row -= 1
			column = 2
	return Matrix


def min_between(a, b):
	if a < b:
		return a
	return b

def max_between(a, b):
	if a > b:
		return a
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

def play_game(current_object, move, configuration):	
	#current_object.print_board()
	#print()
	
	current_object.visited[configuration] = 1

	if (detect_player(move) == 1):
		current_object.benefit[configuration] = 1 #player 1 wins
		#print(configuration, " 1")
		#print()
	else:
		current_object.benefit[configuration] = 3 #player 2 wins
		#print(configuration, " 2")
		#print()

	if (check_end_of_game(current_object) == 1):
		#print("somebody won")
		#current_object.print_board()
		#print()
		return

	if (move == current_object.get_number_of_rows() * current_object.get_number_of_columns() + 1):
		current_object.benefit[configuration] = 2 #equality
		#print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!equality")
		#current_object.print_board()
		print()

	for i in range(current_object.no_of_rows):
		for j in range(current_object.no_of_columns):
			if (current_object.board[i][j] == 0):
				if (detect_player(move) == 1):
					current_object.board[i][j] = 1
					new_configuration = configuration + current_object.powers_of_3[i * current_object.get_number_of_columns() + j]
					if current_object.visited[new_configuration] == 0:
						play_game(current_object, move + 1, new_configuration)
					current_object.benefit[configuration] = max_between(current_object.benefit[configuration], current_object.benefit[new_configuration])
					current_object.board[i][j] = 0
				else:
					current_object.board[i][j] = 2
					new_configuration = configuration + 2 * current_object.powers_of_3[i * current_object.get_number_of_columns() + j]
					if current_object.visited[new_configuration] == 0:
						play_game(current_object, move + 1, new_configuration)
					current_object.benefit[configuration] = min_between(current_object.benefit[configuration], current_object.benefit[new_configuration])
					current_object.board[i][j] = 0

				'''
				if (move % 3 == 0):
					print("print random??????????????????????????????????????????????????")
					current_object.print_board();
					print("benefit ", current_object.benefit[configuration])
					print()
				'''

def check_end_of_game(current_object):
	"""
	for i in range(current_object.get_number_of_rows()):
		for j in range(current_object.get_number_of_columns() - current_object.get_winning_length()):
			value = current_object.board[i][j]
			for k in range(current_object.get_winning_length()):
				if (current_object.board[i][j+k] != value):
					break
			if (k == current_object.get_winning_length()):
				return 1

	for j in range(current_object.get_number_of_columns()):
		for i in range(current_object.get_number_of_rows() - current_object.get_winning_length()):
			value = current_object.board[i][j]
			for k in range(current_object.get_winning_length()):
				if (current_object.board[i+k][j] != value):
					break
			if (k == current_object.get_winning_length()):
				return 1

	return 0
	"""

	if (current_object.board[0][0] == 1 and current_object.board[1][1] == 1 and current_object.board[2][2] == 1):
		return 1
	if (current_object.board[2][0] == 1 and current_object.board[1][1] == 1 and current_object.board[0][2] == 1):
		return 1
	if (current_object.board[0][0] == 2 and current_object.board[1][1] == 2 and current_object.board[2][2] == 2):
		return 1
	if (current_object.board[2][0] == 2 and current_object.board[1][1] == 2 and current_object.board[0][2] == 2):
		return 1

	for i in range(3):
		if(current_object.board[i][0] == 1 and current_object.board[i][1] == 1 and current_object.board[i][2] == 1):
			return 1
		if(current_object.board[0][i] == 1 and current_object.board[1][i] == 1 and current_object.board[2][i] == 1): 
			return 1
		if(current_object.board[i][0] == 2 and current_object.board[i][1] == 2 and current_object.board[i][2] == 2): 
			return 1
		if(current_object.board[0][i] == 2 and current_object.board[1][i] == 2 and current_object.board[2][i] == 2): 
			return 1

	return 0


def detect_player(move):
	if move % 2 == 1:
		return 1
	return 2


c1 = Game(3, 3, 3)
c1.start_game()
#c1.print_benefit()
#c1.print_board()