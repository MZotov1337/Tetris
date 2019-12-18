from tkinter import Canvas, Label, Tk, StringVar, Button, LEFT
from random import choice, randint

col = ["blue", "yellow", "green", "red", "cyan", "magenta"]

class GameCanvas(Canvas):
    def __init__(self, rt, wid, hei, bg):
        self = Canvas(rt, width = wid, height = hei, background = bg)
    
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
