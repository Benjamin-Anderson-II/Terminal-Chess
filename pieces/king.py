from tile import Tile 

class King(Tile):
    sprite = [[0,0,0,0,0,1,1,0,0,0,0,0],
              [0,0,0,0,1,1,1,1,0,0,0,0],
              [0,1,1,1,1,1,1,1,1,1,1,0],
              [0,1,1,0,0,1,1,0,0,1,1,0],
              [0,0,1,1,1,1,1,1,1,1,0,0],
              [0,1,1,1,1,1,1,1,1,1,1,0]]

    p_type = 'k'

    def project(self, board):
        # Right
        if(self.check(self.x+1, self.y, board)):
            self.highlight_tile(self.x+1, self.y, board)
        
        # Up
        if(self.check(self.x, self.y-1, board)):
            self.highlight_tile(self.x, self.y-1, board)

        # Left
        if(self.check(self.x-1, self.y, board)):
            self.highlight_tile(self.x-1, self.y, board)
        
        # Down
        if(self.check(self.x, self.y+1, board)):
            self.highlight_tile(self.x, self.y+1, board)

        # Up-Right
        if(self.check(self.x+1, self.y-1, board)):
            self.highlight_tile(self.x+1, self.y-1, board)
        
        # Up-Left
        if(self.check(self.x-1, self.y-1, board)):
            self.highlight_tile(self.x-1, self.y-1, board)

        # Down-Left
        if(self.check(self.x-1, self.y+1, board)):
            self.highlight_tile(self.x-1, self.y+1, board)
        
        # Down-Right
        if(self.check(self.x+1, self.y+1, board)):
            self.highlight_tile(self.x+1, self.y+1, board)

