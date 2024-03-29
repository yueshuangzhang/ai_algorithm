#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools

def binary_not_equal(i,j):
    return i!=j

def nary_sum_check(t,tenner_sum): 
    #t is a tuple
    return sum(t) == tenner_sum

def tenner_csp_model_1(initial_tenner_board):
  '''Return a CSP object representing a Tenner Grid CSP problem along 
      with an array of variables for the problem. That is return

      tenner_csp, variable_array

      where tenner_csp is a csp representing tenner grid using model_1
      and variable_array is a list of lists

      [ [  ]
        [  ]
        .
        .
        .
        [  ] ]

      such that variable_array[i][j] is the Variable (object) that
      you built to represent the value to be placed in cell i,j of
      the Tenner Grid (only including the first n rows, indexed from 
      (0,0) to (n,9)) where n can be 3 to 7.
      
      
      The input board is specified as a pair (n_grid, last_row). 
      The first element in the pair is a list of n length-10 lists.
      Each of the n lists represents a row of the grid. 
      If a -1 is in the list it represents an empty cell. 
      Otherwise if a number between 0--9 is in the list then this represents a 
      pre-set board position. E.g., the board
  
      ---------------------  
      |6| |1|5|7| | | |3| |
      | |9|7| | |2|1| | | |
      | | | | | |0| | | |1|
      | |9| |0|7| |3|5|4| |
      |6| | |5| |0| | | | |
      ---------------------
      would be represented by the list of lists
      
      [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
      [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
      [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
      [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
      [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]
      
      
      This routine returns model_1 which consists of a variable for
      each cell of the board, with domain equal to {0-9} if the board
      has a 0 at that position, and domain equal {i} if the board has
      a fixed number i at that cell.
      
      model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
      all relevant variables (e.g., all pairs of variables in the
      same row, etc.).
      model_1 also constains n-nary constraints of sum constraints for each 
      column.
  '''
    
#IMPLEMENT

  # get basic information on the board
  num_row = len(initial_tenner_board[0])
  
  # generate vars - according to the domain info
  vars = []
  row_vars = []
  domain = []

  for row in range(num_row): #iterate through n (3<n<8)
    row_vars = []

    # since the number in a row will be between 0 to 9
    for col in range(10):
      # if this is a space to fill
      if (initial_tenner_board[0][row][col] == -1):
        for k in range(10):
          domain.append(k)
      # the number is fixed
      else:
          domain.append(initial_tenner_board[0][row][col])

      row_vars.append(Variable('{}{}'.format(row, col), domain))
    vars.append(row_vars)

  # generate constrains
  cons = []
  # return value:
  # add scope to csp
  csp = CSP("model 1", [scope for v in vars for scope in v])

  # =============================== ROW CONSTRAINS ===============================

  possible_pair = []

  # check # in a row - no repeat
  
  for i in range(len(initial_tenner_board[0])):
    for j in range(10):
      for k in range(j+1, 10):

        con = Constraint("C(Q{},Q{})".format(i,j),[vars[i][j],vars[i][k]])
        sat_tuples = []

        for t in itertools.product(vars[i][j].cur_domain(), vars[i][k].cur_domain()):   
          if binary_not_equal(t[0],t[1]):
            sat_tuples.append(t)
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)
  print("Done here")
        
  # =============================== ADJ CONSTRAINS ===============================

  # The digits in adjacent cells (even cells that are diagonally adjacent) 
  # must be different. 
  # For example, cell(0,0) is adjacent to cell(0,1), cell(1,0) and cell(1,1). 

  # loop through till the line before the last line: num row - 1, check with next row
  for row in range(num_row - 1): 
    for col in range(10):

      # Since the left/right in the same row, -> no need to check, included previously
      # check bottom left, bottom, bottom right

      # === bottom left ===
      if col != 0:
        current_var = vars[row][col]
        bot_left_var = vars[row + 1][col - 1]

        possible_pair = []
        
        for vars_pair in itertools.product(current_var.cur_domain(), bot_left_var.cur_domain()):
          if vars_pair[0] != vars_pair[1]:
            possible_pair.append(vars_pair)

        new_con = Constraint("C:(row {},col {})".format(row,col),[current_var, bot_left_var])
        new_con.add_satisfying_tuples(possible_pair)
        cons.append(new_con)


      # === bot === 
      # check the var below
      possible_pair = []
      # row col and row+1, col
      current_var = vars[row][col]
      bot_var = vars[row + 1][col]
      for vars_pair in itertools.product(current_var.cur_domain(), bot_var.cur_domain()):
        if vars_pair[0] != vars_pair[1]:
          possible_pair.append(vars_pair)

      new_con = Constraint("C:(row {},col {})".format(row,col),[current_var, bot_var])
      new_con.add_satisfying_tuples(possible_pair)
      cons.append(new_con)

      # === bottom right ===
      if col != 9: 
        current_var = vars[row][col]
        bot_right_var = vars[row + 1][col + 1]
        possible_pair = []
        
        for vars_pair in itertools.product(current_var.cur_domain(), bot_right_var.cur_domain()):
          if vars_pair[0] != vars_pair[1]:
            possible_pair.append(vars_pair)

        new_con = Constraint("C:(row {},col {})".format(row,col),[current_var, bot_right_var])
        new_con.add_satisfying_tuples(possible_pair)
        cons.append(new_con)

  # =============================== SUM CONSTRAINS ===============================

  # n-ary sum constraints.
  # The (n+1)-th row contains numbers which give the sum of the numbers in their respective columns. 
  # The numbers in the (n+1)-th row are always given in the start state.

  # for all columns, the sum of the value is the defined by board[1]
  for col in range(10):
    vars_in_col = []
    variable_domain = []
    possible_sum_pair = []

    for row in range(num_row):
      #get all variables - variable list
      vars_in_col.append(vars[row][col])
      #get their domain
      variable_domain.append(vars[row][col].cur_domain())

    for var in itertools.product(*variable_domain):
      # compute sum of the col
      col_sum = sum(var)
      if col_sum == initial_tenner_board[1][col]:
        possible_sum_pair.append(var)

    new_con = Constraint("C:(row {},col {})".format(row,col), vars_in_col)
    new_con.add_satisfying_tuples(possible_sum_pair)
    cons.append(new_con)
    
  # =============================== compute return value ===============================
  for con in cons:
    csp.add_constraint(con)

  return csp, vars

