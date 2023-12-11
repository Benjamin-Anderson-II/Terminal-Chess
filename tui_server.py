import socket as soc
import math

# effectively a C struct
class Button():
    def __init__(self, pad = 0, x = 0, y = 0, txt = "", fg = 0, bg = 49):
        self.pad = pad
        self.x = x
        self.y = y
        self.txt = txt
        self.fg = fg
        self.bg = bg

class Window():
    def __init__(self,
                 x = 0, y = 0, win_width = 0, win_height = 0,
                 v_align = "T", h_align = "L", txt = "",
                 txt_width = 0, txt_height = 0, txt_color = 0, bg_color = 49,
                 highlight_fg = 30, highlight_bg = 43, prev_win = -1):
        self.x = x
        self.y = y
        self.win_width = win_width
        self.win_height = win_height
        self.v_align = v_align
        self.h_align = h_align
        self.txt = txt
        self.txt_width = txt_width
        self.txt_height = txt_height
        self.txt_color = txt_color
        self.bg_color = bg_color
        self.highlight_fg = highlight_fg
        self.highlight_bg = highlight_bg
        self.prev_win = prev_win
        self.buttons = []

HOST = "127.0.0.1"
PORT = 65432

std_fg = 0
std_bg = 49

windows = []

curr_window_idx = -1
curr_btn_idx = -1

def get_color(col, is_bg):
    global btn_col
    if col == "K":
        return 40 if is_bg else 30
    elif col == "R":
        return 41 if is_bg else 31
    elif col == "G":
        return 42 if is_bg else 32
    elif col == "Y":
        return 43 if is_bg else 33
    elif col == "B":
        return 44 if is_bg else 34
    elif col == "M":
        return 45 if is_bg else 35
    elif col == "C":
        return 46 if is_bg else 36
    elif col == "W":
        return 47 if is_bg else 37
    elif col == "0":
        return 49 if is_bg else 0

    return 49 if is_bg else 0

def parse_btn(data):
    global windows, curr_btn_idx
    curr_win = windows[curr_window_idx]
    curr_btn = Button()
    for d in data:
        if d[-1] == 'p':
            curr_btn.pad = int(d[:-1])
        elif d[-1] == 'x':
            curr_btn.x = int(d[:-1]) + curr_win.x
        elif d[-1] == 'y':
            curr_btn.y = int(d[:-1]) + curr_win.y
        elif d[-1] == '}':
            curr_btn.txt = d[1:-1].split("\n")
        elif d[-1] == 'b':
            curr_btn.fg = get_color(d[:-1], True)
        elif d[-1] == 'f':
            curr_btn.bg = get_color(d[:-1], False)

    curr_btn_idx = len(curr_win.buttons)
    curr_win.buttons.append(curr_btn)
            
def mk_btn(fg, bg):
    global windows
    curr_btn = windows[curr_window_idx].buttons[curr_btn_idx]
    btn_x = curr_btn.x
    btn_y = curr_btn.y
    btn_pad = curr_btn.pad
    btn_txt = curr_btn.txt

    s = f"({btn_x},{btn_y});;"
    #set color
    s += f"\033[1;{fg};{bg}m"

    #move to beginning of text
    s += f"\033[{btn_y};{btn_x}H"

    # Make Background Box
    box_w = len(btn_txt[0]) + 4 * btn_pad
    box_h = len(btn_txt) + 2 * btn_pad
    s += f"\033[{btn_pad}A"

    for i in range(box_h):
        for j in range(box_w):
            s += " "
        s += f"\033[{box_w}D\033[1B"
    s += f"\033[{box_h}A"

    #make forground
    for t in btn_txt:
        s += "\033[%dC%s\033[%dD\033[1B" % (btn_pad, t, btn_pad + len(t) + 1)

    #go back to start of btn_txt
    s += f"\033[{len(btn_txt)}D"
    
    return s

def parse_window(data):
    global windows, curr_window_idx
    w = Window()
    for d in data:
        if d[-1] == "x":
            w.x = int(d[:-1])
        elif d[-1] == "y":
            w.y = int(d[:-1])
        elif d[-1] == "W":
            w.win_width = int(d[:-1])
        elif d[-1] == "H":
            w.win_height = int(d[:-1])
        elif d[-1] == "M":
            w.h_align = "M"
        elif d[-1] == "L":
            w.h_align = "L"
        elif d[-1] == "R":
            w.h_align = "R"
        elif d[-1] == "T":
            w.v_align = "T"
        elif d[-1] == "C":
            w.v_align = "C"
        elif d[-1] == "B":
            w.v_align = "B"
        elif d[-1] == "}":
            w.txt = d[1:-1].split("\n")
        elif d[-1] == "f":
            w.txt_color = get_color(d[0], False)
        elif d[-1] == "b":
            w.bg_color = get_color(d[0], True)
        elif d[-1] == "s":
            w.highlight_fg = get_color(d[0], False)
        elif d[-1] == "S":
            w.highlight_bg = get_color(d[0], True)
        elif d[-1] == "p":
            w.prev_win = int(d[:-1])

    curr_window_idx = len(windows)
    windows.append(w)

