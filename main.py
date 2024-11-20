import pygame as pg
from constants import CELL_COLOR, BACKGROUND, FRAMERATE, INITIAL_GRID_SIZE, RESOLUTION, SENSITIVITY


class Grid:
    def __init__(self, points: set):
        self.alive = points

    def kill(self, point: tuple):
        self.alive.remove(point)

    def resurrect(self, point: tuple):
        self.alive.add(point)

    def update(self):
        adjacency = dict()

        for point in self.alive:
            x, y = point
            neighbors = [
                (x+1, y),
                (x-1, y),
                (x, y+1),
                (x, y-1),
                (x+1, y+1),
                (x-1, y-1),
                (x+1, y-1),
                (x-1, y+1)
            ]
            for neighbor in neighbors:
                if neighbor not in adjacency:
                    adjacency[neighbor] = 1
                else:
                    adjacency[neighbor] += 1

        prep_to_kill = set()
        for point in self.alive:
            if point not in adjacency or adjacency[point] not in (2, 3):
                prep_to_kill.add(point)

        prep_to_ressurect = set()
        for point in adjacency:
            if point not in self.alive and adjacency[point] == 3:
                prep_to_ressurect.add(point)

        for point in prep_to_ressurect:
            self.resurrect(point)

        return prep_to_kill


class Render:
    def __init__(self, screen: pg.Surface, top=0, left=0):
        self.camera_pos = top, left
        self.camera_x = left
        self.camera_y = top
        self.screen = screen
        self.color = CELL_COLOR
        self.grid_size = INITIAL_GRID_SIZE

    def render(self, grid: Grid, kill: set):
        for point in grid.alive:
            abs_x, abs_y = point
            rel_x, rel_y = (abs_x - self.camera_x, abs_y - self.camera_y)
            pg.draw.rect(self.screen, self.color,
                         (rel_x*self.grid_size, rel_y*self.grid_size, self.grid_size, self.grid_size))

        for point in kill:
            self._remove(grid, point)

    def move(self, rel_x, rel_y):
        self.camera_x += rel_x*SENSITIVITY
        self.camera_y += rel_y*SENSITIVITY

    def set_pos(self, x, y):
        self.camera_x = x
        self.camera_y = y

    def _remove(self, grid: Grid, point: tuple):
        abs_x, abs_y = point
        rel_x, rel_y = (abs_x - self.camera_x, abs_y - self.camera_y)

        grid.kill(point)
        pg.draw.rect(self.screen, BACKGROUND,
                     (rel_x*self.grid_size, rel_y*self.grid_size, self.grid_size, self.grid_size))

    def zoom(self, delta):
        self.grid_size += delta
        self.screen.fill(BACKGROUND)


def main(screen: pg.Surface, camera: Render):
    screen.fill(BACKGROUND)
    clock = pg.time.Clock()

    pg.display.update()
    points = set()
    dragging = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                dragging = True
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                dragging = False

        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_SPACE]:
            break

        if dragging:
            x, y = pg.mouse.get_pos()
            row, col = x//INITIAL_GRID_SIZE, y//INITIAL_GRID_SIZE
            points.add((row, col))
            pg.draw.rect(camera.screen, camera.color,
                         (row * camera.grid_size, col * camera.grid_size, camera.grid_size, camera.grid_size))

        pg.display.update()

    grid = Grid(points)
    camera.render(grid, set())
    dragging = False

    while True:
        clock.tick(FRAMERATE)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif dragging and event.type == pg.MOUSEMOTION:
                rel_x, rel_y = event.rel
                camera.move(rel_x, rel_y)
                screen.fill(BACKGROUND)

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
                elif event.button == 4:
                    camera.zoom(1)
                elif event.button == 5:
                    camera.zoom(-1)
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False

        kill = grid.update()
        camera.render(grid, kill)

        pg.display.update()

        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_r]:
            camera.set_pos(0, 0)
            camera.grid_size = INITIAL_GRID_SIZE
            main(screen, camera)


if __name__ == '__main__':
    pg.init()
    scr = pg.display.set_mode(RESOLUTION)
    main(scr, Render(scr))

