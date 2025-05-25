#!/usr/bin/env python3

from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.geometry(f"{width}x{height}")
        self.__canvas = Canvas(self.__root)
        self.__canvas.pack()
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

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def draw(self, canvas, fill_color):
        canvas.create_line(self.a.x, self.a.y, self.b.x, self.b.y, fill=fill_color, width=2)

def main():
    win = Window(500, 500)
    l1 = Line(
        Point(100, 100), Point(400,100)
    )
    l2 = Line(
        Point(100,100), Point(600,600)
    )
    win.draw_line(l1)
    win.draw_line(l2, fill_color="red")
    win.wait_for_close()

main()
