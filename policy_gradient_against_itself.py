"""
Builds and trains a neural network that uses policy gradients to learn to play Tic-Tac-Toe.

Returns a probabilitity over the action space expressing the confidence that that action is the best
The opponent is playing using the trained function learned previously by playing against a random player
"""
import functools

from common.network_helpers import create_network
from games.tic_tac_toe_x import TicTacToeXGameSpec
from games.tic_tac_toe import TicTacToeGameSpec
from techniques.train_policy_gradient import train_policy_gradients

HIDDEN_NODES = (100, 100, 100)
BATCH_SIZE = 100  # every how many games to do a parameter update?
LEARN_RATE = 0.0001
PRINT_RESULTS_EVERY_X = 1000  # every how many games to print the results
NETWORK_FILE_PATH = 'current_network'    #'current_network.p'  # path to save the network to
NUMBER_OF_GAMES_TO_RUN = 100000

# to play a different game change this to another spec, e.g TicTacToeXGameSpec or ConnectXGameSpec, to get these to run
# well may require tuning the hyper parameters a bit
game_spec = TicTacToeXGameSpec(4, 3)
create_network_func = functools.partial(create_network, game_spec.board_squares(), (300, 200, 100, 100))


# compute the opponent function which is using the previously learned weights


train_policy_gradients(game_spec, create_network_func, NETWORK_FILE_PATH,
                       number_of_games=NUMBER_OF_GAMES_TO_RUN,
                       batch_size=BATCH_SIZE,
                       learn_rate=LEARN_RATE,
                       print_results_every=PRINT_RESULTS_EVERY_X)