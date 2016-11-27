import collections
import os
import random

import numpy as np
import tensorflow as tf

from common.network_helpers import load_network, get_stochastic_network_move, save_network

import functools

from common.network_helpers import create_network
from games.tic_tac_toe_x import TicTacToeXGameSpec
from games.tic_tac_toe import TicTacToeGameSpec
from techniques.train_policy_gradient import train_policy_gradients

HIDDEN_NODES = (100, 100, 100)

def predict_best_move_low_level(game_spec, create_network, network_file_path, player, board_state):
    """Make a predicition for the next move at a given state using some lower level parameters

    Args:
        create_network (->(input_layer : tf.placeholder, output_layer : tf.placeholder, variables : [tf.Variable])):
            Method that creates the network we will train.
        network_file_path (str): path to the file with weights we want to load for this network
        game_spec (games.base_game_spec.BaseGameSpec): The game we are playing
        player: The player to make the move 1 or -1
        board_state: The state of the board at some time during the game

    Returns:
        a vector of zeros with a 1 on the position which represents the best move to be taken
    """
    reward_placeholder = tf.placeholder("float", shape=(None,))
    actual_move_placeholder = tf.placeholder("float", shape=(None, game_spec.outputs()))

    input_layer, output_layer, variables = create_network()

    policy_gradient = tf.log(
        tf.reduce_sum(tf.mul(actual_move_placeholder, output_layer), reduction_indices=1)) * reward_placeholder

    with tf.Session() as session:
        session.run(tf.initialize_all_variables())

        if network_file_path and os.path.isfile(network_file_path):
            print("Loading trained network from ", network_file_path)
            load_network(session, variables, network_file_path)
        else:
            print("File with trained network can't be loaded. Exiting...'")
            return     

        return get_stochastic_network_move(session, input_layer, output_layer, board_state, player)


def predict_best_move(board_dimention, winner_line_size, trained_model_file, player, board_state):
    """Higher level abstraction function for predicting the best next move 

    Args:
        board_dimention: the size of the board. The board is squared.
        winner_line_size: the number of X/0s in a line you need 
        trained_model_file: the file which contains the trained model with the learned weighhts
        player: the player about to make the move. It could be 1 or -1. 1 means first player and -1 means second player. 
        board_state: a matrix with 1s, -1s and zeros representing the state of the board

    Returns:
        a vector of zeros with a 1 on the position which represents the best move to be taken
    """

    game_spec = TicTacToeXGameSpec(board_dimention, winner_line_size)
    create_network_func = functools.partial(create_network, game_spec.board_squares(), (300, 200, 100, 100))


    return predict_best_move_low_level(game_spec, create_network_func, trained_model_file, player, board_state)


board_state = [[1, 0, 0, 0], 
               [0, -1, 0, 0], 
               [0, 0, 0, 0],
               [0, -1, 0, 0]]
next_move = predict_best_move(4, 3, 'trained_4x4_3', -1, board_state)
print(next_move)