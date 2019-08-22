import Board
import re
#from Board import *
columns_inverse = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
class Piece:
    def __init__(self, color, square, board):
        self.alive = True
        self.color = color
        self.other = "black" if self.color == "white" else "white"
        self.board = board
        self.square = square
        if color != "black" and color != "white" and color != "_":
            raise Exception
        self.moved = False

        if self.color == "white":
            self.board.white_pieces.add(self)
        elif self.color == "black":
            self.board.black_pieces.add(self)

    def move(self, new_square):
        self.board.set_square(new_square, self)
        self.board.set_square(self.square, Empty(self.square, self))
        self.square = new_square
        self.moved = True
        return True

    def legal_move(self, next_move):
        '''
        returns  the new square if the given move is legal, and false otherwise
        '''
        
        return False

class Empty(Piece):
    def __init__(self, square, board):
        self.color = "empty"
        self.square = square
        self.board = board
    
    def __str__(self):
        return "_"

class Pawn(Piece):
    def __init__(self, color, square, board):
        super().__init__(color, square, board)

    def __str__(self):
        if self.color == "black":
            return "P"
        elif self.color == "white":
            return "p"
    
    def evolve(self, piece):
        '''
        pawn turns into another piece if it reaches the backrank
        '''

    def legal_move(self, next_move):
        '''
        returns  the new square if the given move is legal, and false otherwise
        '''
        if self.color == "white":
            if re.match("[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", next_move) and int(next_move[1]) - int(self.square[1]) == 1 and type(self.board.get_piece(next_move)) == Empty:
                return True
            elif re.match("[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", next_move) and self.square[1] == "2" and next_move[1] == "4":
                middle = self.square[0] + "3"
                if type(self.board.get_piece(next_move)) == Empty and type(self.board.get_piece(middle)) == Empty:
                    return True
            elif re.match("[a,b,c,d,e,f,g,h][x][a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", next_move):
                new_square = next_move[2:]
                return self.board.get_piece(new_square).color == "black"
            else:
                return False
        elif self.color == "black":
            if re.match("[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", next_move) and int(next_move[1]) - int(self.square[1]) == -1 and type(self.board.get_piece(next_move)) == Empty:
                return True
            elif re.match("[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", next_move) and self.square[1] == "7" and next_move[1] == "5":
                middle = self.square[0] + "6"
                if type(self.board.get_piece(next_move)) == Empty and type(self.board.get_piece(middle)) == Empty:
                    return True
            elif re.match("[a,b,c,d,e,f,g,h][x][a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", next_move):
                new_square = next_move[2:]
                return self.board.get_piece(new_square).color == "white"
            else:
                return False
        else:
            return False
        

class Rook(Piece):
    def __init__(self, color, square, board):
        super().__init__(color, square, board)

    def __str__(self):
        if self.color == "black":
            return "R"
        elif self.color == "white":
            return "r"
    
    def legal_move(self, next_move):
        '''
        returns  the new square if the given move is legal, and false otherwise
        '''
        new_square = next_move[-2:]
        new_row = int(new_square[1]) - 1
        new_col = int(columns_inverse[new_square[0]])
        self_row, self_col = int(self.square[1]) - 1, int(columns_inverse[self.square[0]])
        if not (bool(new_row - self_row) ^ bool(new_col - self_col)):
            return False
        try:
            dr = int((new_row - self_row) / abs(new_row - self_row))
        except ZeroDivisionError:
            dr = 0
        try:
            dc = int((new_col - self_col) / abs(new_col - self_col))
        except ZeroDivisionError:
            dc = 0
        for i in range(1, max(new_row - self_row, new_col - self_col)):
            if self.board.board[self_row + i * dr][self_col + i * dc].color != "empty":
                return False
        if "x" in next_move:
            return self.board.board[new_row][new_col].color == self.other
        else:
            return self.board.board[new_row][new_col].color == "empty"
        return False

class Knight(Piece):
    def __init__(self, color, square, board):
        super().__init__(color, square, board)

    def __str__(self):
        if self.color == "black":
            return "N"
        elif self.color == "white":
            return "n"
    def legal_move(self, next_move):
        '''
        returns  the new square if the given move is legal, and false otherwise
        '''
        new_square = next_move[-2:]
        new_row = int(new_square[1]) - 1
        new_col = int(columns_inverse[new_square[0]])
        self_row, self_col = int(self.square[1]) - 1, int(columns_inverse[self.square[0]])
        if "x" in next_move:
            if abs(new_row - self_row) == 2 and abs(new_col - self_col) == 1 and self.board.board[new_row][new_col].color == self.other:
                return True
            elif abs(new_row - self_row) == 1 and abs(new_col - self_col) == 2 and self.board.board[new_row][new_col].color == self.other:
                return True
        else:
            if abs(new_row - self_row) == 2 and abs(new_col - self_col) == 1 and self.board.board[new_row][new_col].color == "empty":
                return True
            elif abs(new_row - self_row) == 1 and abs(new_col - self_col) == 2 and self.board.board[new_row][new_col].color == "empty":
                return True
        return False