##############################

def tenner_csp_model_2(initial_tenner_board):
  '''Return a CSP object representing a Tenner Grid CSP problem along 
      with an array of variables for the problem. That is return

      tenner_csp, variable_array

      where tenner_csp is a csp representing tenner using model_1
      and variable_array is a list of lists

      [ [  ]
        [  ]
        .
        .
        .
        [  ] ]

      such that variable_array[i][j] is the Variable (object) that
      you built to represent the value to be placed in cell i,j of
      the Tenner Grid (only including the first n rows, indexed from 
      (0,0) to (n,9)) where n can be 3 to 7.

      The input board takes the same input format (a list of n length-10 lists
      specifying the board as tenner_csp_model_1.
  
      The variables of model_2 are the same as for model_1: a variable
      for each cell of the board, with domain equal to {0-9} if the
      board has a -1 at that position, and domain equal {i} if the board
      has a fixed number i at that cell.

      However, model_2 has different constraints. In particular, instead
      of binary non-equals constaints model_2 has a combination of n-nary 
      all-different constraints: all-different constraints for the variables in
      each row, and sum constraints for each column. You may use binary 
      contstraints to encode contiguous cells (including diagonally contiguous 
      cells), however. Each -ary constraint is over more 
      than two variables (some of these variables will have
      a single value in their domain). model_2 should create these
      all-different constraints between the relevant variables.
  '''

  #IMPLEMENT

  # get basic information on the board
  num_row = len(initial_tenner_board[0])
  
  # generate vars - according to the domain info
  vars = []
  row_vars = []
  domain = []

  for row in range(num_row): #iterate through n (3<n<8)
    row_vars = []

    # since the number in a row will be between 0 to 9
    for col in range(10):
      # if this is a space to fill
      if (initial_tenner_board[0][row][col] == -1):
        domain = []
        for k in range(10):
          domain.append(k)
      # the number is fixed
      else:
          domain = []
          domain.append(initial_tenner_board[0][row][col])

      row_vars.append(Variable('{}{}'.format(row, col), domain))
    vars.append(row_vars)

  # generate constrains
  cons = []
  # return value:
  # add scope to csp
  csp = CSP("model 2", [scope for v in vars for scope in v])

  # =============================== ROW CONSTRAINS ===============================

  possible_pair = []

  # check # in a row - no repeat

  for row in range(num_row):
    # ensure for every row, the domain is complete
    domain = []
    for k in range(10):
      domain.append(k)

    possible_pair = []
    var_in_row = []

    for col in range(10):
      if initial_tenner_board[0][row][col] != -1:
        if initial_tenner_board[0][row][col] in domain:
          domain.remove(initial_tenner_board[0][row][col]) #make the domain smaller
      else:
        var_in_row.append(vars[row][col])

    for vars_pair in itertools.permutations(domain):
      possible_pair.append(vars_pair)

    new_con = Constraint("C{}".format(row), var_in_row)
    new_con.add_satisfying_tuples(possible_pair)
    cons.append(new_con)
  
  # =============================== ADJ CONSTRAINS ===============================

  # The digits in adjacent cells (even cells that are diagonally adjacent) 
  # must be different. 
  # For example, cell(0,0) is adjacent to cell(0,1), cell(1,0) and cell(1,1). 

  # loop through till the line before the last line: num row - 1, check with next row
  for row in range(num_row - 1): 
    for col in range(10):

      # Since the left/right in the same row, -> no need to check, included previously
      # check bottom left, bottom, bottom right

      # === bottom left ===
      if col != 0:
        current_var = vars[row][col]
        bot_left_var = vars[row + 1][col - 1]

        possible_pair = []
        
        for vars_pair in itertools.product(current_var.cur_domain(), bot_left_var.cur_domain()):
          if vars_pair[0] != vars_pair[1]:
            possible_pair.append(vars_pair)

        new_con = Constraint("C:(row {},col {})".format(row,col),[current_var, bot_left_var])
        new_con.add_satisfying_tuples(possible_pair)
        cons.append(new_con)


      # === bot === 
      # check the var below
      possible_pair = []
      # row col and row+1, col
      current_var = vars[row][col]
      bot_var = vars[row + 1][col]
      for vars_pair in itertools.product(current_var.cur_domain(), bot_var.cur_domain()):
        if vars_pair[0] != vars_pair[1]:
          possible_pair.append(vars_pair)

      new_con = Constraint("C:(row {},col {})".format(row,col),[current_var, bot_var])
      new_con.add_satisfying_tuples(possible_pair)
      cons.append(new_con)

      # === bottom right ===
      if col != 9: 
        current_var = vars[row][col]
        bot_right_var = vars[row + 1][col + 1]
        possible_pair = []
        
        for vars_pair in itertools.product(current_var.cur_domain(), bot_right_var.cur_domain()):
          if vars_pair[0] != vars_pair[1]:
            possible_pair.append(vars_pair)

        new_con = Constraint("C:(row {},col {})".format(row,col),[current_var, bot_right_var])
        new_con.add_satisfying_tuples(possible_pair)
        cons.append(new_con)


  # =============================== SUM CONSTRAINS ===============================

  # n-ary sum constraints.
  # The (n+1)-th row contains numbers which give the sum of the numbers in their respective columns. 
  # The numbers in the (n+1)-th row are always given in the start state.

  # for all columns, the sum of the value is the defined by board[1]
  for col in range(10):
    vars_in_col = []
    variable_domain = []
    possible_sum_pair = []

    for row in range(num_row):
      #get all variables - variable list
      vars_in_col.append(vars[row][col])
      #get their domain
      variable_domain.append(vars[row][col].cur_domain())

    for var in itertools.product(*variable_domain):
      # compute sum of the col
      col_sum = sum(var)
      if col_sum == initial_tenner_board[1][col]:
        possible_sum_pair.append(var)

    new_con = Constraint("C:(row {},col {})".format(row,col), vars_in_col)
    new_con.add_satisfying_tuples(possible_sum_pair)
    cons.append(new_con)
    
  # =============================== compute return value ===============================
  
  for con in cons:
    csp.add_constraint(con)
  return csp, vars


b1 = ([[-1, 0, 1,-1, 9,-1,-1, 5,-1, 2],
       [-1, 7,-1,-1,-1, 6, 1,-1,-1,-1],
       [-1,-1,-1, 8,-1,-1,-1,-1,-1, 9],
       [ 6,-1, 4,-1,-1,-1,-1, 7,-1,-1],
       [-1, 1,-1, 3,-1,-1, 5, 8, 2,-1]],
      [29,16,18,21,24,24,21,28,17,27])

from propagators import prop_FC,  prop_GAC, ord_mrv

def print_tenner_soln(var_array):
    for row in var_array:
        print([var.get_assigned_value() for var in row])

csp, var_array = tenner_csp_model_1(b1)
if csp != None:
    solver = BT(csp)
    print("=======================================================")
    print("GAC")
    solver.bt_search(prop_GAC, var_ord=ord_mrv)
    print("Solution")
    print_tenner_soln(var_array)

