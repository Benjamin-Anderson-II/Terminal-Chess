from game import Game

def main():
# create game
    g = Game()
    boardSize = g.board[0][0].size * 8
    g.play()
    print("\033[39;49m\033[%d;%dH" % (boardSize+1, 1), end="")
# play game

if __name__ == "__main__":
    main()
