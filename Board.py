from Piece import *
import re

columns = ["a", "b", "c", "d", "e", "f", "g", "h"]
columns_inverse = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
class Board:
    def __init__(self):
        self.board = [[""]*8 for _ in range(8)]
        for row in range(8):
            for col in range(8):
                square = columns[col] + str(row + 1)
                self.board[row][col] = Empty(square, self)
        self.turn = "white"
        self.moves = []
        self.white_pieces = set()
        self.black_pieces = set()

        self.copy = self.update_copy()
 
    def setup(self):
        self.board[0][0] = Rook("white", "a1", self)
        self.board[0][1] = Knight("white", "b1", self)
        self.board[0][2] = Bishop("white", "c1", self)
        self.board[0][3] = Queen("white", "d1", self)
        self.board[0][4] = King("white", "e1", self)
        self.board[0][5] = Bishop("white", "f1", self)
        self.board[0][6] = Knight("white", "g1", self)
        self.board[0][7] = Rook("white", "h1", self)

        self.board[7][0] = Rook("black", "a8", self)
        self.board[7][1] = Knight("black", "b8", self)
        self.board[7][2] = Bishop("black", "c8", self)
        self.board[7][3] = Queen("black", "d8", self)
        self.board[7][4] = King("black", "e8", self)
        self.board[7][5] = Bishop("black", "f8", self)
        self.board[7][6] = Knight("black", "g8", self)
        self.board[7][7] = Rook("black", "h8", self)

        for i in range(8):
            white_spot = columns[i] + "2"
            black_spot = columns[i] + "7"
            self.board[1][i] = Pawn("white", white_spot, self)
            #self.white_pieces.add(self.board[1][i])
            self.board[6][i] = Pawn("black", black_spot, self)
            #self.black_pieces.add(self.board[6][i])
        
        # print(self.white_pieces)
        # print(self.black_pieces)

        self.copy = self.update_copy()

    def __str__(self):
        result = ""
        for i, line in enumerate(self.board[::-1]):
            for space in line:
                result = result + str(space) + " "
            result = result + "  " + str(8 - i) + "\n"
        result = result + "\na b c d e f g h "
        return result

    def sq_to_mtx(self, square):
        '''
        return the list position given the square
        '''
        assert(re.match("[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", square))
        col = columns_inverse[square[0]]
        row = int(square[1]) - 1
        return col, row

    def get_piece(self, square):
        '''
        returns what's on the square
        '''
        assert type(square) == str and len(square) == 2
        col = columns_inverse[square[0]]
        row = int(square[1]) - 1
        return self.board[row][col]
    
    def set_square(self, square, piece):
        '''
        set a square to have a certain piece or nothing 
        '''
        if not re.match("[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", square):
            raise Exception(square)
        assert isinstance(piece, Piece) or piece == "_"

        # self.copy = self.update_copy()

        col = columns_inverse[square[0]]
        row = int(square[1]) - 1
        self.board[row][col] = piece

    def move(self, move1):
        '''
        make the move
        '''
        successful = False
        major = {'R', 'N', 'B', 'K', 'Q'}
        if move1[0] not in major and move1 != "O-O" and move1 != "O-O-O": #pawn
            if re.match("[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", move1):
                col = columns_inverse[move1[0]]
                row = int(move1[1]) - 1
                pawn_rows = [row - 1, row - 2, row + 1, row + 2]
                for row in pawn_rows:
                    try:
                        pawn = self.board[row][col]
                        if pawn and type(pawn) == Pawn and pawn.color == self.turn:
                            if pawn.legal_move(move1):
                                self.moves.append(move1)
                                successful = pawn.move(move1)
                                break
                    except IndexError:
                        continue
            elif re.match("[a,b,c,d,e,f,g,h][x][a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", move1):
                choices = [self.board[int(move1[3]) - 2][int(columns_inverse[move1[0]])],
                            self.board[int(move1[3])][int(columns_inverse[move1[0]])]]
                new_square = move1[2:]
                for pawn in choices:
                    if pawn.legal_move(move1):
                        successful = pawn.move(new_square)
                        self.moves.append(move1)
                        break

        elif move1[0] == 'R': #rook
            new_square = move1[-2:]
            new_col, new_row = self.sq_to_mtx(new_square)
            choices = [(i,0) for i in range(-7,8)] + [(0, i) for i in range(-7,8)]
            rooks = []
            for dc, dr in choices:
                old_col, old_row = new_col + dc, new_row + dr
                try:
                    if old_col >= 0 and old_col <=7 and old_row >= 0 and old_row <= 7:
                        rook = self.board[old_row][old_col]
                        if type(rook) == Rook and rook.color == self.turn:
                            if rook.legal_move(move1):
                                rooks.append(rook)
                except IndexError:
                    continue
            if re.match("R[x]?[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", move1): 
                pass
            elif re.match("R[a,b,c,d,e,f,g,h][x]?[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", move1):
                rooks = [k for k in rooks if k.square[0] == move1[1]]
            elif re.match("R[1,2,3,4,5,6,7,8][x]?[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", move1):
                rooks = [k for k in rooks if k.square[1] == move1[1]]
            elif re.match("R[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8][x]?[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", move1):
                rooks = [k for k in rooks if k.square == move1[1:3]]
            if len(rooks) == 1:
                    rook = rooks[0]
                    if rook.legal_move(move1):
                        successful = rook.move(new_square)
                        self.moves.append(move1)
            else:
                print("0 or > 1 rooks", [r.square for r in rooks])
                return False
        elif move1[0] == 'N': #knight
            new_square = move1[-2:]
            new_col, new_row = self.sq_to_mtx(new_square)
            choices = [(2, 1), (1, 2), (-2, 1), (1, -2), (2, -1), (-1, 2), (-1, -2), (-2, -1)]
            knights = []
            for dc, dr in choices:
                old_col, old_row = new_col + dc, new_row + dr
                try:
                    knight = self.board[old_row][old_col]
                    if type(knight) == Knight and knight.color == self.turn:
                        if knight.legal_move(move1):
                            knights.append(knight)
                except IndexError:
                    continue
            if re.match("N[x]?[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", move1): 
                pass
            elif re.match("N[a,b,c,d,e,f,g,h][x]?[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", move1):
                knights = [k for k in knights if k.square[0] == move1[1]]
            elif re.match("N[1,2,3,4,5,6,7,8][x]?[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", move1):
                knights = [k for k in knights if k.square[1] == move1[1]]
            elif re.match("N[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8][x]?[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", move1):
                knights = [k for k in knights if k.square == move1[1:3]]
            if len(knights) == 1:
                    knight = knights[0]
                    if knight.legal_move(move1):
                        successful = knight.move(new_square)
                        self.moves.append(move1)
            else:
                print("0 or > 1 knights")
                return False


        elif move1[0] == 'B': #bishop
            new_square = move1[-2:]
            new_col, new_row = self.sq_to_mtx(new_square)
            choices = [(i,i) for i in range(1,8)] + [(i, -i) for i in range(1,8)] + [(-i, i) for i in range(1,8)] + [(-i, -i) for i in range(1, 8)]
            bishops = []
            for dc, dr in choices:
                old_col, old_row = new_col + dc, new_row + dr
                try:
                    if old_col >= 0 and old_col <=7 and old_row >= 0 and old_row <= 7:
                        bishop = self.board[old_row][old_col]
                        if type(bishop) == Bishop and bishop.color == self.turn:
                            if bishop.legal_move(move1):
                                bishops.append(bishop)
                except IndexError:
                    continue
            if re.match("B[x]?[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", move1): 
                pass
            elif re.match("B[a,b,c,d,e,f,g,h][x]?[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", move1):
                bishops = [k for k in bishops if k.square[0] == move1[1]]
            elif re.match("B[1,2,3,4,5,6,7,8][x]?[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", move1):
                bishops = [k for k in bishops if k.square[1] == move1[1]]
            elif re.match("B[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8][x]?[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", move1):
                bishops = [k for k in bishops if k.square == move1[1:3]]
            if len(bishops) == 1:
                    bishop = bishops[0]
                    if bishop.legal_move(move1):
                        successful = bishop.move(new_square)
                        self.moves.append(move1)
            else:
                print("0 or > 1 bishops", bishops)
                return False
        elif move1[0] == 'Q': #queen
            new_square = move1[-2:]
            new_col, new_row = self.sq_to_mtx(new_square)
            choices = [(i,i) for i in range(1,8)] + [(i, -i) for i in range(1,8)] + [(-i, i) for i in range(1,8)] + [(-i, -i) for i in range(1, 8)] \
                    + [(i,0) for i in range(-7,8)] + [(0, i) for i in range(-7,8)]
            queens = []
            for dc, dr in choices:
                old_col, old_row = new_col + dc, new_row + dr
                try:
                    if old_col >= 0 and old_col <=7 and old_row >= 0 and old_row <= 7:
                        queen = self.board[old_row][old_col]
                        if type(queen) == Queen and queen.color == self.turn:
                            if queen.legal_move(move1):
                                queens.append(queen)
                except IndexError:
                    continue
            if re.match("Q[x]?[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", move1): 
                pass
            elif re.match("Q[a,b,c,d,e,f,g,h][x]?[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", move1):
                queens = [k for k in queens if k.square[0] == move1[1]]
            elif re.match("Q[1,2,3,4,5,6,7,8][x]?[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", move1):
                queens = [k for k in queens if k.square[1] == move1[1]]
            elif re.match("Q[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8][x]?[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", move1):
                queens = [k for k in queens if k.square == move1[1:3]]
            if len(queens) == 1:
                    queen = queens[0]
                    if queen.legal_move(move1):
                        successful = queen.move(new_square)
                        self.moves.append(move1)
            else:
                print("0 or > 1 queen", queens)
                return False
        elif move1[0] == 'K': #king
            new_square = move1[-2:]
            new_col, new_row = self.sq_to_mtx(new_square)
            choices = [(1,1), (1,0), (1,-1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
            for dc, dr in choices:
                old_col, old_row = new_col + dc, new_row + dr
                try:
                    if old_col >= 0 and old_col <=7 and old_col >= 0 and old_row <= 7:
                        king = self.board[old_row][old_col]
                        if type(king) == King and king.color == self.turn:
                            break
                except IndexError:
                    continue
            if not re.match("K[x]?[a,b,c,d,e,f,g,h][1,2,3,4,5,6,7,8]", move1): 
                return False
            elif king.legal_move(move1):
                successful = king.move(new_square)
                self.moves.append(move1)
        elif move1 == "O-O": # kingside castle
            if self.turn == "white":
                king = self.get_piece("e1")
                rook = self.get_piece("h1")
                right_pieces = type(king) == King and type(rook) == Rook and king.color == "white" and rook.color == "white" and king.moved == False and rook.moved == False
                if right_pieces and type(self.get_piece("f1")) == Empty and type(self.get_piece("g1")) == Empty:
                    successful = king.castle(rook)
                    self.moves.append(move1)
            elif self.turn == "black":
                king = self.get_piece("e8")
                rook = self.get_piece("h8")
                right_pieces = type(king) == King and type(rook) == Rook and king.color == "black" and rook.color == "black" and king.moved == False and rook.moved == False
                if right_pieces and type(self.get_piece("f8")) == Empty and type(self.get_piece("g8")) == Empty:
                    successful = king.castle(rook)
                    self.moves.append(move1)
        elif move1 == "O-O-O": #queenside castle
            if self.turn == "white":
                king = self.get_piece("e1")
                rook = self.get_piece("a1")
                right_pieces = type(king) == King and type(rook) == Rook and king.color == "white" and rook.color == "white" and king.moved == False and rook.moved == False
                if right_pieces and type(self.get_piece("b1")) == Empty and type(self.get_piece("c1")) == Empty and type(self.get_piece("d1")) == Empty:
                    successful = king.castle(rook)
                    self.moves.append(move1)
            elif self.turn == "black":
                king = self.get_piece("e8")
                rook = self.get_piece("a8")
                right_pieces = type(king) == King and type(rook) == Rook and king.color == "black" and rook.color == "black" and king.moved == False and rook.moved == False
                if right_pieces and type(self.get_piece("b8")) == Empty and type(self.get_piece("c8")) == Empty and type(self.get_piece("d8")) == Empty:
                    successful = king.castle(rook)
                    self.moves.append(move1)

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if type(piece) == King and piece.color == self.turn:
                    my_king = piece

        safe = my_king.safe_spot(my_king.square)
        if successful and safe:
            if self.turn == "white":
                self.turn = "black"
            elif self.turn == "black":
                self.turn = "white"
            self.update_copy()
        elif successful and not safe:
            self.board = self.copy
            self.update_copy()

    def update_copy(self):
        '''
        updates the copy of the boar and the pieces
        '''
        self.white_pieces = set()
        self.black_pieces = set()
        copy = [[""]*8 for _ in range(8)]
        for row in range(8):
            for col in range(8):
                square = columns[col] + str(row + 1)
                test = self.board[row]
                sq = self.board[row][col].square
                piece = self.copy_piece(sq)
                copy[row][col] = piece
                if copy[row][col].color == "white":
                    self.white_pieces.add(piece)
                elif copy[row][col].color == "black":
                    self.black_pieces.add(copy[row][col])
        return copy

    def copy_piece(self, square):
        '''
        return a copy of the piece, bound to the copy board
        '''
        og = self.get_piece(square)
        if type(og) == Empty:
            return Empty(og.square, self)
        elif type(og) == Pawn:
            return Pawn(og.color, og.square, self)
        elif type(og) == Rook:
            return Rook(og.color, og.square, self)
        elif type(og) == Knight:
            return Knight(og.color, og.square, self)
        elif type(og) == Bishop:
            return Bishop(og.color, og.square, self)
        elif type(og) == Queen:
            return Queen(og.color, og.square, self)
        elif type(og) == King:
            return King(og.color, og.square, self)


    def has_move(self, player):
        '''
        returns whether the player has moves
        '''
        assert player == "black" or player == "white"
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece.color == player:
                    for row in range(8):
                        for col in range(8):
                            if piece.legal_move(str(piece) + "x" + square) or piece.legal_move(str(piece) + square):
                                return True
        return False
                            


    def game_over(self):
        '''
        returns whether the game is over. Returns white if white wins, black if black wins, stalemate if stalemate
        '''
        return False
