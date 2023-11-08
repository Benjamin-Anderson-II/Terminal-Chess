from tile import Tile

class Queen(Tile):
    sprite = [[0,0,0,0,0,1,1,0,0,0,0,0],
              [0,0,1,1,0,1,1,0,1,1,0,0],
              [0,0,0,1,1,1,1,1,1,0,0,0],
              [0,0,0,0,1,1,1,1,0,0,0,0],
              [0,0,0,0,1,1,1,1,0,0,0,0],
              [0,0,1,1,1,1,1,1,1,1,0,0]]

    p_type = 'q'

    def project(self, board):
        # Right
        for i in range(self.x+1, 8):# inclusive, exclusive
            if(not self.check(i, self.y, board)):
                break
            self.highlight_tile(i, self.y, board)
            if(board[self.y][i].p_type !='\0'):
                break

        # Up
        for i in range(self.y-1, -1, -1):# inclusive, exclusive
            if(not self.check(self.x, i, board)):
                break
            self.highlight_tile(self.x, i, board)
            if(board[i][self.x].p_type !='\0'):
                break

        # Left
        for i in range(self.x-1, -1, -1):# inclusive, exclusive
            if(not self.check(i, self.y, board)):
                break
            self.highlight_tile(i, self.y, board)
            if(board[self.y][i].p_type !='\0'):
                break

        # Down
        for i in range(self.y+1, 8):# inclusive, exclusive
            if(not self.check(self.x, i, board)):
                break
            self.highlight_tile(self.x, i, board)
            if(board[i][self.x].p_type !='\0'):
                break

        # Up-Right
        for i in range(1, 8):
            if(not self.check(self.x+i, self.y-i, board)):
                break
            self.highlight_tile(self.x+i, self.y-i, board)
            if(board[self.y-i][self.x+i].p_type !='\0'):
                break

        # Up-Left
        for i in range(1, 8):
            if(not self.check(self.x-i, self.y-i, board)):
                break
            self.highlight_tile(self.x-i, self.y-i, board)
            if(board[self.y-i][self.x-i].p_type !='\0'):
                break

        # Down-Left
        for i in range(1, 8):
            if(not self.check(self.x-i, self.y+i, board)):
                break
            self.highlight_tile(self.x-i, self.y+i, board)
            if(board[self.y+i][self.x-i].p_type !='\0'):
                break

        # Down-Right
        for i in range(1, 8):
            if(not self.check(self.x+i, self.y+i, board)):
                break
            self.highlight_tile(self.x+i, self.y+i, board)
            if(board[self.y+i][self.x+i].p_type !='\0'):
                break

