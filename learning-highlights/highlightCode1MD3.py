# From Assignment #6 - Generic Base Conversion ----------------------

def convert(num: str, new_base: int, original_base: int=10) -> str:
    '''
    convert(num:str, new_base:int, original_base:int=10)
    
    Takes a string number and converts it to a new base from an
    original base, supplied as integers. Returns number as a string in
    the new base. Cannot convert to or from a base larger than 36.
    '''

    largest_base = max(new_base, original_base) 

    if largest_base > 36: # Standard is not defined for larger bases
        raise TypeError(
            'Cannot convert to or from a base larger than 36'
        ) from TypeError

    values = "0123456789abcdefghijklmnopqrstuvwxyz"
    value_dict = {values[i]: i
        for i in range(largest_base)
    }

    x = num.lower()

    # Converts string from original base to numeric value
    accu = 0
    rev = x[::-1]
    for i in range(len(rev)):
        accu += value_dict[rev[i]] * (original_base**i)

    key_dict = {i: values[i] for i in range(len((values)))}

    # Converts numeric value to string of new base
    i = 0
    rem = accu
    str_val = "" if rem > 0 else "0"
    while rem > 0:
        str_val = key_dict[rem % new_base] + str_val
        rem = rem // new_base
        i += 1

    return str_val



# From Assignment #8 - Checkers -------------------------------------

import copy

