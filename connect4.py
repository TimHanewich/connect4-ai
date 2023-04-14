
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


