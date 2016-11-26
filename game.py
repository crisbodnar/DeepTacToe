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
		self.benefit = [0 for x in range(no_of_rows * no_of_columns)]
		self.visited = [0 for x in range(100000000)]

	def get_number_of_rows(self):
		return self.no_of_rows

	def get_number_of_columns(self):
		return self.no_of_columns

	def get_board(self):
		return board

	def get_visited(self):
		return visited

	def print_board(self):
		for i in range(self.no_of_rows):
			for j in range(self.no_of_columns):
				print(self.board[i][j], end='')
			print()

	def print_powers_of_3(self):
		for i in range(self.no_of_rows * self.no_of_columns):
			print(self.powers_of_3[i])

	def start_game(self):
		row = randint(0, self.no_of_rows - 1)
		column = randint(0, self.no_of_columns - 1)
		self.board[row][column] = 1
		play_game(self, 2, self.powers_of_3[row * self.no_of_rows + column])

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
	#print(configuration)
	current_object.visited[configuration] = 1
	

def detect_player(move):
	if move % 2 == 1:
		return 1
	return 2


c1 = Game(4, 3, 3)
c1.start_game()
c1.print_board()
#c1.print_powers_of_3()
#c1.play_game(2, )
#c2 = Game("ana", 1, 2)