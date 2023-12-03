from tile import Tile 

class Bishop(Tile):
    sprite = [[0,0,0,0,1,1,1,1,0,0,0,0],
              [0,0,0,0,0,0,1,1,1,0,0,0],
              [0,0,0,1,1,1,1,1,1,0,0,0],
              [0,0,0,0,1,1,1,1,0,0,0,0],
              [0,0,0,1,1,1,1,1,1,0,0,0],
              [0,0,1,1,1,1,1,1,1,1,0,0]]

    p_type = 'b'

    def project(self, board, mv = True):
        # Up-Right
        for i in range(1, 8):
            if(not self.check(self.x, self.y, self.x+i, self.y-i, board, mv)):
                break
            self.highlight_tile(self.x+i, self.y-i, board, mv)
            if(board[self.y-i][self.x+i].p_type !='\0'):
                break
        
        # Up-Left
        for i in range(1, 8):
            if(not self.check(self.x, self.y, self.x-i, self.y-i, board, mv)):
                break
            self.highlight_tile(self.x-i, self.y-i, board, mv)
            if(board[self.y-i][self.x-i].p_type !='\0'):
                break

        # Down-Left
        for i in range(1, 8):
            if(not self.check(self.x, self.y, self.x-i, self.y+i, board, mv)):
                break
            self.highlight_tile(self.x-i, self.y+i, board, mv)
            if(board[self.y+i][self.x-i].p_type !='\0'):
                break
        
        # Down-Right
        for i in range(1, 8):
            if(not self.check(self.x, self.y, self.x+i, self.y+i, board, mv)):
                break
            self.highlight_tile(self.x+i, self.y+i, board, mv)
            if(board[self.y+i][self.x+i].p_type !='\0'):
                break

