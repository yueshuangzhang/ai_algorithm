#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os
from search import * #for search engines
from snowman import SnowmanState, Direction, snowman_goal_state #for snowball specific classes
from test_problems import PROBLEMS #20 test problems

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a snowman state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must never overestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between each snowball that has yet to be stored and the storage point is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.

    if (snowman_goal_state(state)):
      return 0

    # check the ball's position.
    snowballs = state.snowballs
    positions = snowballs.keys()

    destination = state.destination

    # total distance
    distance = 0

    #calculate the position of the balls to the destination
    for position in positions:
      distance += abs(position[0] - destination[0])
      distance += abs(position[1] - destination[1])

    return distance


#HEURISTICS
def trivial_heuristic(state):
  '''trivial admissible snowball heuristic'''
  '''INPUT: a snowball state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''   
  return len(state.snowballs)

def heur_alternate(state):
#IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.

    '''
    This is my thoughts: only for s and m balls
    1. For any snowballs that's right besides the wall/obs: if >= 3 sides is wall/ obsticals & not goal , then distance = inf
    if == 2 sides is obs, top-left, top-right, bottom-right, bottom-left, & not goal, is cornor, distance = inf
    else is a tunnel, then for weight/height steps, if there is a obs, then dis ++

    if == 1, it should be fine .. ignore this case first
    
    use robot to determine the direction!
    '''

    if (snowman_goal_state(state)):
      return 0

    width = state.width
    height = state.height
    robot = state.robot
    snowballs = state.snowballs
    obstacles = state.obstacles

    # total distance
    distance = 0

    #for all balls:
    for snowball in snowballs:
      '''check the number of walls and obticals surrounding the ball'''
      snowball_x = snowball[0]
      snowball_y = snowball[1]

      # bools to keep the position info
      is_wall_up = False
      is_wall_down = False
      is_wall_left = False
      is_wall_right = False

      is_ob_up = False
      is_ob_down = False
      is_ob_left = False
      is_ob_right = False

      # check where are the obsticals
      for i in range(-1,2,1):# -1, 0, 1
        for j in range(-1,2,1):# -1, 0 1

          if(abs(i) != abs(j)): # skip corner and itself
            new_position_x = snowball_x + i
            new_position_y = snowball_y + j

            # check surrounding up, down, left, right
            num_block = 0

            if(new_position_x < 0 or new_position_x >= width):
              num_block += num_block
              if (i == 0):
                if (j == 1):
                  is_wall_right = True
                else:
                  is_wall_left = True
              else: #j = 0
                if (i == 1):
                  is_wall_down = True 
                else:
                  is_wall_up = True
            
            # out of bound
            elif(new_position_y < 0 or new_position_y >= height):
              num_block += num_block
              if (i == 0):
                if (j == 1):
                  is_wall_right = True
                else:
                  is_wall_left = True
              else: #j = 0
                if (i == 1):
                  is_wall_down = True 
                else:
                  is_wall_up = True

            # check obsticals
            elif((new_position_x,new_position_y) in obstacles):
              num_block += num_block
              if (i == 0):
                if (j == 1):
                  is_ob_right = True
                else:
                  is_ob_left = True
              else: #j = 0
                if (i == 1):
                  is_ob_down = True 
                else:
                  is_ob_up = True
              
      if num_block >=3:
        distance = float('inf')
      
      elif num_block == 2:
        # 2 ob/wall
        
        #Case 1: it's corner
        if ((is_wall_up and is_wall_left) or (is_wall_up and is_wall_left) or (is_wall_up and is_wall_left) or (is_wall_up and is_wall_left)):
          if (snowman_goal_state(state)):
            return 0
          else: distance = float('inf')

        else:
          if ((is_ob_up and is_ob_left) or (is_ob_up and is_ob_left) or (is_ob_up and is_ob_left) or (is_ob_up and is_ob_left)):
            if (snowman_goal_state(state)):
              return 0
            else: distance = float('inf')




      else:
        return heur_manhattan_distance(state) + 2

    return distance


def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    
    # f = g + weight*h 
    fval = sN.gval + weight * sN.hval

    return fval

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 5):
#IMPLEMENT
  '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''

  # initialize variable to return
  final_result = False

  # get the current time and the time limit
  start_time = os.times()[0]
  end_time = start_time + timebound # projected end time
  current_time = os.times()[0]
  remain_time = end_time - current_time

  # GBFS: Use the h(n) & g(n). f = w*h + g

  # Define the search method to be used: best first with cycle checking enabled
  search_engine = SearchEngine(strategy='custom', cc_level='full')

  # Initialize the search with function
  f_function = (lambda sN: fval_function(sN, weight))
  search_engine.init_search(initial_state, snowman_goal_state, f_function)
  # (g bound,h bound,g + h bound)
  costbound = (float('inf'),float('inf'),float('inf'))

  # when the search is within limit
  while current_time < end_time:
    
    # get the best search result using the search engine.
    result = search_engine.search(remain_time, costbound)

    if (result): # result == true
      # update remaining time
      current_time = os.times()[0]
      remain_time = end_time - current_time

      if result.gval <=costbound[0]:
        # (g bound,h bound,g + h bound)
        costbound = (result.gval, result.gval, result.gval + result.gval)
        final_result = result

    else: # result == false
      return final_result

  return final_result

def anytime_gbfs(initial_state, heur_fn, timebound = 5):
#IMPLEMENT
  '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''

  # initialize variable to return
  final_result = False

  # get the current time and the time limit
  start_time = os.times()[0]
  end_time = start_time + timebound # projected end time
  current_time = os.times()[0]
  remain_time = end_time - current_time

  # GBFS: Use only the h(n). Goal h(n) = 0. -> Always choose the smallest h(n)

  # Define the search method to be used: best first with cycle checking enabled
  search_engine = SearchEngine(strategy='best_first', cc_level='full')

  # Initialize the search
  search_engine.init_search(initial_state, snowman_goal_state, heur_fn)
  # (g bound,h bound,g + h bound)
  costbound = (float('inf'),float('inf'),float('inf'))

  # when the search is within limit
  while current_time < end_time:
    
    # get the best search result using the search engine.
    result = search_engine.search(remain_time, costbound)

    if (result): # result == true
      # update remaining time
      current_time = os.times()[0]
      remain_time = end_time - current_time

      if result.gval <=costbound[0]:
        # (g bound,h bound,g + h bound)
        costbound = (result.gval, result.gval, result.gval + result.gval)
        final_result = result

    else: # result == false
      return final_result

  return final_result
