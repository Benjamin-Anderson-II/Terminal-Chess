import json

def add_piece(is_white, p_type):
    s = "WHITE, " if is_white else "BLACK, "
    if p_type == 'p':
        s += "1"
    elif p_type == 'h':
        s += "3"
    elif p_type == 'b':
        s += "3.4"
    elif p_type == 'r':
        s += "5"
    elif p_type == 'q':
        s += "9"
    else: # moved to empty tile
        return None
    with open("home_input.txt", "w") as file:
        file.write(f"{s}, None, None")

def get_pieces(is_white):
    with open('track_expenses.json', 'r') as infile:
        try:
            expenses = json.load(infile)
        except BaseException as e:
            print("\033[50;100HCouldn't load JSON")
            return ""
    retval = ""
    is_white = not is_white
    sum_material = 0
    if len(expenses) == 0:
        return ""
    for e in expenses["None"]:
        if e["Category"] == ("WHITE" if not is_white else "BLACK"):
            f = float(e["Amount"])
            if f == 1.0:
                retval += "\u2659" if is_white else "\u265F"
            if f == 3.0:
                retval += "\u2658" if is_white else "\u265E"
            if f == 3.4:
                retval += "\u2657" if is_white else "\u265D"
            if f == 5.0:
                retval += "\u2656" if is_white else "\u265C"
            if f == 9.0:
                retval += "\u2655" if is_white else "\u265B"
            retval += " "
            sum_material += int(f)

    retval += str(sum_material)
    return retval
