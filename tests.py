#!/usr/bin/env python3

import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0,0,num_rows,num_cols,10,10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows
        )
    def test_maze_break_entr_exit(self):
        num_cols = 5
        num_rows = 8
        m1 = Maze(0,0,num_rows,num_cols,10,10)
        self.assertEqual(
            m1._Maze__cells[0][0].has_top_wall,
            False
        )
        self.assertEqual(
            m1._Maze__cells[4][7].has_bottom_wall,
            False
        )

    def test_maze_reset_visit(self):
        num_cols = 12
        num_rows = 8
        m1 = Maze(0,0,num_rows,num_cols,10,10)
        self.assertEqual(
            [[x.visited for x in col] for col in m1._Maze__cells],
            [[False for _ in range(num_rows)] for _ in range(num_cols)]
        )

if __name__ == "__main__":
    unittest.main()
