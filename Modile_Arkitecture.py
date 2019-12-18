from tkinter import Canvas, Label, Tk, StringVar, Button, LEFT
from random import choice, randint
from Module_Piece import *
from Modile_Shape import *
from Module_Canvas import *
from Modile_Arkitecture import *
col = ["blue", "yellow", "green", "red", "cyan", "magenta"]

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
        self.speed = 1000

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
                self._Number += 0

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
        self.speed = 1000 + (level - 1) * 50
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