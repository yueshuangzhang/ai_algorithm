"""
An AI player for Othello. 
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)
    
# Method to compute utility value of terminal state
def compute_utility(board, color):
    #IMPLEMENT

    p1_count, p2_count = get_score(board)
    #Player color: 1 for dark (goes first), 2 for light. 

    if(color == 1):
        return p1_count - p2_count
    else:
        return p2_count - p1_count


# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT
    return 0 #change this!

############ MINIMAX ###############################
# Key (board, color)   Value (move, uti valuecached)
cached = {}
def minimax_min_node(board, color, limit, caching = 0):
    
    # Determine the player color
    if color == 1:
        oppo_color = 2
    else:
        oppo_color = 1

    # the valid moved
    valid_moves = get_possible_moves(board, oppo_color)
    
    if (len(valid_moves) == 0):
        # no move valid and board is not cached
        return None, compute_utility(board, color)

    elif (limit == 0):
        return None, compute_utility(board, color)
    
    else:
        u_value_best = float("Inf") # set at max possible value
        move_best = None

        for move in valid_moves:
            new_board = play_move(board, oppo_color, move[0], move[1])

            # check if the new board is in the cache
            if new_board in cached and caching:
                new_move, u_value = cached[new_board]
            
            else:
                new_move, u_value = minimax_max_node(new_board, color, limit - 1, caching)
               
                if (caching):
                    cached[new_board] = (new_move, u_value)
        
            # get the min value:
            if(u_value < u_value_best):
                u_value_best = u_value
                move_best = move

        return (move_best, u_value_best)

    return ((0,0),0)

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    
    # Determine the player color
    if color == 1:
        oppo_color = 2
    else:
        oppo_color = 1

    # the valid moved
    valid_moves = get_possible_moves(board, color)
    
    if (len(valid_moves) == 0):
        # no move valid and board is not cached
        return None, compute_utility(board, color)

    elif (limit == 0):
        return None, compute_utility(board, color)
    
    else:
        u_value_best = float("-Inf") # set at max possible value
        move_best = None

        for move in valid_moves:
            new_board = play_move(board, color, move[0], move[1])

            # check if the new board is in the cache
            if new_board in cached and caching:
                new_move, u_value = cached[new_board]
            
            else:
                new_move, u_value = minimax_max_node(new_board, color, limit - 1, caching)
               
                if (caching):
                    cached[new_board] = (new_move, u_value)
        
            # get the min value:
            if(u_value > u_value_best):
                u_value_best = u_value
                move_best = move

        return (move_best, u_value_best)

    return ((0,0),0)


def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """
    #IMPLEMENT (and replace the line below)
    move, utiltiy = minimax_max_node(board, color, limit, caching)
    return move

############ ALPHA-BETA PRUNING #####################
cached_alpha_beta = {}
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    # Get the color of the next player
    if color == 1:
        oppo_color = 2
    else:
        oppo_color = 1

    # Get the allowed moves
    valid_moves = get_possible_moves(board, oppo_color)

    # If there are no moves left, return the utility
    if len(valid_moves) == 0:
        return None, compute_utility(board, color)
    elif limit == 0:
        return None, compute_utility(board, color)

    # Else if there are moves, get their utility and return the min
    else:  
        # Get the maximum utility possible to use as a starting point for min  
        u_value_best = float("Inf")
        move_best = None

        ordered_list = []

        # Get the utility of all the moves
        for item in valid_moves:
            current_move = item[0]
            current_board = item[1]

            # Get the next board from that move
            next_board = play_move(board, oppo_color, current_move, current_board)

            # Add the moves to the list
            ordered_list.append((item, next_board))

        # Sort the list by utility
        ordered_list.sort(key = lambda utility: compute_utility(utility[1], color))

        # For item possible move, get the max utiltiy
        for item in ordered_list:
            current_move = item[0]
            current_board = item[1]

            # First check the cache for the board
            if current_board in cached_alpha_beta:
                move, new_utiltiy = cached_alpha_beta[current_board]

            else:
                # If the new utility is less than the current min, update min_utiltiy
                move, new_utiltiy = alphabeta_max_node(current_board, color, alpha, beta, limit-1, caching, ordering)
                
                if caching:
                    cached_alpha_beta[current_board] = (move, new_utiltiy)

            if new_utiltiy < u_value_best:
                u_value_best = new_utiltiy
                move_best = current_move

            if u_value_best <= alpha:
                return move_best, u_value_best 

            if u_value_best < beta:
                beta = u_value_best

        # After checking every move, return the minimum utility
        return move_best, u_value_best

    return ((0,0),0)


def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT (and replace the line below)
    # Get the allowed moves
    valid_moves = get_possible_moves(board, color)

    # If there are no moves left, return the utility
    if len(valid_moves) == 0 or limit == 0:
        return None, compute_utility(board, color)

    # Else if there are moves, get their utility and return the min
    else:  
        # Store the minimum utility possible to use as a starting point for min  
        u_value_best = -1 * len(board)*len(board)
        move_best = None

        ordered_list = []

        # Get the utility of all the moves
        for item in valid_moves:
            current_move = item[0]
            current_board = item[1]

            # Get the next board from that move
            next_board = play_move(board, color, current_move, current_board)

            # Add the moves to the list
            ordered_list.append((item, next_board))

        # Sort the list by utility (reversed so when iterated, it starts at the greatest value)
        ordered_list.sort(key = lambda utility: compute_utility(utility[1], color), reverse=True)

        # For item possible move, get the min utiltiy
        for item in ordered_list:

            current_move = item[0]
            current_board = item[1]
            

            # First check the cache for the board
            if current_board in cached_alpha_beta:
                move, new_utiltiy = cached_alpha_beta[current_board]

            else:
                # If the new utility is greater than the current max, update u_value_best
                move, new_utiltiy = alphabeta_min_node(current_board, color, alpha, beta, limit-1, caching, ordering)
                if caching:
                    cached_alpha_beta[current_board] = (move, new_utiltiy)

            if new_utiltiy > u_value_best:
                u_value_best = new_utiltiy
                move_best = current_move

            if u_value_best >= beta:
                return move_best, u_value_best

            if u_value_best > alpha:
                alpha = u_value_best

        # After checking every move, return the maximum utility
        return move_best, u_value_best

    return ((0,0),0)


def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    #IMPLEMENT (and replace the line below)
    alpha = float("-Inf")
    beta = float("Inf")
    
    move, utiltiy = alphabeta_max_node(board, color, alpha, beta, limit, caching, ordering)
    return move


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching 
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
