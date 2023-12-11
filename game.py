import sys 
sys.path.insert(1, "pieces")

from getkey import getkey, keys

import tui_api as api
import qa_api as qa
from tile import Tile
from pawn import Pawn
from rook import Rook
from horse import Horse
from king import King
from queen import Queen
from bishop import Bishop

class Game:
    def __init__(self, socket):
        self.socket = socket
        self.board = [[Tile(x,y, None) for x in range(8)] for y in range(8)]
        self.cursor_x = self.cursor_y = 0
        self.add_pieces(True)
        self.add_pieces(False)
        self.controls_win = self.print_controls()
        self.make_material_windows(True)
        self.print_board()

    def highlight_curr_tile(self, h = True):
        retval = self.board[self.cursor_y][self.cursor_x].highlight
        self.board[self.cursor_y][self.cursor_x].selected = h
        print(self.board[self.cursor_y][self.cursor_x], end="")
        print("\033[0;49m\033[48;1H")
        return retval

    def select(self, dir):
        self.highlight_curr_tile(False)
        #self.board[self.cursor_y][self.cursor_y].selected = False
        if dir == "UP":
            self.cursor_y -= 1
        elif dir == "DOWN":
            self.cursor_y += 1
        elif dir == "LEFT":
            self.cursor_x -= 1
        elif dir == "RIGHT":
            self.cursor_x += 1
        #self.board[self.cursor_y][self.cursor_x].selected = True
        return self.highlight_curr_tile()

    def make_material_windows(self, first_time = False):
        if not first_time:
            api.exit_window(self.socket, 1)
            api.exit_window(self.socket, 1)
        self.white_material = api.create_window(self.socket, 1, Tile.size*8+2, 40, 1, 
                                           prompt = qa.get_pieces(False), h_align = "L")
        self.black_material = api.create_window(self.socket, 1, 1, 40, 1, 
                                           prompt = qa.get_pieces(True), h_align = "L")

    def move_piece(self, proj_x, proj_y):
        if self.board[self.cursor_y][self.cursor_x].highlight: 
            # unproject 
            self.board[proj_y][proj_x].project(self.board)
            
            #call partner's microservice
            print("\033[51H")
            qa.add_piece(not self.board[proj_y][proj_x].is_white, 
                         self.board[self.cursor_y][self.cursor_x].p_type)
            # print()

            ### Check if Castling
            if (self.board[proj_y][proj_x].p_type == 'k' and 
                (proj_x+2 == self.cursor_x or proj_x-2 == self.cursor_x)):
                #move the rook to the other side of the king
                mv_x = proj_x+int((self.cursor_x-proj_x)/2)
                rk_x = 0 if mv_x<proj_x else 7
                self.board[proj_y][rk_x].first_move = False
                self.board[proj_y][rk_x].set_xy(mv_x, proj_y)
                self.board[proj_y][mv_x] = self.board[proj_y][rk_x]
                self.board[proj_y][rk_x] = Tile(rk_x, proj_y, None)
                print(self.board[proj_y][rk_x], end = "")
                print(self.board[proj_y][mv_x], end = "")

            # move piece
            self.board[self.cursor_y][self.cursor_x] = self.board[proj_y][proj_x]
            self.board[proj_y][proj_x] = Tile(proj_x, proj_y, None)
            self.board[self.cursor_y][self.cursor_x].set_xy(self.cursor_x, self.cursor_y)
            self.board[self.cursor_y][self.cursor_x].selected = True
            self.board[self.cursor_y][self.cursor_x].first_move = False
        
            # Print Changed Tiles
            print(self.board[self.cursor_y][self.cursor_x], end = "")
            print(self.board[proj_y][proj_x], end = "")
            self.make_material_windows()
            return True

        return False

    def project_piece(self, proj_x, proj_y, white):
        if(white != self.board[self.cursor_y][self.cursor_x].is_white):
            return [-1,-2]
        curr_tile = self.board[self.cursor_y][self.cursor_x]
        if proj_x == -1:
            curr_tile.project(self.board)
            for i in self.board:
                for tile in i:
                    if tile.highlight:
                        return [self.cursor_x, self.cursor_y]
            return [-1,-2]
        elif (proj_x == self.cursor_x and
              proj_y == self.cursor_y):
            curr_tile.project(self.board)
            return [-1,-1]
        else:
            return [-1,-2]

    def make_promote_win(self, rook_txt, knight_txt, bishop_txt, queen_txt, is_white, tile_size):
        txt_col = ""
        win_x = x = tile_size*4-2
        win_y = 0
        if is_white:
            txt_col = "Y"
            win_y = tile_size-1
        else:
            txt_col = "K"
            win_y = tile_size * 6 - 1
        choose_win = api.create_window(self.socket, 
                                       win_x, 
                                       win_y, 
                                       tile_size*8+7, 
                                       tile_size+6, 
                                       prompt = " \n \n    Promotion!!", 
                                       win_bg_col = "B",
                                       hgl_txt_col = txt_col,
                                       hgl_bg_col = "R",
                                       parent_win = self.controls_win)
        rook_btn = api.create_button(self.socket,
                                     2, 6,
                                     rook_txt,
                                     txt_col, "G", 0)
        knight_btn = api.create_button(self.socket,
                                       3 + tile_size*2, 6,
                                       knight_txt,
                                       txt_col, "G", 0)
        bishop_btn = api.create_button(self.socket,
                                       4 + tile_size*2*2, 6,
                                       bishop_txt,
                                       txt_col, "G", 0)
        queen_btn = api.create_button(self.socket,
                                      5 + tile_size*2*3, 6,
                                      queen_txt,
                                      txt_col, "G", 0)
        curr_btn = api.search_button(self.socket, "{%s}" % (rook_txt))
        while(1):
            key = getkey()
            if   key == keys.LEFT:
                curr_btn = api.search_button(self.socket, "-x")
            elif key == keys.RIGHT:
                curr_btn = api.search_button(self.socket, "+x")
            elif key == keys.ENTER:
                if curr_btn == rook_btn:
                    self.board[self.cursor_y][self.cursor_x] = Rook(self.cursor_x, self.cursor_y, is_white)
                elif curr_btn == knight_btn:
                    self.board[self.cursor_y][self.cursor_x] = Horse(self.cursor_x, self.cursor_y, is_white)
                elif curr_btn == bishop_btn:
                    self.board[self.cursor_y][self.cursor_x] = Bishop(self.cursor_x, self.cursor_y, is_white)
                elif curr_btn == queen_btn:
                    self.board[self.cursor_y][self.cursor_x] = Queen(self.cursor_x, self.cursor_y, is_white)
                api.exit_window(self.socket, choose_win)
                self.board[self.cursor_y][self.cursor_x].selected = True
                self.print_board()
                break

    def promote(self):
        rook_txt = """            
  ## ## ##  
  ########  
   ######   
   ######   
  ########  """
        knight_txt = """            
   #####    
  #######   
 ########   
    #####   
  ########  """
        bishop_txt = """    ####    
      ###   
   ######   
    ####    
   ######   
  ########  """
        queen_txt = """     ##     
  ## ## ##  
   ######   
    ####    
    ####    
  ########  """

        for i in range(len(self.board[0])):
            tile = self.board[0][i]
            if(tile.p_type == 'p' and tile.is_white == True):
                self.make_promote_win(rook_txt, knight_txt, bishop_txt, queen_txt, tile.is_white, tile.size)
                return

        for i in range(len(self.board[-1])):
            tile = self.board[-1][i]
            if(tile.p_type == 'p' and tile.is_white == False):
                self.make_promote_win(rook_txt, knight_txt, bishop_txt, queen_txt, tile.is_white, tile.size)
                return

    def check_for_mate(self, is_white):
        for i in self.board:
            for tile in i:
                if(tile.is_white == is_white and 
                       tile.p_type != '\0'):
                    tile.project(self.board)
                    l = [t.highlight for j in self.board for t in j]
                    tile.project(self.board)
                    print()
                    if True in l:
                        return False
        return True

    def game_over_win(self, white_wins):
        prompt = ""
        if white_wins:
            prompt = """___      ____  ____  ____  _____  _________  ________       ____      ____  _____  ____  _____   ______   
|_  _|    |_  _||_   ||   _||_   _||  _   _  ||_   __  |     |_  _|    |_  _||_   _||_   \|_   _|.' ____ \  
  \ \  /\  / /    | |__| |    | |  |_/ | | \_|  | |_ \_|       \ \  /\  / /    | |    |   \ | |  | (___ \_| 
   \ \/  \/ /     |  __  |    | |      | |      |  _| _         \ \/  \/ /     | |    | |\ \| |   _.____`.  
    \  /\  /     _| |  | |_  _| |_    _| |_    _| |__/ |         \  /\  /     _| |_  _| |_\   |_ | \____) | 
     \/  \/     |____||____||_____|  |_____|  |________|          \/  \/     |_____||_____|\____| \______.' """
        else:
            prompt = """_____   _____          _        ______  ___  ____        ____      ____  _____  ____  _____   ______   
|_   _ \ |_   _|        / \     .' ___  ||_  ||_  _|      |_  _|    |_  _||_   _||_   \|_   _|.' ____ \  
  | |_) |  | |         / _ \   / .'   \_|  | |_/ /          \ \  /\  / /    | |    |   \ | |  | (___ \_| 
  |  __'.  | |   _    / ___ \  | |         |  __'.           \ \/  \/ /     | |    | |\ \| |   _.____`.  
 _| |__) |_| |__/ | _/ /   \ \_\ `.___.'\ _| |  \ \_          \  /\  /     _| |_  _| |_\   |_ | \____) | 
|_______/|________||____| |____|`.____ .'|____||____|          \/  \/     |_____||_____|\____| \______.' """

        api.create_window(self.socket,
                          x = 1,
                          y = 1+Tile.size*3,
                          win_wid = Tile.size*16+50,
                          win_hgt = Tile.size*2-1,
                          v_align = "C",
                          prompt = prompt,
                          p_txt_col = "K" if white_wins else "W",
                          win_bg_col = "W" if white_wins else "K",
                          parent_win = self.controls_win)


    def verification_win(self):
        w = api.create_window(self.socket,
                              x = Tile.size*6+1,
                              y = 5+Tile.size*3,
                              win_wid = Tile.size*4,
                              win_hgt = Tile.size,
                              prompt = "Are you sure?",
                              p_txt_col = "Y",
                              win_bg_col = "B",
                              hgl_txt_col = "K",
                              hgl_bg_col = "G")
        y_pos = api.create_button(self.socket,
                                  x = 5, y = 3, txt = "Yes", 
                                  txt_col = "K", bg_col = "W", pad = 1)
        n_pos = api.create_button(self.socket,
                                  x = 13, y = 3, txt = "No", 
                                  txt_col = "K", bg_col = "W", pad = 1)
        return w, y_pos, n_pos

    # Pre: Game is created and no modifications have been made to the object
    def play(self):
        curr_player_is_white = True
        self.cursor_y = 6;
        self.highlight_curr_tile()
        projection_tile = False
        proj_piece_loc = [-1,-1] #(x,y)
        while(1):
            # Reset Cursor
            print("\033[0m\033[51;1H")

            if self.check_for_mate(curr_player_is_white):
                self.game_over_win(not curr_player_is_white)
                break
            key = getkey()
            if   key == keys.UP:
                if(self.cursor_y <= 0):
                    continue
                projection_tile = self.select("UP")
            elif key == keys.DOWN:
                if(self.cursor_y >= 7):
                    continue
                projection_tile = self.select("DOWN")
            elif key == keys.LEFT:
                if(self.cursor_x <= 0):
                    continue
                projection_tile = self.select("LEFT")
            elif key == keys.RIGHT:
                if(self.cursor_x >= 7):
                    continue
                projection_tile = self.select("RIGHT")
            elif key == 'r':
                win_id, yes_pos, no_pos = self.verification_win()
                curr_pos = api.search_button(self.socket, "-x")
                while(1):
                    k = getkey()
                    if k == keys.ENTER:
                        api.exit_window(self.socket, win_id)
                        self.print_board()
                        break
                    elif k == keys.LEFT:
                        curr_pos = api.search_button(self.socket, "-x")
                    elif k == keys.RIGHT:
                        curr_pos = api.search_button(self.socket, "+x")
                if(curr_pos == yes_pos):
                    self.game_over_win(not curr_player_is_white)
                    break
            elif key == keys.ENTER:
                # Projection Logic
                curr_tile = self.board[self.cursor_y][self.cursor_x]
                if curr_tile.p_type == '\0' and not curr_tile.highlight:
                    continue

                tmp = self.project_piece(proj_piece_loc[0], proj_piece_loc[1], curr_player_is_white)
                if tmp[1] != -2:
                    print(f"\033[0;49m\033[48;1H")
                    proj_piece_loc = tmp
                    continue

                # Movement Logic
                if self.move_piece(proj_piece_loc[0], proj_piece_loc[1]):
                    proj_piece_loc = [-1,-1]
                    print(f"\033[0m\033[51;1H")
                    curr_player_is_white = not curr_player_is_white
                    self.promote()
                    continue


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
        print(s, end="")

    def print_controls(self):
        s = """ _____             _             _
/  __ \           | |           | |
| /  \/ ___  _ __ | |_ _ __ ___ | |___
| |    / _ \| '__\| __| '__/ _ \| / __|
| \__/\ (_) | | | | |_| |  |(_) | \__ \\
 \____/\___/|_| |_|\__|_|  \___/|_|___/
Press the Arrow Keys to move around
Press ENTER to select and de-select pieces
press R to Resign
"""
        return api.create_window(self.socket, 97, 1, 50, 11, "T", "L", s)


#TODO:
# Implement En Passant
# Implement Menus via 'h' & 'r'
