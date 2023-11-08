from tile import Tile

class Horse(Tile):
    sprite = [[0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,1,1,1,1,1,0,0,0],
              [0,0,1,1,1,1,1,1,1,0,0,0],
              [0,1,1,1,1,1,1,1,1,0,0,0],
              [0,0,0,0,1,1,1,1,1,0,0,0],
              [0,0,1,1,1,1,1,1,1,1,0,0]]

    p_type = 'h'

    
    def project(self, board):
        if(self.check(self.x+2, self.y-1, board)):
            self.highlight_tile(self.x+2, self.y-1, board)

        if(self.check(self.x+1, self.y-2, board)):
            self.highlight_tile(self.x+1, self.y-2, board)

        if(self.check(self.x-1, self.y-2, board)):
            self.highlight_tile(self.x-1, self.y-2, board)

        if(self.check(self.x-2, self.y-1, board)):
            self.highlight_tile(self.x-2, self.y-1, board)

        if(self.check(self.x-2, self.y+1, board)):
            self.highlight_tile(self.x-2, self.y+1, board)

        if(self.check(self.x-1, self.y+2, board)):
            self.highlight_tile(self.x-1, self.y+2, board)

        if(self.check(self.x+1, self.y+2, board)):
            self.highlight_tile(self.x+1, self.y+2, board)

        if(self.check(self.x+2, self.y+1, board)):
            self.highlight_tile(self.x+2, self.y+1, board)
