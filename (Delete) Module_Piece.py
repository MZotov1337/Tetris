from tkinter import Canvas, Label, Tk, StringVar, Button, LEFT
from random import choice, randint
from Module_Shape import *

col = ["blue", "yellow", "green", "red", "cyan", "magenta"]



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
