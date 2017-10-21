"""6.009 Lab 5 -- Mines"""
spaces_revealed = 0
status = 'ongoing'
NEIGHBORS = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
from copy import deepcopy

def dump(game):
    """Print a human-readable representation of game.

    Arguments:
       game (dict): Game state


    >>> dump({'dimensions': [1, 2], 'mask': [[False, False]], 'board': [['.', 1]]})
    dimensions: [1, 2]
    board: ['.', 1]
    mask:  [False, False]
    """
    lines = ["dimensions: {}".format(game["dimensions"]),
             "board: {}".format("\n       ".join(map(str, game["board"]))),
             "mask:  {}".format("\n       ".join(map(str, game["mask"])))]
    print("\n".join(lines))

def new_game(num_rows, num_cols, bombs):
    """Start a new game.

    Return a game state dictionary, with the "board" and "mask" fields
    adequately initialized.

    Args:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs

    Returns:
       A game state dictionary

    >>> dump(new_game(2, 4, [(0, 0), (1, 0), (1, 1)]))
    dimensions: [2, 4]
    board: ['.', 3, 1, 0]
           ['.', '.', 1, 0]
    mask:  [False, False, False, False]
           [False, False, False, False]
    """
    game_state = {'dimensions': [num_rows, num_cols], 'board':[[0 for i in range(num_cols)] for j in range(num_rows)], 'mask': [[False for x in range(num_cols)] for y in range(num_rows)]}

    for b in bombs:
        game_state['board'][b[0]][b[1]] = '.' 


    for rows in range(len(game_state['board'])):
        for col in range(len(game_state['board'][rows])):
            if game_state['board'][rows][col] != '.':
                game_state['board'][rows][col] = count_neighboring_bombs(game_state['board'],rows,col)



    return game_state

def count_neighboring_bombs(game_board, x, y):
    """Get a count of the neighboring bombs for all vacant spaces on board.

    Return a 'board' with empty spaces filled in with the count of number of neighboring bombs

    Args:
        game_board (list): game board with only bombs populated
        x (int): x-position of current space 
        y (int): y-position of current space

    Returns:
        number of bombs adjacent to current position(x,y)

    >>> count_neighboring_bombs([['.', 0, 0, 0], ['.', '.', 0, 0]], 0, 1)
    3

    """
    
    count = 0

    for r in range(x-1,x+2):
        for c in range(y-1,y+2):
            try:
                if game_board[r][c] == '.' and r >= 0 and c >= 0:
                    count += 1
            except IndexError:
                pass
    return count
                





def dig(game, row, col):
    """Recursively dig up (row, col) and neighboring squares.

    Update game["mask"] to reveal (row, col); then recursively reveal (dig up)
    its neighbors, as long as (row, col) does not contain and is not adjacent to
    a bomb.  Return a pair: the first element indicates whether the game is over
    using a string equal to "victory", "defeat", or "ongoing", and the second
    one is a number indicates how many squares were revealed.

    The first element is "defeat" when at least one bomb is visible on the board
    after digging (i.e. game["mask"][bomb_location] == True), "victory" when all
    safe squares (squares that do not contain a bomb) and no bombs are visible,
    and "ongoing" otherwise.

    Args:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       Tuple[str,int]: A pair of game status and number of squares revealed

    >>> game = {"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask": [[False, True, False, False],
    ...                  [False, False, False, False]]}
    >>> dig(game, 0, 3)
    ('victory', 4)
    >>> dump(game)
    dimensions: [2, 4]
    board: ['.', 3, 1, 0]
           ['.', '.', 1, 0]
    mask:  [False, True, True, True]
           [False, False, True, True]

    >>> game = {"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask": [[False, True, False, False],
    ...                  [False, False, False, False]]}
    >>> dig(game, 0, 0)
    ('defeat', 1)
    >>> dump(game)
    dimensions: [2, 4]
    board: ['.', 3, 1, 0]
           ['.', '.', 1, 0]
    mask:  [True, True, False, False]
           [False, False, False, False]
    """
    spaces_revealed = 0

    if game['board'][row][col] == '.':
        game['mask'][row][col] = True
        return ('defeat', 1)
    if check_victory(game) == 'victory':
        return ('victory', 0)


        

    if spaces_revealed == 0 and game['board'][row][col] == '.' and not game['mask'][row][col]: # initial choice was space with bomb
        game['mask'][row][col] = True
        spaces_revealed += 1
        return ('defeat', 1)




    # reveal space
    game['mask'][row][col] = True 
    spaces_revealed += 1
    

    result = dig_helper(game,row,col,spaces_revealed)


    return result



