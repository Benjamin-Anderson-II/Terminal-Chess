from tile import Tile

class Queen(Tile):
    sprite = [[0,0,0,0,0,1,1,0,0,0,0,0],
              [0,0,1,1,0,1,1,0,1,1,0,0],
              [0,0,0,1,1,1,1,1,1,0,0,0],
              [0,0,0,0,1,1,1,1,0,0,0,0],
              [0,0,0,0,1,1,1,1,0,0,0,0],
              [0,0,1,1,1,1,1,1,1,1,0,0]]

    p_type = 'q'

    def project(self, board, mv = True):
        # Right
        for i in range(self.x+1, 8):# inclusive, exclusive
            if(not self.check(self.x, self.y, i, self.y, board, mv)):
                break
            self.highlight_tile(i, self.y, board, mv)
            if(board[self.y][i].p_type !='\0'):
                break

        # Up
        for i in range(self.y-1, -1, -1):# inclusive, exclusive
            if(not self.check(self.x, self.y, self.x, i, board, mv)):
                break
            self.highlight_tile(self.x, i, board, mv)
            if(board[i][self.x].p_type !='\0'):
                break

        # Left
        for i in range(self.x-1, -1, -1):# inclusive, exclusive
            if(not self.check(self.x, self.y, i, self.y, board, mv)):
                break
            self.highlight_tile(i, self.y, board, mv)
            if(board[self.y][i].p_type !='\0'):
                break

        # Down
        for i in range(self.y+1, 8):# inclusive, exclusive
            if(not self.check(self.x, self.y, self.x, i, board, mv)):
                break
            self.highlight_tile(self.x, i, board, mv)
            if(board[i][self.x].p_type !='\0'):
                break

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