### YOUR SOLUTION HERE
class CheckersGame () :
    def __init__ (self, board = False, turn = "white", isWon = False) :
        
        if board:
            self.board = board
        else:
            self.board  = [ [ 0, 2, 0, 2, 0, 2, 0, 2 ]
                          , [ 2, 0, 2, 0, 2, 0, 2, 0 ]
                          , [ 0, 2, 0, 2, 0, 2, 0, 2 ]
                          , [ 0, 0, 0, 0, 0, 0, 0, 0 ]
                          , [ 0, 0, 0, 0, 0, 0, 0, 0 ]
                          , [ 1, 0, 1, 0, 1, 0, 1, 0 ]
                          , [ 0, 1, 0, 1, 0, 1, 0, 1 ]
                          , [ 1, 0, 1, 0, 1, 0, 1, 0 ]
                          ]  
        
        self.whoseMove = turn
        self.isWon = isWon
    
    def checkWinner(self) :
        
        flatten = ["r" if a%2 == 0 else "w" for line in self.board for a in line if a != 0]
        
        if not( "w" in flatten and "r" in flatten ):
            if "w" in flatten:
                self.isWon = "white"
            else:
                self.isWon = "red"
    
    def changeTurn(self) :
        
        self.whoseMove = "red" if self.whoseMove == "white" else "white"
    
    def parseMove (self, move) :
        
        individualMoves = move.split()
        processedMoves = []
        
        for each in individualMoves:
            if len(each) != 2 or len({*each} - {'0','1','2','3','4','5','6','7'}):
                raise ValueError
                
            grab = lambda x: int(each[x]) 
            processedMoves.append( (grab(0), grab(1)) )
            
            
        return tuple(processedMoves)
    
    def move(self, move, processed_moves = None, turn_switching = True) :
        
        if processed_moves:
            moves = processed_moves
        else:
            moves = self.parseMove(move)
        
        for i in range(len(moves) - 1):
            
            y1, x1 = moves[i][0], moves[i][1]
            y2, x2 = moves[i+1][0], moves[i+1][1]
            
            if abs(x2-x1) == 1: # A single move, not a jump
                self.board[y1][x1], self.board[y2][x2] = 0, self.board[y1][x1]
                
            if abs(x2-x1) == 2: # A jump
                self.board[y1][x1], self.board[y2][x2] = 0, self.board[y1][x1] # same swap
                
                average = lambda x, y: int(abs(x + y)/2)
                avY, avX = average(y1, y2), average(x1, x2)
                self.board[avY][avX] = 0 # Eliminate the jumped character
                
            if self.board[y2][x2] == 1 and y2 == 0:
                self.board[y2][x2] = 3
            if self.board[y2][x2] == 2 and y2 == 7:
                self.board[y2][x2] = 4
        
        self.checkWinner()
        
        if turn_switching:
            self.changeTurn()
        
    def isValidMove(self, move, processed_moves = None, double_jump = False) :

        if processed_moves:
            moves = processed_moves
        else:
            # Validate input
            try:
                moves = self.parseMove(move)

            except:
                return False

        if moves == (): # No moves input
            return False
        
        # Get move coordinates from first two (more will be adressed later)
        y1, x1 = moves[0][0], moves[0][1]
        y2, x2 = moves[1][0], moves[1][1]
        
        pieceMoved = self.board[y1][x1]
        
        if pieceMoved == 0: # Must move a piece
            return False
        
        # Check if it is the players turn
        if pieceMoved in (1, 3) and self.whoseMove != "white":
            return False
        elif pieceMoved in (2, 4) and self.whoseMove != "red":
            return False
        
        # Check if moves are legal
        if abs(x2-x1) > 2 or abs(y2-y1) > 2: # To big of a move
            return False
        
        if self.whoseMove == "white" and pieceMoved == 1 and (y2-y1) > 0: # White regular player cannot move backwards
            return False
        elif self.whoseMove == "red" and pieceMoved == 2 and (y2-y1) < 0: # Red regular player cannot move backwards
            return False
            
        
        elif abs(x2-x1) == 0 or abs(y2-y1) == 0: # Cannot move in a line
            return False
        
        elif abs(x2-x1) == 1: # SINGLE MOVE ------------
            
            if double_jump: # Cannot do single move when double jumping
                return False 
            
            if abs(y2-y1) >= 2: # Must be diagonal 1 space
                return False
            
            if self.board[y2][x2] != 0: # Space must be unoccupied
                return False
            
            # Otherwise, single move is valid --> Move on
            
        elif abs(x2-x1) == 2:  # JUMP ------------
            
            if abs(y2-y1) == 1 or abs(y2-y1) >= 3: # Must be diagonal 2 space
                return False
            
            average = lambda x, y: int(abs(x + y)/2)
            avY, avX = average(y1, y2), average(x1, x2)
            jumpedSpace = self.board[avY][avX]
            
            if jumpedSpace == 0: # Must be jumping another piece
                return False
            
            if self.board[y2][x2] != 0: # Space must be unoccupied
                return False
            
            if jumpedSpace in (1, 3) and self.whoseMove == "white": # Cannot jump self
                return False 
            elif jumpedSpace in (2, 4) and self.whoseMove == "red": # Cannot jump self
                return False

            # Otherwise, jump move is valid --> Move on
        
        if len(moves) <= 2:
            return True # There are no moves, all rules have been checked
        
        else:
            
            if self.whoseMove == "white" and y2 == 0 and pieceMoved == 1:
                return False # It has been made a king and must stop moving
            elif self.whoseMove == "red" and y2 == 7 and pieceMoved == 2:
                return False # It has been made a king and must stop moving
        
            copyBoard = CheckersGame(copy.deepcopy(self.board), self.whoseMove)
            copyBoard.move("", processed_moves = moves[:2], turn_switching = False)
            
            return copyBoard.isValidMove("", processed_moves = moves[1:], double_jump = True)
        
 
    # Function to print out a visual representation of the current
    # board. Original method supplied in the 1MD3 Course Assignment,
    # modified slightly by myself to display more "square"
    def __str__ (self) :
        out = "   0   1   2   3   4   5   6   7 \n ╔═══╤═══╤═══╤═══╤═══╤═══╤═══╤═══╗\n"
        i = 0
        for row in self.board :
            out += f"{str(i)}║"
            j = 0
            for item in row :
                if item == 0:
                    out += "░░░" if (i + j) % 2 == 0 else "   "
                elif item >= 1 and item <= 4:
                    out += [" ○ ", " ● ", " ♔ ", " ♚ "][item-1]
                out += "│"
                j += 1
            out = out[:-1]
            out += f"║{str(i)}\n ╟───┼───┼───┼───┼───┼───┼───┼───╢\n"
            i += 1
        out = out[:-34]
        out += "╚═══╧═══╧═══╧═══╧═══╧═══╧═══╧═══╝\n   0   1   2   3   4   5   6   7 \n"
        return out