def dig_helper(game, row, col, revealed):
    """Recursive helper function for dig 
    helps keep track of spaces revealed

    >>> dig_helper({'dimensions': [2,2],'board': [[1,'.'],[1,1]],'mask':[[True, False],[True, True]]},0,0,1)
    ('victory', 1)

    """


    if check_victory(game) == 'victory' :
        return ('victory', revealed)


    if game['board'][row][col]>0:
        status = check_victory(game)
        if status == 'victory':
            return ('victory',revealed)
        elif status == 'ongoing':
            return ('ongoing', revealed)

    if not game['mask'][row][col]:
        game['mask'][row][col] = True
        revealed += 1

    
    # recursive calls to check neighbors
    for (i,j) in NEIGHBORS:
        if inBounds(game['dimensions'],row+i, col+j):
            if game['board'][row+i][col+j] == 0 and not game['mask'][row+i][col+j]:
                revealed = dig_helper(game,row+i,col+j, revealed)[1]
            elif not game['mask'][row+i][col+j]:
                game['mask'][row+i][col+j] = True
                revealed += 1


    return (check_victory(game), revealed)








        
def check_victory(game):
    """Check if game has been won

    Goes through board and mask to check if every bomb remains hidden
    as well as checks if every non-bomb space is revealed

    Args:
        game (dict): Game state

    Returns:
        str: Status of the game state


    >>> game = {"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask": [[False, True, True, True],
    ...                  [False, False, True, True]]}
    >>> check_victory(game)
    'victory'



    """
    for r in range(game['dimensions'][0]):
        for c in range(game['dimensions'][1]):
            if game['board'][r][c] != '.' and not game['mask'][r][c]:
                return 'ongoing'
            elif game['board'][r][c] == '.' and game['mask'][r][c]:
                return 'defeat'
    return 'victory'




def inBounds(dimensions, x,y):
    """Check if coordinate is in bounds 

    Args: 
        dimensions (list): dimensions of board [# of rows, # of columns]
        x (int): x-position of selection
        y (int): y-position of selection

    Returns:
        True if selection falls within dimensions of game board

    >>> inBounds([2,4],1,2)
    True

    >>> inBounds([2,4],-1,1)
    False
    """
    if x<dimensions[0] and x >= 0 and y < dimensions[1] and y>=0:
        return True
    return False



def render(game, xray=False):
    """Prepare a game for display.

    Returns a two-dimensional array (list of lists) of "_" (hidden squares), "."
    (bombs), " " (empty squares), or "1", "2", etc. (squares neighboring bombs).
    game["mask"] indicates which squares should be visible.  If xray is True (the
    default is False), game["mask"] is ignored and all cells are shown.

    Args:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game["mask"]

    Returns:
       A 2D array (list of lists)

    >>> render({"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask":  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'],
     ['_', '_', '1', '_']]

    >>> render({"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask":  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '],
     ['.', '.', '1', ' ']]
    """
    result = [[ "_" for x in range(game['dimensions'][1])] for i in range(game['dimensions'][0]) ]

    if xray:
        for i in range(game['dimensions'][0]):
            for j in range(game['dimensions'][1]):
                if game['board'][i][j] == 0:
                    result[i][j] = ' '
                else:
                    result[i][j] = str(game['board'][i][j])
        return result
        
    
    for i in range(game['dimensions'][0]):
        for j in range(game['dimensions'][1]):
            if game['mask'][i][j]:
                if game['board'][i][j] == 0:
                    result[i][j] = ' '
                else:
                    result[i][j] = str(game['board'][i][j])

    return result



