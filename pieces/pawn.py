from tile import Tile 

class Pawn(Tile):
    sprite =    [[0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,1,1,0,0,0,0,0],
                 [0,0,0,0,1,1,1,1,0,0,0,0],
                 [0,0,0,0,0,1,1,0,0,0,0,0],
                 [0,0,0,0,1,1,1,1,0,0,0,0],
                 [0,0,0,1,1,1,1,1,1,0,0,0]]
    p_type = 'p'

#    def __str__(self):
#        s = self.color + self.cursor_to_self()
#
#        s += "\033[1B\033[5C"
#        s +=   "  \033[1B\033[3D"
#        s +=  "    \033[1B\033[3D"
#        s +=   "  \033[1B\033[3D"
#        s +=  "    \033[1B\033[5D"
#        s += "      "
#        return s

    #This will project the possible moves that the piece can take
    # @params: board is a 2d list of Tile objects
    def project(self, board):
        # project normal moves
        # check_for_mate(altered board)
        # check_for_block
        v = -1 if self.is_white else 1
        #Can't project anything if something is blocking first move
        if(board[self.y+v][self.x].p_type != '\0'):
            return None

        self.highlight_tile(self.x, self.y+v, board)

        if(self.check(self.x-1, self.y+v, board) and
               board[self.y+v][self.x-1].p_type != '\0'):
            self.highlight_tile(self.x-1, self.y+v, board)
        
        if(self.check(self.x+1, self.y+v, board) and
               board[self.y+v][self.x+1].p_type != '\0'):
            self.highlight_tile(self.x+1, self.y+v, board)

        # project first move variant
        if(self.first_move):
            # check_for_mate(altered board)
            if(board[self.y+(v*2)][self.x].p_type != '\0'):
                return None
            self.highlight_tile(self.x, self.y+(v*2), board)
    #def promote(): # promotes pawn when they reach the other side

