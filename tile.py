class Tile:
    size = 6
    sprite =  [[0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0]]
    p_type = '\0'

    def __init__(self, x, y, is_white):
        self.x = x
        self.y = y
        self.is_white = is_white
        self.piece_color = "\033[31;43m" if self.is_white else "\033[31;40m"
        self.tile_color  = "\033[31;47m" if (x+y)%2==0 else "\033[31;42m"
        self.highlight = False
        self.first_move  = True

    def cursor_to_xy(self, x, y):
        return "\033[%d;%dH" % (y*self.size+1,
                                x*self.size*2+1)

    def __str__(self):
        # add highlight feature w/ blue 0s in circle pattern
        # determine "black or white" based off of X and Y for background
        s = self.cursor_to_xy(self.x, self.y)
        for i in self.sprite:
            for j in i:
                s += self.piece_color if j else self.tile_color
                s += "@" if self.highlight else " "
            s += "\033[1B\033[%dD" % (2*self.size)

        return s

    def check(self, x, y, board):
        if ((y < 0 or y >= 8) or # y out of bounds
            (x < 0 or x >= 8) or # x out of bounds
            (board[y][x].p_type != '\0' and # piece is on tile
             board[y][x].piece_color == self.piece_color)): # and is same color as self
            return False

        return True

    def highlight_tile(self, x, y, board):
        board[y][x].highlight = not (board[y][x].highlight)
        print(board[y][x], end="")

    def project(self, board):
        return None