def render_ascii(game, xray=False):
    """Render a game as ASCII art.

    Returns a string-based representation of argument "game".  Each tile of the
    game board should be rendered as in the function "render(game)".

    Args:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game["mask"]

    Returns:
       A string-based representation of game

    >>> print(render_ascii({"dimensions": [2, 4],
    ...                     "board": [[".", 3, 1, 0],
    ...                               [".", ".", 1, 0]],
    ...                     "mask":  [[True, True, True, False],
    ...                               [False, False, True, False]]}))
    .31_
    __1_
    """
    result = render(game, xray)
    result_string = ''
    count = 0
    for i in result:
        for j in i:
            result_string += str(j)
        if count != (len(result)-1):
            result_string += '\n'
        count += 1


    return result_string

def nd_new_game(dims, bombs):
    """Start a new game.

    Return a game state dictionary, with the "board" and "mask" fields
    adequately initialized.  This is an N-dimensional version of new_game().

    Args:
       dims (list): Dimensions of the board
       bombs (list): bomb locations as a list of tuples, each an N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> dump(nd_new_game([2, 4, 2], [(0, 0, 1), (1, 0, 0), (1, 1, 1)]))
    dimensions: [2, 4, 2]
    board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
           [['.', 3], [3, '.'], [1, 1], [0, 0]]
    mask:  [[False, False], [False, False], [False, False], [False, False]]
           [[False, False], [False, False], [False, False], [False, False]]
    """
    game = {}
    game['dimensions'] = dims[:]
    

    game['board'] = nd_mkboard(dims, 0)
    #print game['board']
    game['mask'] = nd_mkboard(dims, False)
    #print game['mask']
    

    #set bombs
    for b in bombs:
        nd_set_recursive(game['board'], b, '.')
    
    #count neighboring bombs

    list_of_indices = generate_indices(game)
    for index in list_of_indices:
        if nd_get_recursive(game['board'], index) != '.':
            neighbors = nd_neighbors(game, index)
            nd_set_recursive(game['board'], index, count_neighbor_bombs(neighbors, bombs))

    
    return game

def nd_mkboard(dims, filler):
    """Creates n-dimensional board and fills all space with givn value

    Args:
        dims (list): dimesnsions of the board
        filler: Value that will fill all spaces on the board

    >>> nd_mkboard([2,2], True)
    [[True, True], [True, True]]
    """
    if len(dims) == 0:
        return filler
    else:
        return [nd_mkboard(deepcopy(dims[1:]), filler) for i in xrange(dims[0])]

def nd_product(sequences):
    """Produce the Cartesian product of sequences.
    
    Arguments:
        sequences (list): Sequences to compute the product of

    Returns:
        A list of tuples
    >>> nd_product(((1, 2, 3), ("a", "b")))
    [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b'), (3, 'a'), (3, 'b')]
    """

    if len(sequences) == 0:
        return[()]
    return [x + (y,) for x in nd_product(sequences[:-1]) for y in sequences[-1]]

def nd_neighbors(game, coords):
    """Produce all neighbors of coords in game.

    Arguments:
        game (dict): Game state
        coords (tuple): Reference point
    Returns:
        An iterable of coordinates
    >>> game = {"dimensions": [2, 4, 2],
    ... "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ... [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ... "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ... [[False, False], [False, False], [False, False], [False, False]]]}
    >>> sorted(nd_neighbors(game, (1, 2, 0)))
    [(0, 1, 0), (0, 1, 1),
    (0, 2, 0), (0, 2, 1),
    (0, 3, 0), (0, 3, 1),
    (1, 1, 0), (1, 1, 1),
    (1, 2, 0), (1, 2, 1),
    (1, 3, 0), (1, 3, 1)]
    """
    dims = game['dimensions']
    r =[]
    for i in range(len(coords)):
        r.append(range( max(0, coords[i]-1), min(dims[i], coords[i]+2)))
    return sorted(nd_product(r))

