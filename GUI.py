from tkinter import *
from Board import *
from PIL import Image, ImageTk

square_size = 80
#white_pawn = ImageTk.PhotoImage(Image.open("images/p_white.png"))

class GUI_Board:

    def __init__(self, root, board=Board()):
        self.board = board
        self.root = root
        self.square_size = square_size
        self.canvas = Canvas(root, width=8*self.square_size, height=8*self.square_size, background="grey")
        self.canvas.pack(side="top", fill="both", anchor="c", expand=True)
        #a = self.canvas.create_image(10, 10, image=white_pawn, anchor='nw') 
        # self.canvas.tag_raise(a)

        # frame = Frame(W, width=100, height=50)
        # frame.place(x=700, y=0)
        
        light = False
        for x in range(8):
            for y in range(8):
                if light:
                    color = "#%02x%02x%02x" % (100, 100, 100)
                else:
                    color = "#%02x%02x%02x" % (200, 200, 200)
                sq = self.canvas.create_rectangle(self.square_size*x, self.square_size*y, self.square_size*x+self.square_size, self.square_size*y+self.square_size, fill=color)
                self.canvas.tag_bind(sq, "<ButtonPress-1>", callback)
                light = not light
            light = not light

        for row in range(8):
            for col in range(8):
                piece = str(self.board.board[row][col])
                if piece == "p":
                    a = Label(self.canvas, image = white_pawn)
                    a.grid(column = col+1, row = row+1)
                    print(piece)
                elif piece == "P":
                    a = Label(self.canvas, image = black_pawn)
                    a.grid(column = col+1, row = row+1)

        # btn_column = Label(self.canvas, image = photo)
        # btn_column.grid(column=8, row=8)

        # a = Label(self.canvas, image = photo)
        # a.grid(column=7, row=7)

        # c = Label(self.canvas, image = photo)
        # c.grid(column=6, row=6)

        # d = Label(self.canvas, image = photo)
        # d.grid(column=5, row=5)

        # e = Label(self.canvas, image = photo)
        # e.grid(column=4, row=4)

        # f = Label(self.canvas, image = photo)
        # f.grid(column=3, row=3)

        # g = Label(self.canvas, image = photo)
        # g.grid(column=2, row=2)

        # h = Label(self.canvas, image = photo)
        # h.grid(column=1, row=1)


    def click(self, event):
        # Figure out which square we've clicked
        col_size = row_size = event.widget.master.square_size

        current_column = event.x / col_size
        current_row = 7 - (event.y / row_size)

        piece = self.board.board[current_column][current_row]

        # if self.selected_piece:
        #     self.move(self.selected_piece[1], position)
        #     self.selected_piece = None
        #     self.hilighted = None
        #     self.pieces = {}
        #     self.refresh()
        #     self.draw_pieces()

        # self.hilight(position)
        self.refresh()

    def refresh(self, event={}):
        '''Redraw the board'''
        pass
        # if event:
        #     xsize = int((event.width-1) / 8)
        #     ysize = int((event.height-1) / 8)
        #     self.square_size = min(xsize, ysize)

        # self.canvas.delete("square")
        # color = self.color2
        # for row in range(self.rows):
        #     color = self.color1 if color == self.color2 else self.color2
        #     for col in range(self.columns):
        #         x1 = (col * self.square_size)
        #         y1 = ((7-row) * self.square_size)
        #         x2 = x1 + self.square_size
        #         y2 = y1 + self.square_size
        #         if (self.selected is not None) and (row, col) == self.selected:
        #             self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="orange", tags="square")
        #         elif(self.hilighted is not None and (row, col) in self.hilighted):
        #             self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="spring green", tags="square")
        #         else:
        #             self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
        #         color = self.color1 if color == self.color2 else self.color2
        # for name in self.pieces:
        #     self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        # self.canvas.tag_raise("piece")
        # self.canvas.tag_lower("square")

           
        

    def callback(self, event):
        print("clicked at", event.x, event.y)
        return event.x, event.y

# root
root = Tk()
white_pawn=Image.open("images/p_white.png")  
white_pawn=ImageTk.PhotoImage(white_pawn)
black_pawn=Image.open("images/P_black.png")  
black_pawn=ImageTk.PhotoImage(black_pawn)

white_rook=Image.open("images/r_white.png")
white_rook=ImageTk.PhotoImage(white_rook)
black_rook=Image.open("images/R_black.png")
black_rook=ImageTk.PhotoImage(black_rook)

white_knight=Image.open("images/n_white.png")
white_knight=ImageTk.PhotoImage(white_knight)
black_knight=Image.open("images/N_black.png")
black_knight=ImageTk.PhotoImage(black_knight)

white_bishop=Image.open("images/b_white.png")
white_bishop=ImageTk.PhotoImage(white_bishop)
black_bishop=Image.open("images/B_black.png")
black_bishop=ImageTk.PhotoImage(black_bishop)

white_queen=Image.open("images/q_white.png")
white_queen=ImageTk.PhotoImage(white_queen)
black_queen=Image.open("images/Q_black.png")
black_queen=ImageTk.PhotoImage(black_queen)

white_king=Image.open("images/k_white.png")
white_king=ImageTk.PhotoImage(white_king)
black_king=Image.open("images/K_black.png")
black_king=ImageTk.PhotoImage(black_king)



def callback(event):
        print("clicked at", event.x, event.y)
        return event.x, event.y

# app = App(root)

gui_board = GUI_Board(root)
# frame = Frame(root, width=8*square_size, height=8*square_size)
# frame.bind("<Button-1>", callback)
# frame.pack(side="top")



# frame = Frame(root, background="#%02x%02x%02x" % (128, 192, 200), width=1000, height=1000)
# frame.bind("<Button-1>", callback)
# frame.pack()

menu = Menu(root)
root.config(menu=menu)

# menu
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=callback)
filemenu.add_command(label="Open...", command=callback)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=callback)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=callback)


# toolbar = Frame(root)

# b = Button(toolbar, text="new", width=6, command=callback)
# b.pack(side=LEFT, padx=2, pady=2)

# b = Button(toolbar, text="open", width=6, command=callback)
# b.pack(side=LEFT, padx=2, pady=2)

# toolbar.pack(side=TOP, fill=X)

# separator.pack(fill=X, padx=5, pady=5)

root.mainloop()
#root.destroy() # optional; see description below