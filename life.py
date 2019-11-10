import pathlib
import random

from typing import List, Optional, Tuple
from copy import deepcopy


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    
    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool=True,
        max_generations: Optional[float]=float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.n_generation = 1


    def create_grid(self, randomize: bool=False) -> Grid:
        # Copy from previous assignment
        grid = [[0 for i in range(self.cols)] for j in range(self.rows)]
        if randomize:
            for i in range(0, self.rows):
                for j in range(0, self.cols):
                    grid[i][j] = random.randint(0, 1)
        return grid


    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        Cells = []
        x, y = cell
        n = self.rows - 1
        m = self.cols - 1
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if not (0 <= i <= n and 0 <= j <= m) or (i == x and j == y):
                    continue
                Cells.append(self.curr_generation[i][j])
        return Cells


    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        new_grid = deepcopy(self.curr_generation)
        for i in range(self.rows):
            for j in range(self.cols):
                a = sum(self.get_neighbours((i, j)))
                if self.curr_generation[i][j]:
                    if a in (2, 3):
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
                else:
                    if a == 3:
                        new_grid[i][j] = 1
        return new_grid


    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.n_generation += 1


    @property
    def is_max_generations_exceed(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.n_generation >= self.max_generations
        

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation


    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid = []
        f = open(filename, 'r')
        lines = f.read().split('\n')
        rows = len(lines)
        cols = len(lines[0].strip()) 
        game = GameOfLife(size=(rows, cols), randomize=False)

        for s in lines:
            line = []
            for ch in s:
                line.append(int(ch))
            grid.append(line)
        game.curr_generation = deepcopy(grid)
        return game


    def save(filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, mode='w') as f:
            for row in self.curr_generation:
                for i in row:
                    f.write(str(i))
                f.write('\n')