# Function to run a game of checkers from a predefined list of moves
# or through an interactive console game.
# Original code for function supplied in the 1MD3 Course Assignment
def runGame (init = False, moveList = False) :
    game = CheckersGame()

    if (init != False) :
        game.board = init
    
    print("Checkers Initialized...")
    print(game)
    if (moveList != False) :
        print("Move List Detected, executing moves")
        for move in moveList :
            print(f"{game.whoseMove} makes move {move}\n")
            if (move == "q") :
                return
            if (move == "r") :
                clear()
                print(game)
            elif (game.isValidMove(move)) :
                game.move(move)
                print(game)
                if (game.isWon != 0) :
                    break
            else :
                print("Invalid Move")    
                
    print("Moves must be typed as coordinates (with no commas or brackets) separated by spaces. Row, then column.")
    print("Example: 54 43")
    print("When performing multiple jumps, enter each co-ordinate your piece will land on in sequence.")
    while (game.isWon == False) :
        print(f"{game.whoseMove} to move")
        move = input(">> ")
        if (move == "q") :
            return
        if (move == "r") :
                print("\nRefreshing Screen\n\n", game)
        elif (game.isValidMove(move)) :
            game.move(move)
            print(game)
            if (game.isWon != 0) :
                break
        else :
            print("Invalid Move")
    print("The Game is Finished!")
    print(f"Congratulations, {game.isWon}!")


# Here is sample game from start to end. Supplied by 1MD3 course assignment.

moves = [ '50 41'
, '23 32'
, '41 23'
, '12 34'
, '52 41'
, '21 32'
, '41 30'
, '41 52'
, '34 43'
, '56 47'
, '43 52'
, '61 43 21' # double jump
, '10 32'
, '30 21'
, '25 36'
, '21 10'
, '01 13'
, '01 12'
, '10 01'
, '14 25'
, '01 23 41' # w.king double jumps backward
, '41 32'
, '25 34'
, '41 32'
, '34 43'
, '32 21'
, '43 52'
, '72 61'
, '05 14'
, '61 50'
, '52 43'
, '52 61'
, '54 43'
, '61 72' # red gets kinged 
, '70 61'
, '36 47'
, '36 45'
, '50 41'
, '72 50 32 54 72' # round the world! Red king jumps 4, lands back in the place he started.  
, '65 54'
, '16 25'
, '21 12'
, '14 23'
, '54 36 14 32' # This is an invalid move, the final jump is backwards and therefore disallowed.  
, '54 36 14' # This is fine though.
, '72 63'
, '74 52'
, '07 16'
, '14 05'
, '27 36'
, '05 27 45'
, '03 14'
, '76 65'
, '14 25'
, '12 34 61'
, '12 34 16'
]

runGame(moveList = moves)



# From Assignment #9 - File IO and Manipulation ---------------------

'''
Write a function `converter(swagger, outfile, filters)` which takes in a swagger.yaml file input, an output json file,
and a list of filter functions. 

- If `filters` is an empty list, just clone the YAML information to JSON.
- Otherwise, the `filters` list will contain strings that are class names in the config.
    - If there are items in `filters`, your output will be a dictionary like so:

        output = {
            'openapi': '...',
            'info': { ... },
            'tags': [ ... ],
            'servers': [ ... ],
            'paths': {
                'path_including_filter_1': { ... },
                'path_including_filter_2': { ... },
            },
            'components': {
                'schemas': {
                    'filter': { ... },
                },
                'responses': { ... },
        }
        
    - `output['paths']`
        - Only include items where the path name contains the filter item (no spaces, no capitals)
    - `output['components']['schemas']`
        - Only include items where the class name is EXACTLY equal to the filter item (Spaces and Capitals allowed)
'''