def count_neighbor_bombs(neighbors, bombs):
    """Counts the number of neighboring bombs

    Args: 
        neighbors (list): list of neighbors to be investigated 
        bombs (list): list of all bombs on board

    returns:
        count of bombs in list neighbors

    >>> count_neighbor_bombs([(0,1), (1,1)], [(0,1), (2,4)])
    1
    """
    count = 0
    for n in neighbors:
        if n in bombs:
            count +=1
    return count




def generate_indices(game):
    """Generates list of all coordinates of n-dimensional board

    Args:
        game (dic): game state dictionary
    returns:
        list of all coordinates

    >>> generate_indices({'dimensions': [2,2], 'board': [[1,'.'], [1,1]], 'mask': [[True, False], [True, True]]})
    [(0, 0), (0, 1), (1, 0), (1, 1)]
    """
    return sorted(nd_product([range(dim) for dim in game['dimensions']]))

def nd_set_recursive(nd_array, coords, value):
    """Set element at coords in nd_array.

    Arguments:
        nd_array (list): N-dimensional input array
        coords (tuple): Coordinates of interest
        value: Value to put at coords

    >>> test = [[False, False],[False, False]]
    >>> nd_set_recursive(test, (0,0), True)
    >>> test
    [[True, False], [False, False]]

    """
    if len(coords) == 1:
        nd_array[coords[0]] = value
    else:
        nd_set_recursive(nd_array[coords[0]], coords[1:], value)


def nd_get_recursive(nd_array, coords):
    """Get element at coords in nd_array.

    Arguments:
        nd_array (list): N-dimensional input array
        coords (tuple): Coordinates of interest

    Returns:
        An array element

    >>> nd_get_recursive([[False, True],[False, False]], (0,1))
    True
    """

    if len(coords) == 1:
        return nd_array[coords[0]]
    else:
        return nd_get_recursive(nd_array[coords[0]], coords[1:])



def nd_dig(game, coords):
    """Recursively dig up square at coords and neighboring squares.

    Update game["mask"] to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a pair: the first element indicates whether the game is over
    using a string equal to "victory", "defeat", or "ongoing", and the second
    one is a number indicates how many squares were revealed.

    The first element is "defeat" when at least one bomb is visible on the board
    after digging (i.e. game["mask"][bomb_location] == True), "victory" when all
    safe squares (squares that do not contain a bomb) and no bombs are visible,
    and "ongoing" otherwise.

    This is an N-dimensional version of dig().

    Args:
       game (dict): Game state
       coords (tuple): Where to start digging

    Returns:
       A pair of game status and number of squares revealed

    >>> game = {"dimensions": [2, 4, 2],
    ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ...                  [[False, False], [False, False], [False, False], [False, False]]]}
    >>> nd_dig(game, (0, 3, 0))
    ('ongoing', 8)
    >>> dump(game)
    dimensions: [2, 4, 2]
    board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
           [['.', 3], [3, '.'], [1, 1], [0, 0]]
    mask:  [[False, False], [False, True], [True, True], [True, True]]
           [[False, False], [False, False], [True, True], [True, True]]

    >>> game = {"dimensions": [2, 4, 2],
    ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ...                  [[False, False], [False, False], [False, False], [False, False]]]}
    >>> nd_dig(game, (0, 0, 1))
    ('defeat', 1)
    >>> dump(game)
    dimensions: [2, 4, 2]
    board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
           [['.', 3], [3, '.'], [1, 1], [0, 0]]
    mask:  [[False, True], [False, True], [False, False], [False, False]]
           [[False, False], [False, False], [False, False], [False, False]]
    """
    spaces_revealed = 0
    if nd_get_recursive(game['board'], coords) == '.':
        nd_set_recursive(game['mask'], coords, True)
        return ('defeat', 1)
    if nd_check_victory(game) == 'victory':
        return ('victory', 0)

    #reveal space
    nd_set_recursive(game['mask'], coords, True)
    spaces_revealed += 1

    result = nd_dig_helper(game, coords, spaces_revealed)


    return result




