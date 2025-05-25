#!/usr/bin/env python3

from graphics import Window
from maze import Maze

def main():
    win = Window(800, 800)
    # margins of 50 => 700x500 effectively
    maze = Maze(50,50,16,16,10,10,win)
    maze.solve()
    win.wait_for_close()

main()
