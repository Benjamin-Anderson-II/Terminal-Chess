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
        self.selected = False
        self.first_move  = True

    def cursor_to_xy(self, x, y):
        return "\033[%d;%dH" % (y*self.size+1,
                                x*self.size*2+1)

    def set_xy(self,  x, y):
        self.x = x
        self.y = y
        self.tile_color = "\033[31;47m" if (x+y)%2==0 else "\033[31;42m"

    def __str__(self):
        # add highlight feature w/ blue 0s in circle pattern
        # determine "black or white" based off of X and Y for background
        s = self.cursor_to_xy(self.x, self.y)
        for i in range(len(self.sprite)):
            for j in range(len(self.sprite[i])):
                s += self.piece_color if self.sprite[i][j] else self.tile_color
                pad = 1
                if (i < pad     or i > len(self.sprite)     - 1 -  pad or
                    j < pad * 2 or j > len(self.sprite[i]) - 1 - (pad * 2)):
                    s += "@" if self.highlight else " "
                else:
                    s += "\033[34m@" if self.selected else " "
            s += "\033[1B\033[%dD" % (2*self.size)

        return s

    def find_king(self, board):
        for i in range(len(board)):
            for j in range(len(board[i])):
                tile = board[i][j]
                if tile.p_type == 'k' and tile.is_white == self.is_white:
                    return (j, i)
        return (-1,-1)

    def check(self, curr_x, curr_y, dest_x, dest_y, board, mv = True):
        if ((dest_y < 0 or dest_y >= 8) or # y out of bounds
            (dest_x < 0 or dest_x >= 8) or # x out of bounds
            (board[dest_y][dest_x].p_type != '\0' and # piece is on tile
             board[dest_y][dest_x].piece_color == self.piece_color)): # and is same color as self
            return False

        if(not mv):
            return True

        curr_tile = board[curr_y][curr_x]
        curr_p_type = curr_tile.p_type
        retval = True
        dest_tile = board[dest_y][dest_x]
        dest_p_type = dest_tile.p_type
        board[dest_y][dest_x] = curr_tile
        board[curr_y][curr_x] = Tile(curr_x, curr_y, None)
        king_x, king_y = self.find_king(board)
        for i in board:
            for tile in i:
                if(tile.piece_color != self.piece_color and 
                       tile.p_type != '\0'):
                    tile.project(board, False)
                    if(board[king_y][king_x].highlight == True):
                        retval = False
                    tile.project(board, False)

        board[dest_y][dest_x] = dest_tile
        board[curr_y][curr_x] = curr_tile

        return retval

    def highlight_tile(self, x, y, board, mv):
        board[y][x].highlight = not (board[y][x].highlight)
        if(mv):
            print(board[y][x], end="")

    def project(self, board):
        return None
