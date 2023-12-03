from tile import Tile 

class Pawn(Tile):
    sprite =    [[0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,1,1,0,0,0,0,0],
                 [0,0,0,0,1,1,1,1,0,0,0,0],
                 [0,0,0,0,0,1,1,0,0,0,0,0],
                 [0,0,0,0,1,1,1,1,0,0,0,0],
                 [0,0,0,1,1,1,1,1,1,0,0,0]]
    p_type = 'p'

    #This will project the possible moves that the piece can take
    # @params: board is a 2d list of Tile objects
    def project(self, board, mv = True):
        v = -1 if self.is_white else 1

        if(self.check(self.x, self.y, self.x, self.y+v, board, mv) and
               board[self.y+v][self.x].p_type == '\0'):
            self.highlight_tile(self.x, self.y+v, board, mv)

        if(self.check(self.x, self.y, self.x-1, self.y+v, board, mv) and
               board[self.y+v][self.x-1].p_type != '\0'):
            self.highlight_tile(self.x-1, self.y+v, board, mv)
        
        if(self.check(self.x, self.y, self.x+1, self.y+v, board, mv) and
               board[self.y+v][self.x+1].p_type != '\0'):
            self.highlight_tile(self.x+1, self.y+v, board, mv)

        # project first move variant
        if(self.first_move):
            # check_for_mate(altered board, mv)
            if(self.check(self.x, self.y, self.x, self.y+(v*2), board, mv) and
                   board[self.y+(v*2)][self.x].p_type == '\0'):
                self.highlight_tile(self.x, self.y+(v*2), board, mv)
        return 1
