import sys 
sys.path.insert(1, "pieces")

from getkey import getkey, keys

from tile import Tile
from pawn import Pawn
from rook import Rook
from horse import Horse
from king import King
from queen import Queen
from bishop import Bishop

class Game:
    def __init__(self):
        self.board = [[Tile(x,y, None) for x in range(8)] for y in range(8)]
        self.cursor_x = self.cursor_y = 0
        self.add_pieces(True)
        self.add_pieces(False)
        self.board[3][3] = Queen (3, 3, False)
        self.board[4][4] = Horse (4, 4, False)
        self.board[4][2] = Rook  (2, 4, True)
        self.board[4][5] = Bishop(5, 4, False)
        self.board[5][6] = Pawn  (6, 5, True)
        self.board[3][1] = King  (1, 3, False)
        self.board[5][6].first_move = False
        self.print_board()

    def highlight_curr_tile(self, h = True):
        self.board[self.cursor_y][self.cursor_x].highlight = h
        print(self.board[self.cursor_y][self.cursor_x], end="")
        print("\033[0;49m\033[48;1H")

    # Pre Game is created and no modifications have been made to the object
    def play(self):
        self.cursor_y = 6;
        self.highlight_curr_tile()
        while(1):
            key = getkey()
            if   key == keys.UP:
                if(self.cursor_y <= 0):
                    continue
                self.highlight_curr_tile(False)
                self.cursor_y -= 1
                self.highlight_curr_tile()
            elif key == keys.DOWN:
                if(self.cursor_y >= 7):
                    continue
                self.highlight_curr_tile(False)
                self.cursor_y += 1
                self.highlight_curr_tile()
            elif key == keys.LEFT:
                if(self.cursor_x <= 0):
                    continue
                self.highlight_curr_tile(False)
                self.cursor_x -= 1
                self.highlight_curr_tile()
            elif key == keys.RIGHT:
                if(self.cursor_x >= 7):
                    continue
                self.highlight_curr_tile(False)
                self.cursor_x += 1
                self.highlight_curr_tile()
#            elif key == 'h':
#            elif key == 'r':
#            elif key == 'n':
            elif key == 'q':
                break
            elif key == keys.ENTER:
                self.board[self.cursor_y][self.cursor_x].project(self.board)
                print("\033[0;49m\033[48;1H")
                
    def add_pieces(self, is_white):
        major_row = 7 if is_white else 0
        minor_row = 6 if is_white else 1

        for i in range(8):
            self.board[minor_row][i] = Pawn(i, minor_row, is_white)

        self.board[major_row][0] =   Rook(0, major_row, is_white)
        self.board[major_row][1] =  Horse(1, major_row, is_white)
        self.board[major_row][2] = Bishop(2, major_row, is_white)
        self.board[major_row][3] =  Queen(3, major_row, is_white)
        self.board[major_row][4] =   King(4, major_row, is_white)
        self.board[major_row][5] = Bishop(5, major_row, is_white)
        self.board[major_row][6] =  Horse(6, major_row, is_white)
        self.board[major_row][7] =   Rook(7, major_row, is_white)

    def print_board(self):
        s = ""
        for i in range(8):
            for j in range(8):
                s += str(self.board[j][i])
        s += "\033[0;49m\033[1;%dH" % 97
        s += " _____             _             _\033[1B\033[34D"
        s += "/  __ \           | |           | |\033[1B\033[35D"
        s += "| /  \/ ___  _ __ | |_ _ __ ___ | |___\033[1B\033[38D"
        s += "| |    / _ \| '__\| __| '__/ _ \| / __|\033[1B\033[39D"
        s += "| \__/\ (_) | | | | |_| |  |(_) | \__ \\\033[1B\033[39D"
        s += " \____/\___/|_| |_|\__|_|  \___/|_|___/\033[2B\033[38D"
        s += "Press the Arrow Keys to move around\033[1B\033[35D"
        s += "Press ENTER to select and de-select pieces\033[1B\033[42D"
        s += "press Q to Quit\033[1B\033[15D"
        print(s, end="")


#TODO:
#- create Player
#- give them their pieces based on their color
#- print the pieces in the print_board function
#- create getters and setters for piece locations
# figure out a way to read what piece is at what locations
#  OR
# figure out how to make a clickable UI in the terminal and get pieces that way (prob harder)
# allow each piece to highlight their possible moves (no check calcs yet)
# allow pieces to move to those locations
# calculate check before highlighting (hand off)
# Implement Pawn Promotion
# Implement Castling
# Implement En Passant
# Make Board Bigger (or at least the pieces within each tile)
