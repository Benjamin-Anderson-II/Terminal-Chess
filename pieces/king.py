from tile import Tile 

class King(Tile):
    sprite = [[0,0,0,0,0,1,1,0,0,0,0,0],
              [0,0,0,0,1,1,1,1,0,0,0,0],
              [0,1,1,1,1,1,1,1,1,1,1,0],
              [0,1,1,0,0,1,1,0,0,1,1,0],
              [0,0,1,1,1,1,1,1,1,1,0,0],
              [0,1,1,1,1,1,1,1,1,1,1,0]]

    p_type = 'k'

    def project(self, board, mv = True):
        # Right
        if(self.check(self.x, self.y, self.x+1, self.y, board, mv)):
            self.highlight_tile(self.x+1, self.y, board, mv)
        
        # Up
        if(self.check(self.x, self.y, self.x, self.y-1, board, mv)):
            self.highlight_tile(self.x, self.y-1, board, mv)

        # Left
        if(self.check(self.x, self.y, self.x-1, self.y, board, mv)):
            self.highlight_tile(self.x-1, self.y, board, mv)
        
        # Down
        if(self.check(self.x, self.y, self.x, self.y+1, board, mv)):
            self.highlight_tile(self.x, self.y+1, board, mv)

        # Up-Right
        if(self.check(self.x, self.y, self.x+1, self.y-1, board, mv)):
            self.highlight_tile(self.x+1, self.y-1, board, mv)
        
        # Up-Left
        if(self.check(self.x, self.y, self.x-1, self.y-1, board, mv)):
            self.highlight_tile(self.x-1, self.y-1, board, mv)

        # Down-Left
        if(self.check(self.x, self.y, self.x-1, self.y+1, board, mv)):
            self.highlight_tile(self.x-1, self.y+1, board, mv)
        
        # Down-Right
        if(self.check(self.x, self.y, self.x+1, self.y+1, board, mv)):
            self.highlight_tile(self.x+1, self.y+1, board, mv)

        if(not self.first_move): # must be king's first move
            return None
        if(board[self.y][self.x+3].first_move == True and # rook's first move
               self.check(self.x, self.y, self.x+1, self.y, board, mv) and # does not pass over tiles under attack
               self.check(self.x, self.y, self.x+2, self.y, board, mv)):
            self.highlight_tile(self.x+2, self.y, board, mv)
        
        if(board[self.y][self.x-4].p_type == 'r' and board[self.y][self.x-4].first_move == True and 
               self.check(self.x, self.y, self.x-1, self.y, board, mv) and 
               self.check(self.x, self.y, self.x-2, self.y, board, mv) and 
               board[self.y][self.x-3].p_type == '\0'): # space in front of rook is free
            self.highlight_tile(self.x-2, self.y, board, mv)
