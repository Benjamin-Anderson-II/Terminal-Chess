"""
Sends messages to the server through the socket
Recieves 4096 bytes back and prints the printable portion
Returns the starting "return" portion of the recieved message
"""
def _send_and_recv(soc, msg):
    soc.sendall(msg.encode())
    recv = soc.recv(4096)
    r = recv.decode("utf-8").split(";;")
    print(r[1])
    return r[0]


"""
Constructs a button creation message for soc
Returns the terminal's x, y coordinates for the button as a string 
  format: "(x,y)"
"""
def create_button(soc, x = 1, y = 1, txt = "Button", txt_col = "0", 
                  bg_col = "0", pad = 1):
    send = "B;%dp;%dx;%dy;{%s};%sb%sf" % (pad,
                                          x, y, txt,
                                          txt_col,
                                          bg_col)

    return _send_and_recv(soc, send)


"""
Constructs a window creation message and uses _send_and_recv on it
Returns the server's window index for the window that has been created
"""
def create_window(soc, x = 1, y = 1, win_wid = 50, win_hgt = 7, 
                  v_align = "T", h_align = "M", prompt = "Window", 
                  p_txt_col = "0", win_bg_col = "0",
                  hgl_txt_col = "W", hgl_bg_col = "K",
                  parent_win = -1):
    send = "W;%dx;%dy;%dW;%dH;%s;%s;{%s};%sf;%sb;%ss;%sS;%dp" % (x, y,
                                                                 win_wid,
                                                                 win_hgt,
                                                                 v_align,
                                                                 h_align,
                                                                 prompt,
                                                                 p_txt_col,
                                                                 win_bg_col,
                                                                 hgl_txt_col,
                                                                 hgl_bg_col,
                                                                 parent_win)
    return int(_send_and_recv(soc, send))

"""
Constructs and sends a Search message to the server
Returns the x and y coordinates in the same format as create_button
"""
def search_button(soc, search):
    return _send_and_recv(soc, "S;%s" % (search))

"""
Constructs an Exit Window Message to the server
Returns the window index of the new current window
"""
def exit_window(soc, idx):
    return int(_send_and_recv(soc, "E;%d" % (idx)))

"""
Constructs and sends a change window message to the server
Returns the window index of the window that was changed to
"""
def change_window(soc, idx):
    return int(_send_and_recv(soc, "C;%d" % (idx)))
