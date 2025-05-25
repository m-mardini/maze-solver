#!/usr/bin/env python3

from time import sleep
from tkinter import BOTH, Canvas, Tk


class Point:
    def __init__(self, x: int, y:int):
        self.x = x
        self.y = y

class Line:
    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b
    def draw(self, canvas, fill_color):
        canvas.create_line(self.a.x, self.a.y, self.b.x, self.b.y, fill=fill_color, width=2)

class Window:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.geometry(f"{width}x{height}")
        self.__canvas = Canvas(self.__root)
        self.__canvas.pack(fill=BOTH, expand=True)
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line: Line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

class Cell:
    def __init__(self, win: Window | None = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.visited = False
        self.__win = win
    def get_center(self):
        return Point((self.__x1 + self.__x2) // 2, (self.__y1 + self.__y2) // 2)
    def draw(self, x1: int, y1: int, x2:int, y2:int):
        self.__x1, self.__y1, self.__x2, self.__y2 = x1,y1,x2,y2
        if not self.__win:
            return
        has_walls = [self.has_left_wall, self.has_right_wall,
                 self.has_top_wall, self.has_bottom_wall]
        walls = [
            Line(Point(x1,y1), Point(x1,y2)),
            Line(Point(x2,y1), Point(x2,y2)),
            Line(Point(x1,y1), Point(x2,y1)),
            Line(Point(x1,y2), Point(x2,y2))
        ]
        line_colors = ["black" if x else "#d9d9d9" for x in has_walls]
        for line, color in zip(walls, line_colors):
            self.__win.draw_line(line, color)
    def draw_move(self, to_cell, undo=False):
        line_color = "gray" if undo else "red"
        if not self.__win:
            return
        self.__win.draw_line(Line(self.get_center(), to_cell.get_center()), fill_color=line_color)

