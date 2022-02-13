import os
import random

dependencies = ['pygame']

try:
    import pygame as pg
except ImportError:
    for dependency in dependencies:
        os.system('pip install ' + dependency)
    import pygame as pg

pg.init()

WINDOW = pg.display.set_mode((1920, 1080))
WINDOW.fill((61, 61, 61))
pg.display.update()
###############################


class Cell:
    grid = {}

    def __init__(self, x, y, status=False):

        self.x = x
        self.y = y
        self.status = status

        Cell.grid[(x, y)] = {
            'obj': self,
            'adj': dict()
        }

    def get(self):
        return self.status

    @classmethod
    def set_grid(cls):
        locales = [
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1)
        ]

        for lc in cls.grid:

            for dx, dy in locales:
                cell = cls.grid[lc]
                try:
                    cls.grid[
                        (cell['obj'].x + dx, cell['obj'].y + dy)
                    ]['adj'][
                        (cell['obj'].x, cell['obj'].y)
                    ] = cell['obj'].get
                except KeyError:
                    pass # usually means corner has been hit

    def draw(self):
        color = self.status and (255, 255, 255)
        color = color or (61, 61, 61)
        pg.draw.rect(WINDOW, color, (self.x*20, self.y*20, 20, 20))

    def __repr__(self):
        return f'Cell({self.x}, {self.y}, status={self.status})'

################################


for i in range(96):
    for j in range(54):
        Cell(i, j).draw()

pg.display.update()
running = True

Cell.set_grid()
clicked = False

if __name__ == "__main__":
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                clicked = False

        if clicked:
            x, y = pg.mouse.get_pos()
            lx, ly = x-x%20, y-y%20
            pg.draw.rect(WINDOW, (255, 255, 255), (lx, ly, 20, 20))
            pg.display.update()
            Cell.grid[(lx//20, ly//20)]['obj'].status = True
        elif pg.key.get_pressed()[pg.K_SPACE]:
            break

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break

        kill = []
        revive = []
        for cell in Cell.grid:
            alive = 0
            for adj in Cell.grid[cell]['adj']:
                alive = alive + Cell.grid[cell]['adj'][adj]()

            if not Cell.grid[cell]['obj'].get() and alive == 3:
                revive.append(cell)
            elif alive not in (2, 3):
                kill.append(cell)

        for k in kill:
            Cell.grid[k]['obj'].status = False
            pg.draw.rect(WINDOW, (61, 61, 61), (k[0]*20, k[1]*20, 20, 20))

        for r in revive:
            Cell.grid[r]['obj'].status = True
            pg.draw.rect(WINDOW, (255, 255, 255), (r[0]*20, r[1]*20, 20, 20))

        pg.display.update()
        kill = []
        revive = []
