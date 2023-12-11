from game import Game
import socket

def main():
# create game
    HOST = "127.0.0.1"
    PORT = 65432

    print("\033[2J")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        g = Game(s)
        boardSize = g.board[0][0].size * 8
        g.play()
        print("\033[0m\033[51;1H")
        with open('track_expenses.json', 'w') as j:
            j.write("{}")

if __name__ == "__main__":
    main()
