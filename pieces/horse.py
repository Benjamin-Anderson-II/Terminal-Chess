from tile import Tile

class Horse(Tile):
    sprite = [[0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,1,1,1,1,1,0,0,0],
              [0,0,1,1,1,1,1,1,1,0,0,0],
              [0,1,1,1,1,1,1,1,1,0,0,0],
              [0,0,0,0,1,1,1,1,1,0,0,0],
              [0,0,1,1,1,1,1,1,1,1,0,0]]

    p_type = 'h'

    
    def project(self, board, mv = True):
        if(self.check(self.x, self.y, self.x+2, self.y-1, board, mv)):
            self.highlight_tile(self.x+2, self.y-1, board, mv)

        if(self.check(self.x, self.y, self.x+1, self.y-2, board, mv)):
            self.highlight_tile(self.x+1, self.y-2, board, mv)

        if(self.check(self.x, self.y, self.x-1, self.y-2, board, mv)):
            self.highlight_tile(self.x-1, self.y-2, board, mv)

        if(self.check(self.x, self.y, self.x-2, self.y-1, board, mv)):
            self.highlight_tile(self.x-2, self.y-1, board, mv)

        if(self.check(self.x, self.y, self.x-2, self.y+1, board, mv)):
            self.highlight_tile(self.x-2, self.y+1, board, mv)

        if(self.check(self.x, self.y, self.x-1, self.y+2, board, mv)):
            self.highlight_tile(self.x-1, self.y+2, board, mv)

        if(self.check(self.x, self.y, self.x+1, self.y+2, board, mv)):
            self.highlight_tile(self.x+1, self.y+2, board, mv)

        if(self.check(self.x, self.y, self.x+2, self.y+1, board, mv)):
            self.highlight_tile(self.x+2, self.y+1, board, mv)
