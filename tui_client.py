# This is an example client, and can be used as a template

import socket
from getkey import getkey, keys
import tui_api as api

HOST = "127.0.0.1" # Server's hostname or IP addr
PORT = 65432 # Same port as server

#(x, y)
create_pos = (18, 7)
create_txt = "NEW WIN"
exit_pos  = (48, 11)
exit_txt  = "EXIT"
nothing_pos = (31, 6)
nothing_txt = "NOTHING"

## [x,y]  <- list so that it can be changed
cursor_pos = [create_pos[0], create_pos[1]]

def decode_pos(pos):
    cursor_pos[0] = int(pos[1:-1].split(",")[0])
    cursor_pos[1] = int(pos[1:-1].split(",")[1])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    win_w = 70
    win_h = 15
    win_x = 10
    win_y = 3

    print("\033[2J")
    prompt = "This is the first line, and will act as a header.\nThis is after a newline character."
    main_win = api.create_window(s, win_x, win_y, win_w, win_h, "M", "T", prompt, "K", "W", "C", "R")
    curr_win = main_win
    api.create_button(s, create_pos[0], create_pos[1], create_txt, "W", "K")
    api.create_button(s, exit_pos[0], exit_pos[1], exit_txt, "W", "K")
    api.create_button(s, nothing_pos[0], nothing_pos[1], nothing_txt, "W", "K")
    decode_pos(api.search_button(s, "{%s}" % (create_txt)))

    while True:
        print(f"\033[H{curr_win}")
        key = getkey()
        if key == keys.LEFT:
            decode_pos(api.search_button(s, "-x"))
        if key == keys.RIGHT:
            decode_pos(api.search_button(s, "+x"))
        if key == keys.UP:
            decode_pos(api.search_button(s, "-y"))
        if key == keys.DOWN:
            decode_pos(api.search_button(s, "+y"))
        if key == keys.ENTER:

            # Window 2 variables
            win2_x = 20
            win2_y = 6
            win2_w = 40
            win2_h = 10
            w2btn_x = 36
            w2btn_y = 1
            
            ## Since the window is not at 1,1 we need to add the x and y positions for the window
            if cursor_pos[0] == create_pos[0] + win_x and cursor_pos[1] == create_pos[1] + win_y:
                curr_win = api.create_window(s, win2_x, win2_y, win2_w, win2_h, 
                                             "M", "C", "NEW WINDOW", "M", "G", parent_win = main_win)

                decode_pos(api.create_button(s, w2btn_x, w2btn_y, "X", "R", "B"))

            elif(curr_win == 1 and cursor_pos[0] == w2btn_x+win2_x and cursor_pos[1] == w2btn_y+win2_y):
                    curr_win = api.exit_window(s, curr_win)

            elif cursor_pos[0] == exit_pos[0] + win_x and cursor_pos[1] == exit_pos[1] + win_y:
                break
                
        if key == 'q':
            if curr_win != main_win:
                curr_win = api.exit_window(s, curr_win)
            else:
                print("\033[H\033[0m", end = "")
                break
