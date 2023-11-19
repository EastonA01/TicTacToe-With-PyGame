"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # Check first if the game is over, if it is then return none
    if terminal(board) == True:
        return None

    # Declare counts for X and O's
    x_count = 0
    o_count = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                x_count += 1
    for i in range(3):
        for j in range(3):
            if board[i][j] == O:
                o_count += 1

    # If the board is empty OR the count is the same, it's X's turn
    if x_count == o_count:
        return X
    # Else count how many X's on the board and how many O's,
    # Depending on who has more, it is the lesser's turn
    elif x_count > o_count:
        return O

    elif o_count > x_count:
        return X

    # Final odd check to see if anything breaks
    else:
        raise "Fatal error at player"
### Code for player ends here ###


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # If game is finished, return None
    if terminal(board) == True:
        return None
    # Start with declaring the set so that we can append into it later, placed None inside code because otherwise parenthesis and commas separating values turn into a single colon.
    possible_moves = {None}
    # Iterate through each row and cell in a double for loop
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                # Specific source of the solution for this found here [https://stackoverflow.com/questions/39295942/python-append-tuple-to-a-set-with-tuples], data would always send off crazy errors prior to this fix.
                possible_moves.update([(i, j)])
    # Remove None From possible_moves
    possible_moves.remove(None)
    return possible_moves
### Code for actions ends here ###


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # print(board)
    if action == None:
        raise Exception("Odd NoneType Error")
    # Break the tuple into two sections, row and column numbers
    row, column = action
    # Check if the action is a valid placement on the board
    # Current iteration presumes we are talking about a valid board placement within the grid 0-2 in i and j
    if board[row][column] != None:
        raise Exception("Not a valid position on the board")
    else:
        # Declare the deep copy to apply our changes to
        board_copy = copy.deepcopy(board)
        # In order to apply the changes, we do need to know whose turn it is.
        if player(board) == X:
            board_copy[row][column] = X
            return board_copy
        elif player(board) == O:
            board_copy[row][column] = O
            return board_copy
        else:
            raise Exception("Fatal Error at Result")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check if X is a winner
    if helper_match(board, X) == True:
        return X
    # Check if O is a winner
    elif helper_match(board, O) == True:
        return O
    # If no winner, return none
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check for win state
    if winner(board) == X or winner(board) == O:
        return True
    # Check for NON-blackout state
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                return False
    # Game Ending Blackout
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Check first if game is over, if so return none
    if terminal(board) == True:
        return None
    # Player Variable
    bot = player(board)

    # Check for best max value (1 or 0)
    # Code is basically the same for X and O, save for supplementing mini_value and max_value for our score
    if bot == X:
        # Store best score
        best_score = -1
        # Store best move as an empty variable till we occupy it later in the loop
        best_move = EMPTY
        for action in actions(board):
            tmp_board = result(board, action)
            score = mini_value(tmp_board)
            # This single greater than sign was the bane of my existence. If set to a less than sign best score will never update and loop to an error.
            if score > best_score:
                best_score = score
                best_move = action
        return best_move
    # Look for the mini value
    else:
        # Do the code that looks for the smallest possible mini value (-1 or 0)
        best_score = 1
        best_move = EMPTY
        for action in actions(board):
            tmp_board = result(board, action)
            score = max_value(tmp_board)
            if score < best_score:
                best_score = score
                best_move = action
        return best_move


def mini_value(board):
    """
    Returns the best action for the case of an O win (mini)
    """
    # Check for terminal board state
    if terminal(board) == True:
        return utility(board)
    # Declare mini
    mini = math.inf
    # Recursively loop in max by comparing our best move against our opposing agent
    for action in actions(board):
        mini = min(mini, max_value(result(board, action)))
    return mini


def max_value(board):
    """
    Returns the best action for the case of an X win (max)
    """
    # Check for terminal board state
    if terminal(board) == True:
        return utility(board)
    # Declare maxi
    # Calling it maxi since max is a built-in python function [Found this and min() out from my mentor W3Schools.com]
    maxi = -math.inf
    # Recursively loop in max by comparing our best move against our opposing agent
    for action in actions(board):
        maxi = max(maxi, mini_value(result(board, action)))
    return maxi


def helper_match(board, player):
    """
    Returns the matching pattern to check win condition for X or O
    """
    player = player
    # Check Vertical Win
    if player == board[0][0] and player == board[1][0] and player == board[2][0]:
        return True
    elif player == board[0][1] and player == board[1][1] and player == board[2][1]:
        return True
    elif player == board[0][2] and player == board[1][2] and player == board[2][2]:
        return True
    # Check Horizontal Win
    elif player == board[0][0] and player == board[0][1] and player == board[0][2]:
        return True
    elif player == board[1][0] and player == board[1][1] and player == board[1][2]:
        return True
    elif player == board[2][0] and player == board[2][1] and player == board[2][2]:
        return True
    # Check Diaganol Wins
    elif player == board[0][2] and player == board[1][1] and player == board[2][0]:
        return True
    elif player == board[0][0] and player == board[1][1] and player == board[2][2]:
        return True
    # If no matches, return False
    else:
        return False