import math


class game:

    def __init__(self) -> None:
        
        # arrays
        self.board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]] # Reads like english riding, left to right, then top to bottom. first one would be top-left. Then move to the right, right again, right again, etc. Then down, then right, then right, etc.

    def print(self) -> None:

        ToReturn:str = ""

        for row in self.board:
            for col in row:
                ToReturn = ToReturn + str(col) + "   "
            ToReturn = ToReturn[0:len(ToReturn) - 3]
            ToReturn = ToReturn + "\n"
        ToReturn = ToReturn[0:len(ToReturn)-1]

        print(ToReturn)
    
    def set(self, row:int, column:int, value:int) -> None:
        self.board[row - 1][column - 1] = value
    
    # what is occupying that position? Is it empty (0), or 1 or -1?
    def occupying(self, row:int, column:int) -> int:
        val = self.board[row - 1][column - 1]
        return val
        

    # drop a token in one of the 7 columns
    def drop(self, value:int, column:int) -> None:

        row1 = self.occupying(1, column)
        row2 = self.occupying(2, column)
        row3 = self.occupying(3, column)
        row4 = self.occupying(4, column)
        row5 = self.occupying(5, column)
        row6 = self.occupying(6, column)

        if row6 == 0:
            self.set(6, column, value)
        elif row5 == 0:
            self.set(5, column, value)
        elif row4 == 0:
            self.set(4, column, value)
        elif row3 == 0:
            self.set(3, column, value)
        elif row2 == 0:
            self.set(2, column, value)
        elif row1 == 0:
            self.set(1, column, value)
        else:
            raise Exception("Invalid move! Unable to drop value '" + str(value) + "' on column '" + str(column) + "'. That column is full.")

    # if a particular value (player) is winning
    def winning_for(self, value:int) -> bool:

        # Check horizontal locations for win
        for c in range(4):
            for r in range(6):
                if self.board[r][c] == value and self.board[r][c+1] == value and self.board[r][c+2] == value and self.board[r][c+3] == value:
                    return True
    
        # Check vertical locations for win
        for c in range(7):
            for r in range(3):
                if self.board[r][c] == value and self.board[r+1][c] == value and self.board[r+2][c] == value and self.board[r+3][c] == value:
                    return True
    
        # Check positively sloped diaganols
        for c in range(4):
            for r in range(3):
                if self.board[r][c] == value and self.board[r+1][c+1] == value and self.board[r+2][c+2] == value and self.board[r+3][c+3] == value:
                    return True
    
        # Check negatively sloped diaganols
        for c in range(7-3):
            for r in range(3, 6):
                if self.board[r][c] == value and self.board[r-1][c+1] == value and self.board[r-2][c+2] == value and self.board[r-3][c+3] == value:
                    return True

        # if it got this far, no, nobody has won
        return False
    
    # if either side is winning
    def winning(self) -> bool:
        
        if self.winning_for(1) or self.winning_for(-1):
            return True
        else:
            return False

    def longest_connect(self, value:int) -> int:

        max_seen:int = 0
        
        # verticals
        max_seen = max(max_seen, self.__longest_connect__(1, 1, 1, 0, value))
        max_seen = max(max_seen, self.__longest_connect__(1, 2, 1, 0, value))
        max_seen = max(max_seen, self.__longest_connect__(1, 3, 1, 0, value))
        max_seen = max(max_seen, self.__longest_connect__(1, 4, 1, 0, value))
        max_seen = max(max_seen, self.__longest_connect__(1, 5, 1, 0, value))
        max_seen = max(max_seen, self.__longest_connect__(1, 6, 1, 0, value))
        max_seen = max(max_seen, self.__longest_connect__(1, 7, 1, 0, value))

        # horizontals
        max_seen = max(max_seen, self.__longest_connect__(1, 1, 0, 1, value))
        max_seen = max(max_seen, self.__longest_connect__(2, 1, 0, 1, value))
        max_seen = max(max_seen, self.__longest_connect__(3, 1, 0, 1, value))
        max_seen = max(max_seen, self.__longest_connect__(4, 1, 0, 1, value))
        max_seen = max(max_seen, self.__longest_connect__(5, 1, 0, 1, value))
        max_seen = max(max_seen, self.__longest_connect__(6, 1, 0, 1, value))

        # diaganols
        max_seen = max(max_seen, self.__longest_connect__(1, 1, -1, 1, value))
        max_seen = max(max_seen, self.__longest_connect__(2, 1, -1, 1, value))
        max_seen = max(max_seen, self.__longest_connect__(3, 1, -1, 1, value))
        max_seen = max(max_seen, self.__longest_connect__(4, 1, -1, 1, value))
        max_seen = max(max_seen, self.__longest_connect__(5, 1, -1, 1, value))
        max_seen = max(max_seen, self.__longest_connect__(6, 1, -1, 1, value))
        max_seen = max(max_seen, self.__longest_connect__(6, 2, -1, 1, value))
        max_seen = max(max_seen, self.__longest_connect__(6, 3, -1, 1, value))
        max_seen = max(max_seen, self.__longest_connect__(6, 4, -1, 1, value))
        max_seen = max(max_seen, self.__longest_connect__(6, 5, -1, 1, value))
        max_seen = max(max_seen, self.__longest_connect__(6, 6, -1, 1, value))
        max_seen = max(max_seen, self.__longest_connect__(6, 7, -1, 1, value))

        return max_seen
        
    def __longest_connect__(self, start_row:int, start_col:int, row_add:int, col_add:int, value:int) -> int:
        
        on_row:int = start_row
        on_col:int = start_col

        on_chain:int = 0
        longest_seen:int = 0

        while True:

            # test
            occ = self.occupying(on_row, on_col)
            if occ == value:
                on_chain = on_chain + 1
            else:
                if on_chain > longest_seen:
                    longest_seen = on_chain
                on_chain = 0

            # increment
            on_row = on_row + row_add
            on_col = on_col + col_add

            # if we are over, quit
            if on_row > 6:
                return max(longest_seen, on_chain)
            elif on_col > 7:
                return max(longest_seen, on_chain)
                