def mk_win():
    global windows, curr_window_idx
    w = windows[curr_window_idx]
    s = f"{curr_window_idx};;"
    # Make Background
    #goto x,y
    s += "\033[%d;%dH\033[1;%d;%dm" % (w.y, w.x, w.txt_color, w.bg_color)
    for i in range(w.win_height):
        for j in range(w.win_width):
            s += " "
        s += f"\033[1B\033[{w.win_width}D"
    s += f"\033[{w.win_height}A"

    ## Make Prompt

    # Set Text Box Position
    if w.v_align == "T":
        s += "\033[%dH" % (w.y)
    elif w.v_align == "C":
        s += "\033[%dH" % ((w.y) + (w.win_height / 2) - (len(w.txt) / 2))
    elif w.v_align == "B":
        s += "\033[%dH" % (w.y + w.win_height - len(w.txt))

    if w.h_align == "L":
        s += "\033[%dC" % (w.x)
    elif w.h_align == "M":
        s += "\033[%dC" % (w.x)
    elif w.h_align == "R":
        s += "\033[%dC" % (w.x + w.win_width - w.len(w.txt[0]) - 1)

    # Put in Text
    for t in w.txt:
        offset = 0
        if w.h_align == "M":
            offset = w.win_width / 2 - len(t) / 2 - 1
        elif w.h_align == "R":
            offset = w.win_width - len(t) - 1
        s += "\033[%dC%s\033[%dD\033[1B" % (offset, t, offset + len(t)+1)

    return s
    

def get_angle(x1, y1, x2, y2):
    return math.atan(math.fabs(y2-y1) / math.fabs(x2-x1))

def get_closest_btn(buttons, curr_btn, condition, right_angle = 0, updown = 1):
    global curr_btn_idx
    min_a = math.inf
    min_d = math.inf
    best = 0
    for i in range(len(buttons)):
        if i == curr_btn_idx:
            continue
        if right_angle != 0 and condition(buttons[i].y - curr_btn.y):
            continue
        elif right_angle == 0 and condition(buttons[i].x - curr_btn.x):
            continue
        curr_a = right_angle + updown * get_angle(curr_btn.x, curr_btn.y, buttons[i].x, buttons[i].y)
        curr_d = math.dist([curr_btn.x, curr_btn.y], [buttons[i].x, buttons[i].y])
        if(curr_d < min_d):
            min_a = curr_a
            min_d = curr_d
            best = i
        elif curr_d == min_d and curr_a < min_a:
            best = i
            min_a = curr_a
    if min_a == math.inf:
        return curr_btn_idx
    return best 

def search(data):
    global windows, curr_btn_idx, curr_window_idx
    buttons = windows[curr_window_idx].buttons
    curr_btn = buttons[curr_btn_idx]
    for d in data:
        if d[-1] == "}":
            for i in range(len(buttons)):
                if buttons[i].txt == d[1:-1]:
                    return i
        elif d == "+y":
            return get_closest_btn(buttons, curr_btn, lambda y: y<=0, math.pi/2, -1)
        elif d == "-y":
            return get_closest_btn(buttons, curr_btn, lambda y: y>=0, math.pi/2, -1)
        elif d == "+x":
            return get_closest_btn(buttons, curr_btn, lambda x: x<=0)
        elif d == "-x":
            return get_closest_btn(buttons, curr_btn, lambda x: x>=0)

def exit_win(win):
    global curr_window_idx, windows, curr_btn_idx
    w = windows[int(win)].prev_win
    curr_win = windows[curr_window_idx]
    s = f"{w};;"

    #clear window from view
    s += "\033[%d;%dH\033[%d;%dm" % (curr_win.y, curr_win.x, std_fg, std_bg)
    for i in range(curr_win.win_height):
        for j in range(curr_win.win_width):
            s += " "
        s += f"\033[1B\033[{curr_win.win_width}D"
    s += f"\033[{curr_win.win_height}A"

    windows.pop(curr_window_idx)
    curr_window_idx = w
    s += mk_win().split(";;")[1]
    cbi = curr_btn_idx
    for i in range(len(windows[curr_window_idx].buttons)):
        curr_btn_idx = i
        if cbi == i:
            s += mk_btn(windows[curr_window_idx].highlight_fg, windows[curr_window_idx].highlight_bg).split(";;")[1]
        else:
            s += mk_btn(windows[curr_window_idx].buttons[i].fg, windows[curr_window_idx].buttons[i].bg).split(";;")[1]

    curr_btn_idx = cbi

    return s

with soc.socket(soc.AF_INET, soc.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            data = data.decode("utf-8").split(";")
            if data[0] == "B":
                if curr_window_idx == -1:
                    conn.sendall(b"(-1,-1);; ")
                    continue
                parse_btn(data[1:])
                curr_window = windows[curr_window_idx]
                curr_btn = curr_window.buttons[curr_btn_idx]
                if len(curr_window.buttons) == 0:
                    conn.sendall(mk_btn(curr_window.highlight_fg, curr_window.highlight_bg).encode())
                else:
                    conn.sendall(mk_btn(curr_btn.fg, curr_btn.bg).encode())
            elif data[0] == "S":
                curr_window = windows[curr_window_idx]
                if len(windows[curr_window_idx].buttons) == 0:
                    conn.sendall(b"(-1,-1);; ")
                    continue

                btn_idx = search(data[1:])
                # goto button
                curr_btn = curr_window.buttons[curr_btn_idx]
                curr_btn = windows[curr_window_idx].buttons[curr_btn_idx]
                s = mk_btn(curr_btn.fg, curr_btn.bg).split(";;")[1]
                curr_btn_idx = btn_idx
                curr_btn = windows[curr_window_idx].buttons[curr_btn_idx]
                r = mk_btn(windows[curr_window_idx].highlight_fg, windows[curr_window_idx].highlight_bg)
                v = r.split(";;")
                v.insert(1, ";;")
                v.insert(2, s)
                j = "".join(v)
                conn.sendall(j.encode())
            elif data[0] == "W":
                parse_window(data[1:])
                conn.sendall(mk_win().encode())
            elif data[0] == "E":
                # Close Window
                conn.sendall(exit_win(data[1]).encode())
            elif data[0] == "C":
                curr_window_idx = int(data[1])
                conn.sendall(mk_win().encode())