class Bishop(Piece):
    def __init__(self, color, square, board):
        super().__init__(color, square, board)

    def __str__(self):
        if self.color == "black":
            return "B"
        elif self.color == "white":
            return "b"

    def legal_move(self, next_move):
        '''
        returns  the new square if the given move is legal, and false otherwise
        '''
        new_square = next_move[-2:]
        new_row = int(new_square[1]) - 1
        new_col = int(columns_inverse[new_square[0]])
        self_row, self_col = int(self.square[1]) - 1, int(columns_inverse[self.square[0]])
        if abs(new_row - self_row) != abs(new_col - self_col):
            return False
        dr = int((new_row - self_row) / abs(new_row - self_row))
        dc = int((new_col - self_col) / abs(new_col - self_col))
        for i in range(1, abs(new_row - self_row)):
            if self.board.board[self_row + i * dr][self_col + i * dc].color != "empty":
                return False
        if "x" in next_move:
            return self.board.board[new_row][new_col].color == self.other
        else:
            return self.board.board[new_row][new_col].color == "empty"
        return False

class Queen(Piece):
    def __init__(self, color, square, board):
        super().__init__(color, square, board)

    def __str__(self):
        if self.color == "black":
            return "Q"
        elif self.color == "white":
            return "q"
    
    def legal_move(self, next_move):
        '''
        returns  the new square if the given move is legal, and false otherwise
        '''
        new_square = next_move[-2:]
        #print(new_square)
        new_row = int(new_square[1]) - 1
        new_col = int(columns_inverse[new_square[0]])
        self_row, self_col = int(self.square[1]) - 1, int(columns_inverse[self.square[0]])
        bishop_like = abs(new_row - self_row) == abs(new_col - self_col)
        rook_like = (bool(new_row - self_row) ^ bool(new_col - self_col))
        if not rook_like ^ bishop_like:
            return False
        try:
            dr = int((new_row - self_row) / abs(new_row - self_row))
        except ZeroDivisionError:
            dr = 0
        try:
            dc = int((new_col - self_col) / abs(new_col - self_col))
        except ZeroDivisionError:
            dc = 0
        for i in range(1, max(new_row - self_row, new_col - self_col)):
            if self.board.board[self_row + i * dr][self_col + i * dc].color != "empty":
                #print("in the way")
                return False
        if "x" in next_move:
            return self.board.board[new_row][new_col].color == self.other
        else:
            return self.board.board[new_row][new_col].color == "empty"
        return False

            

class King(Piece):
    def __init__(self, color, square, board):
        super().__init__(color, square, board)
        self.is_checked = False

    def __str__(self):
        if self.color == "black":
            return "K"
        elif self.color == "white":
            return "k"
    
    def legal_move(self, next_move):
        '''
        returns  the new square if the given move is legal, and false otherwise
        '''
        new_square = next_move[-2:]
        new_row = int(new_square[1]) - 1
        new_col = int(columns_inverse[new_square[0]])
        self_row, self_col = int(self.square[1]) - 1, int(columns_inverse[self.square[0]])
        
        if max(abs(new_row - self_row), abs(new_col - self_col)) > 1:
            return False
        try:
            dr = int((new_row - self_row) / abs(new_row - self_row))
        except ZeroDivisionError:
            dr = 0
        try:
            dc = int((new_col - self_col) / abs(new_col - self_col))
        except ZeroDivisionError:
            dc = 0
        if "x" in next_move:
            return self.board.board[new_row][new_col].color == self.other
        else:
            return self.board.board[new_row][new_col].color == "empty"
        return False

    def castle(self, rook):
        '''
        performs castling
        '''
        if self.color == "white":
            if rook.square == "h1":
                self.move("g1")
                rook.move("f1")
            elif rook.square == "a1":
                self.move("c1")
                rook.move("d1")
            else:
                return False
        elif self.color == "black":
            if rook.square == "h8":
                self.move("g8")
                rook.move("f8")
            elif rook.square == "a8":
                self.move("c8")
                rook.move("d8")
            else:
                return False
        return True

    def safe_spot(self, square):
        '''
        returns whether a square is a safe spot for the king
        '''
        enemies = self.board.white_pieces if self.color == "black" else self.board.black_pieces
        for piece in enemies:
            if piece.legal_move(str(piece) + "x" + square):
                print("move", str(piece) + "x" + square)
                print("my_square", square)
                print("Illegal move!", piece, piece.color, piece.square)
                return False
        return True