def nd_dig_helper(game, coords, revealed):
    """Recursive helper function for nd_dig 
    helps keep track of spaces revealed

    >>> dig_helper({'dimensions': [2,2],'board': [[1,'.'],[1,1]],'mask':[[True, False],[True, True]]},0,0,1)
    ('victory', 1)

    """

    status = nd_check_victory(game)
    if status == 'victory':
        return ('victory', revealed)

    current = nd_get_recursive(game['board'], coords)
    if current > 0:
        if status == 'victory':
            return ('victory',revealed)
        else:
            return ('ongoing', revealed)

    is_revealed = nd_get_recursive(game['mask'], coords)
    if not is_revealed:
        nd_set_recursive(game['mask'], coords, True)
        revealed += 1

    list_of_neighbors = nd_neighbors(game, coords)
    # recursive calls to check neighbors
    for index in list_of_neighbors:
        if nd_inBounds(game['dimensions'], index):
            current = nd_get_recursive(game['board'], index)
            is_revealed = nd_get_recursive(game['mask'], index)
            if current == 0 and not is_revealed:
                revealed = nd_dig_helper(game, index, revealed)[1]
            elif not is_revealed:
                nd_set_recursive(game['mask'], index, True)
                revealed += 1

    if nd_check_victory(game) == 'victory':
        return ('victory', revealed)
    return ('ongoing', revealed)




def nd_inBounds(dims, coords):
    """Checks if coordinates are in bounds of board

    >>> nd_inBounds([1,2,4], (0,1,2))
    True
    """
    for i in range(len(dims)):
        if not (0 <= coords[i] < dims[i]):
            return False
    return True



def nd_check_victory(game):
    """ Compute game status.
        
        Return one of "ongoing", "victory", or "defeat".

    >>> nd_check_victory({'dimensions':[2,2], 'board':[[1,'.'],[1,1]], 'mask':[[True,False],[True, True]]})
    'victory'
    """
    list_of_indices = generate_indices(game)

    for index in list_of_indices:
        current = nd_get_recursive(game['board'], index)
        revealed = nd_get_recursive(game['mask'], index)
        if current == '.' and revealed:
            return 'defeat'
        elif current >= 0 and not revealed and current !='.':
            return 'ongoing'
    return 'victory'

def nd_render(game, xray=False):
    """Prepare a game for display.

    Returns an N-dimensional array (nested lists) of "_" (hidden squares), "."
    (bombs), " " (empty squares), or "1", "2", etc. (squares neighboring bombs).
    game["mask"] indicates which squares should be visible.  If xray is True (the
    default is False), game["mask"] is ignored and all cells are shown.

    This is an N-dimensional version of render().

    Args:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game["mask"]

    Returns:
       An n-dimensional array (nested lists)

    >>> nd_render({"dimensions": [2, 4, 2],
    ...            "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                      [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...            "mask": [[[False, False], [False, True], [True, True], [True, True]],
    ...                     [[False, False], [False, False], [True, True], [True, True]]]},
    ...           False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> nd_render({"dimensions": [2, 4, 2],
    ...            "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                      [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...            "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ...                     [[False, False], [False, False], [False, False], [False, False]]]},
    ...           True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """


    rendered_game = nd_mkboard(game['dimensions'], '_')
    index = [0 for _ in xrange(len(game['dimensions']))]
    place = 0


    list_of_indices = generate_indices(game)


    
    if xray:
        for index in list_of_indices:
            current = nd_get_recursive(game['board'], index)
            if current != 0:
                nd_set_recursive(rendered_game, index, str(current))
            else:
                nd_set_recursive(rendered_game, index, ' ')
        return rendered_game


    for index in list_of_indices:
        is_revealed = nd_get_recursive(game['mask'], index)

        if is_revealed:
            current = nd_get_recursive(game['board'], index)
            if current == 0:
                nd_set_recursive(rendered_game, index, ' ')
            else:
                nd_set_recursive(rendered_game, index, str(current))
        
    

    return rendered_game









    
