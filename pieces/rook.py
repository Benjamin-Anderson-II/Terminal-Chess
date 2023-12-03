from tile import Tile

# TODO:
## Make highlighted versions for the sprites
## make all of the sprites print through their sprite arrays

class Rook(Tile):
    sprite = [[0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,1,1,0,1,1,0,1,1,0,0],
              [0,0,1,1,1,1,1,1,1,1,0,0],
              [0,0,0,1,1,1,1,1,1,0,0,0],
              [0,0,0,1,1,1,1,1,1,0,0,0],
              [0,0,1,1,1,1,1,1,1,1,0,0]]
    p_type = 'r'

    def project(self, board, mv = True):
        # Right
        for i in range(self.x+1, 8):# inclusive, exclusive
            if(self.check(self.x, self.y, i, self.y, board, mv)):
                self.highlight_tile(i, self.y, board, mv)
            if(board[self.y][i].p_type !='\0'):
                break
        
        # Up
        for i in range(self.y-1, -1, -1):# inclusive, exclusive
            if(self.check(self.x, self.y, self.x, i, board, mv)):
                self.highlight_tile(self.x, i, board, mv)
            if(board[i][self.x].p_type !='\0'):
                break

        # Left
        for i in range(self.x-1, -1, -1):# inclusive, exclusive
            if(self.check(self.x, self.y, i, self.y, board, mv)):
                self.highlight_tile(i, self.y, board, mv)
            if(board[self.y][i].p_type !='\0'):
                break
        
        # Down
        for i in range(self.y+1, 8):# inclusive, exclusive
            if(self.check(self.x, self.y, self.x, i, board, mv)):
                self.highlight_tile(self.x, i, board, mv)
            if(board[i][self.x].p_type !='\0'):
                break

