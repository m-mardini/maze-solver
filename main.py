#!/usr/bin/env python3

from graphics import Window
from maze import Maze

def main():
    win = Window(800, 600)
    # margins of 50 => 700x500 effectively
    maze = Maze(50,50,22,30,25,25,win,250)
    maze.solve()
    win.wait_for_close()

main()
