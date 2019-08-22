from Board import *
# from GUI import *

from tkinter import *

import sys

# x = input('Enter your name:')
# print('Hello, ' + x)


def play():
    board = Board()
    while True:
        white_move = input("White to Move:")
        board.move(white_move)
        if board.game_over():
            break

        black_move = input("Black to Move:")
        board.move(black_move)
        if board.game_over():
            break
    winner = board.game_over()
    if winner == "white" or winner == "black":
        return "{} wins!".format(winner)
    
def gui_play():
    board = Board()
    while True:
        if board.turn == "white":
            move = input("White to Move:")
            
        elif board.turn == "black":
            move = input("Black to Move:")

        if move == "exit":
                break
        board.move(move)
        print(board)


def testing():

    # print(board.get_piece("a1"))
    # print(board.get_piece("e4"))

    board = Board()
    # board.set_square("e1", King("white", "e1", board))
    # board.set_square("d8", Queen("black", "d8", board))
    # board.set_square("d7", Queen("black", "d7", board))
    # board.set_square("a8", King("black", "a8", board))
    # board.copy = board.update_copy()
    #board.move("Kf1")
    # print(board.white_pieces)
    # print(board.black_pieces)
    board.setup()

    # board.move("e4")
    # board.move("e5")
    # board.move("Nf3")
    # board.move("Nc6")
    # board.move("Bb5")
    # board.move("a6")
    # board.move("Ba4")
    # board.move("Nf6")

    print(board)
    while True:
        if board.turn == "white":
            move = input("White to Move:")
            
        elif board.turn == "black":
            move = input("Black to Move:")

        if move == "exit":
            break

        if move == "show copy":
            result = ""
            for i, line in enumerate(board.copy[::-1]):
                for space in line:
                    result = result + str(space) + " "
                result = result + "  " + str(8 - i) + "\n"
            result = result + "\na b c d e f g h "
            print(result)
            continue
        board.move(move)
        print(board)

print(sys.argv)
if "testing" in sys.argv:
    testing()
elif "play" in sys.argv:
    play()
elif "gui" in sys.argv:
    gui_play()
else:
    testing()