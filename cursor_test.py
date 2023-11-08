from getkey import getkey, keys
while(1):
    key = getkey()
    if key == keys.UP:
        print("UP")
    elif key == keys.DOWN:
        print("DOWN")
    elif key == keys.RIGHT:
        print("RIGHT")
    elif key == keys.LEFT:
        print("LEFT")
    elif key == 'q':
        break
    elif key == keys.ENTER:
        print("ENTER")
