import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=15, speed: int=10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed 
        self.screen_size = life.cols * self.cell_size, life.rows * self.cell_size
        self.screen = pygame.display.set_mode(self.screen_size)


    def draw_lines(self) -> None:
        # Copy from previous assignment
        width, height = self.screen_size

        for x in range(0, width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, height))
        for y in range(0, height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (width, y))


    def draw_grid(self) -> None:
        # Copy from previous assignment
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                x = i * self.cell_size + 1
                y = j *self.cell_size + 1
                a = self.cell_size - 1
                b = self.cell_size - 1
                if self.life.curr_generation[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (x, y, a, b))
                elif self.life.curr_generation[i][j] == 0:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (x, y, a, b))


    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        running = True
        pause = False
        while running and self.life.is_changing and not self.life.is_max_generations_exceed:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYUP and event.key == K_SPACE:
                    pause = not pause
                elif event.type == MOUSEBUTTONDOWN and pause:
                    self.mouse_fill_cell()

            self.draw_lines()
            self.draw_grid()
            if not pause:
                self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


    def mouse_fill_cell(self) -> None:
        x, y = pygame.mouse.get_pos()
        row = x // self.cell_size
        col = y // self.cell_size
        self.life.curr_generation[row][col] = (self.life.curr_generation[row][col] + 1) % 2


if __name__ == '__main__':
    life = GameOfLife((25, 25), max_generations=200)
    gui = GUI(life)
    gui.run()