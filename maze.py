#!/usr/bin/env python3

import random
from graphics import Cell, Window
from time import sleep


class Maze:
    def __init__(
            self, x1: int, y1: int,
            num_rows: int, num_cols: int,
            cell_size_x: int, cell_size_y: int,
            win: Window | None = None,
            seed: int | None = None
    ):
        self.__x1, self.__y1 = x1, y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []
        if seed is not None:
            random.seed(seed)
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_i(0,0)
        self.__reset_cells_visited()

    def __create_cells(self):
        for i in range(self.num_cols):
            self.__cells.append([])
            for j in range(self.num_rows):
                self.__cells[i].append(Cell(self.__win))
                self.__draw_cell(i ,j)

    def __draw_cell(self, i, j):
        x1 = self.__x1 + (i-1) * self.cell_size_x
        y1 = self.__y1 + (j-1) * self.cell_size_y
        self.__cells[i][j].draw(x1, y1, x1+self.cell_size_x, y1+self.cell_size_y)
        self.__animate()

    def __animate(self):
        if self.__win:
            self.__win.redraw()
        sleep(0.001)

    def __reset_cells_visited(self):
        for col in self.__cells:
            for cell in col:
                cell.visited = False

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0,0)
        i,j = self.num_cols-1, self.num_rows-1
        self.__cells[i][j].has_bottom_wall = False
        self.__draw_cell(i,j)

    def __break_walls_i(self, i, j):
        stack = [(i,j)]
        while stack:
            i,j = stack[-1]
            self.__cells[i][j].visited = True
            possible_directions = []
            # try going left
            if i > 0 and not self.__cells[i-1][j].visited:
                possible_directions.append("left")
            # now right
            if i < self.num_cols-1 and not self.__cells[i+1][j].visited:
                possible_directions.append("right")
            if j > 0 and not self.__cells[i][j-1].visited:
                possible_directions.append("up")
            if j < self.num_rows-1 and not self.__cells[i][j+1].visited:
                possible_directions.append("down")
            if len(possible_directions) == 0:
                stack.pop()
                continue
            direction = possible_directions[random.randrange(len(possible_directions))]
            if direction == "left":
                self.__cells[i][j].has_left_wall = False
                self.__cells[i-1][j].has_right_wall = False
                target_i, target_j = i-1, j
            elif direction == "right":
                self.__cells[i][j].has_right_wall = False
                self.__cells[i+1][j].has_left_wall = False
                target_i, target_j = i+1, j
            elif direction == "up":
                self.__cells[i][j].has_top_wall = False
                self.__cells[i][j-1].has_bottom_wall = False
                target_i, target_j = i, j-1
            else:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[i][j+1].has_top_wall = False
                target_i, target_j = i, j+1
            self.__draw_cell(i,j)
            self.__draw_cell(target_i, target_j)
            stack.append((target_i, target_j))

    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True
        while True:
            possible_directions = []
            # try going left
            if i > 0 and not self.__cells[i-1][j].visited:
                possible_directions.append("left")
            # now right
            if i < self.num_cols-1 and not self.__cells[i+1][j].visited:
                possible_directions.append("right")
            if j > 0 and not self.__cells[i][j-1].visited:
                possible_directions.append("up")
            if j < self.num_rows-1 and not self.__cells[i][j+1].visited:
                possible_directions.append("down")
            if len(possible_directions) == 0:
                return
            direction = possible_directions[random.randrange(len(possible_directions))]
            if direction == "left":
                self.__cells[i][j].has_left_wall = False
                self.__cells[i-1][j].has_right_wall = False
                target_i, target_j = i-1, j
            elif direction == "right":
                self.__cells[i][j].has_right_wall = False
                self.__cells[i+1][j].has_left_wall = False
                target_i, target_j = i+1, j
            elif direction == "up":
                self.__cells[i][j].has_top_wall = False
                self.__cells[i][j-1].has_bottom_wall = False
                target_i, target_j = i, j-1
            else:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[i][j+1].has_top_wall = False
                target_i, target_j = i, j+1
            self.__draw_cell(i,j)
            self.__draw_cell(target_i, target_j)
            self.__break_walls_r(target_i, target_j)

    def _solve_i(self, i, j):
        stack = [(i,j,None, None)]
        while stack:
            self.__animate()
            i,j,k,l = stack[-1]
            self.__cells[i][j].visited = True
            if i == self.num_cols-1 and j == self.num_rows-1:
                return True
            directions = [
                [
                    i > 0 and not self.__cells[i][j].has_left_wall and not self.__cells[i-1][j].visited,
                    i-1, j
                ],
                [
                    i < self.num_cols-1 and not self.__cells[i][j].has_right_wall and not self.__cells[i+1][j].visited,
                    i+1, j
                ],
                [
                    j > 0 and not self.__cells[i][j].has_top_wall and not self.__cells[i][j-1].visited,
                    i, j-1
                ],
                [
                    j < self.num_rows-1 and not self.__cells[i][j].has_bottom_wall and not self.__cells[i][j+1].visited,
                    i, j+1
                ]
            ]
            for d in directions:
                if d[0]:
                    self.__cells[i][j].draw_move(self.__cells[d[1]][d[2]])
                    stack.append((d[1],d[2],i,j))
                    # all possible moves on the stack
            if all([d[0] is False for d in directions]):
                # no valid moves got added: undo this route
                if k is not None:
                    self.__cells[i][j].draw_move(self.__cells[k][l], True)
                stack.pop()

                #self.__cells[i][j].draw_move(self.__cells[d[1]][d[2]],True)
        return False


    def _solve_r(self, i: int, j: int):
        self.__animate()
        self.__cells[i][j].visited = True
        if i == self.num_cols-1 and j == self.num_rows-1:
            return True
        directions = [
            [
                i > 0 and not self.__cells[i][j].has_left_wall and not self.__cells[i-1][j].visited,
                i-1, j
            ],
            [
                i < self.num_cols-1 and not self.__cells[i][j].has_right_wall and not self.__cells[i+1][j].visited,
                i+1, j
            ],
            [
                j > 0 and not self.__cells[i][j].has_top_wall and not self.__cells[i][j-1].visited,
                i, j-1
            ],
            [
                j < self.num_rows-1 and not self.__cells[i][j].has_bottom_wall and not self.__cells[i][j+1].visited,
                i, j+1
            ]
        ]
        #print(f"from ({i},{j}), options are {directions}")
        for d in directions:
            if d[0]:
                #print(f"trying to move from ({i},{j}) to ({d[1]},{d[2]})")
                self.__cells[i][j].draw_move(self.__cells[d[1]][d[2]])
                res = self._solve_r(d[1],d[2])
                if res:
                    return True
                else:
                    self.__cells[i][j].draw_move(self.__cells[d[1]][d[2]],True)
        return False

    def solve(self):
        return self._solve_i(0,0)