import json
import yaml
# import copy # Already imported above for A8


def converter(swagger: str, outfile: str, filters: list) -> dict:
    file_content = {}
    output_data = {}
    
    out_file = outfile if outfile.endswith(".json") else outfile + ".json"
    
    try:
        with open(swagger, "r") as file:
            yaml_data = yaml.load(file, Loader=yaml.loader.SafeLoader)
    
    except Exception:
        with open(swagger + ".yaml", "r") as file:
            yaml_data = yaml.load(file, Loader=yaml.loader.SafeLoader)
        
    output = copy.deepcopy(yaml_data)
    
    if len(filters) > 0:
        
        alt_filters = [filt.lower().replace(" ", "") for filt in filters]

        for path in yaml_data['paths']:
            rem = True

            for alt_filt in alt_filters:
                if alt_filt in path:
                    rem = False
                    break

            if rem:
                output['paths'].pop(path)

        for schema in yaml_data['components']['schemas']:

            if schema not in filters:
                output['components']['schemas'].pop(schema)

        with open(out_file, "w") as file:
            json.dump(output, file)    
    
    return output

print(
    converter(
        'config1.yaml',
        'config1out.json',
        ['Auth', 'Notification']
        )
)



# Personal notes and practice - sqlite3 -----------------------------

# SQL NOTES
import sqlite3

connection = sqlite3.connect("aquarium.db")

# Cursor is an object which allows us to send and manipulate SQL commands as strings.
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS fish")
cursor.execute("CREATE TABLE IF NOT EXISTS fish (id INTEGER PRIMARY KEY, name TEXT, species TEXT, tank_number INTEGER)")

for each in [('Sammy', 'shark', 1), ('Jamie', 'cuttlefish', 7), ('Jax', 'Octopus', 7)]:
    cursor.execute("INSERT INTO fish (name, species, tank_number) VALUES (?, ?, ?)", each)
                                            #Cannot use ? and (tuple,) instead of (?, ?, ?)

cursor.execute("DELETE FROM fish WHERE name = ?", ("Sammy",)) #Ensure that values are always passed in as a tuple!
cursor.execute("UPDATE fish SET tank_number = ? WHERE name = ?" (3, "Jax"))
cursor.execute("UPDATE fish SET species = 'Micheal Jackson' WHERE name LIKE 'J%'")
connection.commit() # Update database with changes
rows = cursor.execute("SELECT * FROM fish").fetchall() # Select all from fish


# SQL Practice Question
''' QUESTION WRITTEN BY RICHIE MOTORGEANU (https://github.com/Multipixels)
    ANSWER WRITTEN BY MYSELF
Implement the function `getSongDict(database)` that will return a dictionary with the relevant data from the database.
The dictionary will have the following format.

The key for each entry should be its trackid (as a string). Value is a dictionary of relevant data.

{
    trackid (string): {
        'trackname': string,
        'genre': string,
        'genreid': int,
        'composer': string,
        'album': {
            'albumtitle': string,
            'artistname': string
         }
    },
    trackid (string): {
        'trackname': string,
        'genre': string,
        'genreid': int,
        'composer': string,
        'album': {
            'albumtitle': string,
            'artistname': string
         }
    }
}
'''
import sqlite3

def getSongDict(database):
    
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    trackParse = cursor.execute(
        "SELECT TrackId, tracks.Name, genres.Name, tracks.GenreId, Composer, albums.Title, artists.Name \
        FROM tracks, genres, albums, artists \
        WHERE tracks.GenreId = genres.GenreId \
        AND tracks.AlbumId = albums.AlbumId \
        AND albums.ArtistId = artists.ArtistId"
        ).fetchall()

    connection.close()

    return { str(each[0]): {
             'trackname': each[1],
             'genre': each[2],
             'genreid': each[3],
             'composer': each[4],
             'album': {'albumtitle': each[5], 'artistname': each[6]},
            } for each in trackParse }

print(getSongDict("chinook.db"))