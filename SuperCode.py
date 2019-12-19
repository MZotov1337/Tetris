from tkinter import Canvas, Label, Tk, StringVar, Button, LEFT
from random import choice, randint

col = ["blue", "yellow", "green", "red", "black", "cyan", "magenta"]

class GameCanvas(Canvas):
    
    def drop_Piecees(self, Piecees_to_drop):
        for Piece in Piecees_to_drop:
            self.move(Piece, 0, Arkitecture.LENGTH)
        self.update()    
    
    def clean_line(self, Deleting):
        for Piece in Deleting:
            self.delete(Piece)
        self.update()

    def completed_lines(self, YY):
        cleaned_lines = 0
        YY = sorted(YY)
        for y in YY:
            if sum(1 for Piece in self.find_withtag('game') if self.coords(Piece)[3] == y) == ((Arkitecture.width - 20) // Arkitecture.LENGTH): 
                self.clean_line([Piece for Piece in self.find_withtag('game') if self.coords(Piece)[3] == y])
                self.drop_Piecees([Piece for Piece in self.find_withtag('game') if self.coords(Piece)[3] < y])
                cleaned_lines += 1
        return cleaned_lines

    def game_board(self):
        board = [[0] * ((Arkitecture.width - 20) // Arkitecture.LENGTH) for _ in range(Arkitecture.height // Arkitecture.LENGTH)]
        for Piece in self.find_withtag('game'):
            x, y, _, _ = self.coords(Piece)
            board[int(y // Arkitecture.LENGTH)][int(x // Arkitecture.LENGTH)] = 1
        return board
    def Piecees(self):
        return self.find_withtag('game') == self.find_withtag(fill="blue")

class Shape():
    def __init__(self, coords = None):
        if not coords:
            self.__coords = choice(Arkitecture.SHAPES)
        else:
            self.__coords = coords

    @property
    def coords(self):
        return self.__coords

    def rotate(self):  
        self.__coords = self.__rotate()

    def rotate_directions(self):
        rotated = self.__rotate()
        directions = [(rotated[i][0] - self.__coords[i][0],
                       rotated[i][1] - self.__coords[i][1]) for i in range(len(self.__coords))]

        return directions

    @property
    def matrix(self):
        return [[1 if (j, i) in self.__coords else 0 \
                 for j in range(max(self.__coords, key=lambda x: x[0])[0] + 1)] \
                 for i in range(max(self.__coords, key=lambda x: x[1])[1] + 1)]

    def drop(self, board, offset):
        off_x, off_y = offset
        last_level = len(board) - len(self.matrix) + 1
        for level in range(off_y, last_level):
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[0])):
                    if board[level+i][off_x+j] == 1 and self.matrix[i][j] == 1:
                        return level - 1
        return last_level - 1  

    def __rotate(self):
        max_x = max(self.__coords, key=lambda x:x[0])[0]
        new_original = (max_x, 0)

        rotated = [(new_original[0] - coord[1],
                    new_original[1] + coord[0]) for coord in self.__coords]

        min_x = min(rotated, key=lambda x:x[0])[0]
        min_y = min(rotated, key=lambda x:x[1])[1]
        return [(coord[0] - min_x, coord[1] - min_y) for coord in rotated]

class Piece():
    def __init__(self, canvas, Point0, shape = None):
        self.shapes = shape
        if not shape:
            self.shapes = Shape()
        self.canvas = canvas
        self.Piecees = self.__create_Piecees(Point0)

    @property
    def shape(self):
        return self.shapes

    def move(self, direction):
        if all(self.__can_move(self.canvas.coords(Piece), direction) for Piece in self.Piecees):
            x, y = direction
            for Piece in self.Piecees:
                self.canvas.move(Piece, x * Arkitecture.LENGTH, y * Arkitecture.LENGTH)
            return True
        return False

    def rotate(self):
        directions = self.shapes.rotate_directions()
        if all(self.__can_move(self.canvas.coords(self.Piecees[i]), directions[i]) for i in range(len(self.Piecees))):
            self.shapes.rotate()
            for i in range(len(self.Piecees)):
                x, y = directions[i]
                self.canvas.move(self.Piecees[i],
                                 x * Arkitecture.LENGTH,
                                 y * Arkitecture.LENGTH)

    @property
    def offset(self):
        return (min(int(self.canvas.coords(Piece)[0]) // Arkitecture.LENGTH for Piece in self.Piecees), min(int(self.canvas.coords(Piece)[1]) // Arkitecture.LENGTH for Piece in self.Piecees))

    def predict_movement(self, board):
        level = self.shapes.drop(board, self.offset)
        min_y = min([self.canvas.coords(Piece)[1] for Piece in self.Piecees])
        return (0, level - (min_y // Arkitecture.LENGTH))

    def predict_drop(self, board):
        level = self.shapes.drop(board, self.offset)
        self.remove_predicts()

        min_y = min([self.canvas.coords(Piece)[1] for Piece in self.Piecees])
        for Piece in self.Piecees:
            x1, y1, x2, y2 = self.canvas.coords(Piece)
            Piece = self.canvas.create_rectangle(x1, level * Arkitecture.LENGTH + (y1 - min_y), x2, (level + 1) * Arkitecture.LENGTH + (y1 - min_y), fill="white", tags = "predict")

    def remove_predicts(self):
        for i in self.canvas.find_withtag('predict'):
            self.canvas.delete(i) 
        self.canvas.update()

    def __create_Piecees(self, Point0):
        Piecees = []
        off_x, off_y = Point0
        for coord in self.shapes.coords:
            x, y = coord
            Piece = self.canvas.create_rectangle(x * Arkitecture.LENGTH + off_x, y * Arkitecture.LENGTH + off_y, x * Arkitecture.LENGTH + Arkitecture.LENGTH + off_x, y * Arkitecture.LENGTH + Arkitecture.LENGTH + off_y, fill=choice(col), tags="game")
            Piecees += [Piece]

        return Piecees

    def __can_move(self, Piece_coords, new_pos):
        x, y = new_pos
        x = x * Arkitecture.LENGTH
        y = y * Arkitecture.LENGTH
        x_left, y_up, x_right, y_down = Piece_coords

        overlap = set(self.canvas.find_overlapping((x_left + x_right) / 2 + x, 
                                                   (y_up + y_down) / 2 + y, 
                                                   (x_left + x_right) / 2 + x,
                                                   (y_up + y_down) / 2 + y))
        other_items = set(self.canvas.find_withtag('game')) - set(self.Piecees)

        if y_down + y > Arkitecture.height or x_left + x < 0 or x_right + x > Arkitecture.width or overlap & other_items:
            return False
        return True        

class Arkitecture():
    SHAPES = ([(0, 0), (1, 0), (0, 1), (1, 1)],     # Square
              [(0, 0), (1, 0), (2, 0), (3, 0)],     # Stick
              [(2, 0), (0, 1), (1, 1), (2, 1)],     # Right L
              [(0, 0), (0, 1), (1, 1), (2, 1)],     # Left L
              [(0, 1), (1, 1), (1, 0), (2, 0)],     # Right Z
              [(0, 0), (1, 0), (1, 1), (2, 1)],     # Left Z
              [(1, 0), (0, 1), (1, 1), (2, 1)])     # T

    LENGTH = 20

    width = 300
    height = 500
    SrartPos = width / 2 / LENGTH * LENGTH - LENGTH

    def __init__(self, predictable = False):
        self._level = 1
        self._score = 0
        self._Number = 0
        self.speed = 1000
        self.predictable = predictable

        self.root = Tk()
        self.root.geometry("500x550") 
        self.root.title('Tetryais')
        self.root.bind("<Key>", self.game_control)
        self.game_canvas()
        self.levelsc()
        self.NxtPiece()

    def game_control(self, event):
        if event.char in ["s", "S", "\uf702"]:
            self.current_piece.move((-1, 0))
            self.update_predict()
        elif event.char in ["d", "D", "\uf703"]:
            self.current_piece.move((1, 0))
            self.update_predict()
        elif event.char in ["t", "T", "\uf701"]:
            self.hard_drop()
        elif event.char in ["f", "F", "\uf700"]:
            self.current_piece.rotate()
            self.update_predict()

    def new_game(self):
        self.level = 1
        self.score = 0
        self.Number = 0
        self.speed = 500

        self.canvas.delete("all")
        self.next_canvas.delete("all")

        self.frame()
        self.__draw_next_canvas_frame()

        self.current_piece = None
        self.next_piece = None        

        self.game_board = [[0] * ((Arkitecture.width - 20) // Arkitecture.LENGTH) for _ in range(Arkitecture.height // Arkitecture.LENGTH)]

        self.update_piece()

    def update_piece(self):
        if not self.next_piece:
            self.next_piece = Piece(self.next_canvas, (20,20))

        self.current_piece = Piece(self.canvas, (Arkitecture.SrartPos, 0), self.next_piece.shape)
        self.next_canvas.delete("all")
        self.__draw_next_canvas_frame()
        self.next_piece = Piece(self.next_canvas, (20,20))
        self.update_predict()

    def start(self):
        self.new_game()
        self.root.after(self.speed, None)
        self.drop()
        self.root.mainloop()

    def drop(self):
        if not self.current_piece.move((0,1)):
            self.current_piece.remove_predicts()
            self.completed_lines()
            self.game_board = self.canvas.game_board()
            self.update_piece()

            if self.is_game_over():
                return
            else:
                self._Number += 1

        self.root.after(self.speed, self.drop)

    def hard_drop(self):
        self.current_piece.move(self.current_piece.predict_movement(self.game_board))

    def update_predict(self):
        if self.predictable:
            self.current_piece.predict_drop(self.game_board)

    def update_status(self):
        self.status_var.set(f"Level: {self.level}, Score: {self.score}")
        self.status.update()

    def is_game_over(self):
        if not self.current_piece.move((0,1)):

            self.Again = Button(self.root, text="Play Again", command=self.play_again)
            self.Exit = Button(self.root, text="Exit", command=self.quit) 
            self.Again.place(x = Arkitecture.width + 10, y = 200, width=100, height=25)
            self.Exit.place(x = Arkitecture.width + 10, y = 300, width=100, height=25)
            return True
        return False

    def play_again(self):
        self.Again.destroy()
        self.Exit.destroy()
        self.start()

    def quit(self):
        self.root.quit()     

    def completed_lines(self):
        YY = [self.canvas.coords(Piece)[3] for Piece in self.current_piece.Piecees]
        completed_line = self.canvas.completed_lines(YY)
        if completed_line == 1:
            self.score += 100
        elif completed_line == 2:
            self.score += 300
        elif completed_line == 3:
            self.score += 700
        elif completed_line == 4:
            self.score += 1500

    def game_canvas(self):
        self.canvas = GameCanvas(self.root, width = Arkitecture.width, height = Arkitecture.height, bg = 'Black')
        self.canvas.pack(padx = 5 ,side=LEFT)



    def levelsc(self):
        self.status_var = StringVar()        
        self.status = Label(self.root,textvariable=self.status_var, font=("Helvetica", 10, "bold"))
        self.status.pack()

    def NxtPiece(self):
        self.next_canvas = Canvas(self.root, width = 100, height = 100)
        self.next_canvas.pack(padx=5 , pady=10)

    def frame(self):
        self.canvas.create_line(10, 0, 10, self.height, fill = "red", tags = "line")
        self.canvas.create_line(self.width-10, 0, self.width-10, self.height, fill = "red", tags = "line")
        self.canvas.create_line(10, self.height, self.width-10, self.height, fill = "red", tags = "line")

    def __draw_next_canvas_frame(self):
        self.next_canvas.create_rectangle(10, 10, 90, 90, tags="frame")

    #Here we get lvl, number of pieces 
    def lvl(self):
        return self._level

    def ZerLvl(self, level):
        self.speed = 500 - (level - 1) * 25
        self._level = level
        self.update_status()

    def Score(self):
        return self._score  

    def ZerScore(self, score):
        self._score = score
        self.update_status()

    def Number(self):
        return self._Number

    def ZerNumber(self, Number):
        self.level = Number // 5 + 1
        self._Number = Number

    level = property(lvl, ZerLvl)
    score = property(Score, ZerScore)
    Number = property(Number, ZerNumber)


game = Arkitecture(predictable = True)
game.start()

