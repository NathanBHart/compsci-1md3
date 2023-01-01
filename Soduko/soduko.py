import copy


class TooManyChoices(Exception):
    pass
    
class NoChoices(Exception):
    pass

class UnsolvablePuzzle(Exception):
    pass


class SudokuPuzzle(object):
    def __init__(self, board: list = None):
        """
        Make a copy of the input board. If input board is None, create board of 0s.

        Original method supplied by Mark Hutchison and Dr. Nicholas Moore from the 1MD3 Course 2022
        """
        if board is not None and \
                len(board) == 9 and \
                all(len(row) == 9 for row in board) and \
                all(0 <= board[row][col] <= 9
                    for col in range(9)
                    for row in range(9)
                ):
            self.board: list = [[cell for cell in row] for row in board]
        else:
            self.board: list = [[0 for _ in range(9)] for _ in range(9)]

    def __str__(self) -> str:
        '''
        Create a string representation of the current board that can be effectively printed to a console

        Original method supplied by Mark Hutchison and Dr. Nicholas Moore from the 1MD3 Course 2022
        '''
        puzzle: str = "╔" + ("═══╦" * 8) + "═" * 3 + "╗\n"
        for row_index, row in enumerate(self.board):
            puzzle += "║"
            for col_index, cell in enumerate(row):
                puzzle += f" {cell if cell not in [0, None] else ' '} ║"
            if row_index < 8:
                puzzle += "\n╠" + ("═══╬" * 8) + "═══╣\n"
            else:
                puzzle += '\n'
        return puzzle + "╚" + "═══╩" * 8 + "═" * 3 + "╝\n"

    def __eq__(self, other) -> bool:
        '''
        Allows two soduko boards to be equated.

        # Original method supplied by Mark Hutchison and Dr. Nicholas Moore from the 1MD3 Course 2022
        '''
        return all(
            self.board[row][col] == other.board[row][col]
            for row in range(9) 
            for col in range(9)
        )


    def all_filled(self) -> bool:
        '''
        Method returns true if all cells are filled with a nonzero entry.
        '''
        return 0 not in [x for row in self.board for x in row]


    def horizontal_check(self, row, value):
        '''
        Method returns true if a given value does not already occur
        in a specified row.        
        '''
        return value not in self.board[row]


    def vertical_check(self, col, value):
        '''
        Method returns true if a given value does not already occur
        in a specified column.        
        '''
        return value not in [
            self.board[x][col]for x in range(len(self.board))
        ]
    

    def sub_square_check(self, x, y, value):
        '''
        Method returns true if a given value at a given location does
        not already occur in it's parent 3x3 subsquare.        
        '''
        top_x = (x//3) * 3
        top_y = (y//3) * 3
        
        subsquare = [self.board[ran_y][top_x:top_x+3] for ran_y in range(top_y, top_y+3)]

        return value not in [x for row in subsquare for x in row]

    def apply_strategy(self, strategy):
        '''
        Method applies a given strategy to an entire board, mutating
        any cells for which a strategy works. Returns True only if at
        least one cell was sucessfully motated for the given strategy.
        '''
        passed = False
        
        for x in range(9):
            for y in range(9):
                if self.board[y][x] == 0:
                    try:
                        self.board[y][x] = strategy(self, x, y)
                        passed = True
                    except Exception:
                        pass
                
        return passed

    def solve(self, strategies):
        '''
        Attempts to solve a board given a list of strategies.
        If the board cannot be solved by alternating between the
        provided strategies, it will attempt a recursive brute force
        solution (while using the provided strategies to optimize time).

        If a board is invalid (cannot be solved even with brute force),
        it will raise a UnsolvablePuzzle exception.
        '''

        def target(self):

            for y in range(9):
                for x in range(9):

                    if self.board[y][x] != 0:
                        continue

                    nums = {1,2,3,4,5,6,7,8,9}
        
                    for i in range(1, 9+1):
                        
                        if not self.horizontal_check(y, i) or \
                                not self.vertical_check(x, i) or \
                                not self.sub_square_check(x, y, i):
                            nums.discard(i)

                    return (x, y), nums

        
        while not self.all_filled():
        
            stale = True

            for strategy in strategies:
                test = self.apply_strategy(strategy)
                if test:
                    stale = False

            if stale:

                target_cell = target(self) # Will run strategies first
                    # brute force is a fall back strategy I decided to implement

                for each in target_cell[1]:

                    x = target_cell[0][0]
                    y = target_cell[0][1]
                    
                    new_board = copy.deepcopy(self)
                    new_board.board[y][x] = each

                    try:
                        new_board.solve(strategies)
                        
                        self.board = new_board.board
                        
                        return True
                    except Exception:
                        pass

                raise UnsolvablePuzzle
                
        return True


def elimination_strategy(self, x, y):
        '''
        Method applies elimination strategy to a given cell, returning
        the only value that can work in that cell (assuming there is
        only one possible value). If there are multiple valid values
        for the current board layout, a TooManyChoices exception will
        be raised. If there are no valid options for the cell a
        NoChoices exception will be raised.  
        '''
        nums = {1,2,3,4,5,6,7,8,9}
        
        for i in range(1, 9+1):
            
            if not self.horizontal_check(y, i) or \
                    not self.vertical_check(x, i) or \
                    not self.sub_square_check(x, y, i):
                nums.discard(i)
        
        if len(nums) == 1:
            return list(nums)[0]
        elif len(nums) > 1:
            raise TooManyChoices
        else:
            raise NoChoices 


def load_puzzle(file_name, puzzle_name):
    import json
    
    try:
        with open(file_name, "r") as fh:
            return SudokuPuzzle(json.load(fh)[puzzle_name])
    except Exception:
        with open(file_name + ".json", "r") as fh:
            return SudokuPuzzle(json.load(fh)[puzzle_name])


puzzle = load_puzzle("A10_puzzles.json", "medium")

print("Unsolved Puzzle:")
print(puzzle)

puzzle.solve([elimination_strategy]) 

print("Solved Puzzle:")
print(puzzle)