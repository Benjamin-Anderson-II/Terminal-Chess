from game import Game
import socket

def main():
# create game
    HOST = "127.0.0.1"
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        g = Game(s)
        boardSize = g.board[0][0].size * 8
        g.play()
        print("\033[39;49m\033[%d;%dH" % (boardSize+1, 1), end="")

if __name__ == "__main__":
    main()
