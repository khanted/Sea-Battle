from random import randint, choice
import pygame

EMPTY = 0
SHIP = 1
EMPTY_CHECKED = 2
SHIP_CHECKED = 3
EMPTY_RESTRICTED = 4
list2 = []

H = "H"
V = "V"

MISS = "мимо"
KILLED = "убит"
HIT = "ранен"


class Ship(object):
    def __init__(self, x, y, direct, d):
        self.start_point_x = x
        self.start_point_y = y
        self.direction = direct
        self.decks = d


class Sea(object):
    def __init__(self, sea_size=10):
        self.sea = []
        self.size = sea_size

        for i in range(self.size):
            line = [EMPTY for j in range(self.size)]
            self.sea.append(line)

    def draw_with_ships(self):
        for line in self.sea:
            for p in line:
                if p == 1:
                    print(p, end=" ")
                else:
                    print("*", end=" ")
            print()

    def draw(self):
        for line in self.sea:
            for p in line:
                if p == SHIP_CHECKED:
                    print("+", end=" ")
                elif p == EMPTY_CHECKED:
                    print("-", end=" ")
                else:
                    print("*", end=" ")
            print()

    def can_be_placed(self, ship):
        if ship.direction == H:
            for y in range(ship.start_point_y, ship.start_point_y + ship.decks):
                if self.sea[ship.start_point_x][y] != EMPTY:
                    return False
        else:
            for x in range(ship.start_point_x, ship.start_point_x + ship.decks):
                if self.sea[x][ship.start_point_y] != EMPTY:
                    return False
        return True

    def set_restricted_point(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.sea[x][y] = EMPTY_RESTRICTED

    def set_restricted_area(self, ship):
        start_point_x = ship.start_point_x
        start_point_y = ship.start_point_y
        decks = ship.decks
        if ship.direction == V:
            self.set_restricted_point(start_point_x - 1, start_point_y)
            self.set_restricted_point(start_point_x - 1, start_point_y + 1)
            self.set_restricted_point(start_point_x - 1, start_point_y - 1)
            self.set_restricted_point(start_point_x + decks, start_point_y)
            self.set_restricted_point(start_point_x + decks, start_point_y + 1)
            self.set_restricted_point(start_point_x + decks, start_point_y - 1)
            for x in range(start_point_x, start_point_x + decks):
                self.set_restricted_point(x, start_point_y - 1)
                self.set_restricted_point(x, start_point_y + 1)
        else:
            self.set_restricted_point(start_point_x, start_point_y - 1)
            self.set_restricted_point(start_point_x + 1, start_point_y - 1)
            self.set_restricted_point(start_point_x - 1, start_point_y - 1)
            self.set_restricted_point(start_point_x, start_point_y + decks)
            self.set_restricted_point(start_point_x + 1, start_point_y + decks)
            self.set_restricted_point(start_point_x - 1, start_point_y + decks)
            for y in range(start_point_y, start_point_y + decks):
                self.set_restricted_point(start_point_x - 1, y)
                self.set_restricted_point(start_point_x + 1, y)

    def place_ship(self, ship):
        self.set_restricted_area(ship)
        if ship.direction == V:
            for x in range(ship.start_point_x, ship.start_point_x + ship.decks):
                self.sea[x][ship.start_point_y] = SHIP
                list2.append(x)
                list2.append(ship.start_point_y)
        else:
            for y in range(ship.start_point_y, ship.start_point_y + ship.decks):
                self.sea[ship.start_point_x][y] = SHIP
                list2.append(ship.start_point_x)
                list2.append(y)

    def set_ships(self):
        ships_set = 0
        for decks in [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]:
            while True:
                ship = Ship(randint(0, self.size - decks), randint(0, self.size - decks), choice([H, V]), decks)
                if self.can_be_placed(ship):
                    self.place_ship(ship)
                    break

    def get_cell(self, x, y):
        return self.sea[x][y]

    """def make_shot(self, x, y):
        x = int(input())
        y = int(input())
        if sea[x][y] == 0:
            sea[x][y] = 3
            return MISS
        if sea[x][y] == 1:
            sea[x][y] = 8
            if self.ship_was_destroyed(self, x, y):
                return HIT
            if not self.ship_was_destroyed(self, x, y):
                return KILLED"""

    """def ship_was_destroyed(self, x, y):
        x = int(input())
        y = int(input())
        if sea[x + 1][y] == 1 or sea[x - 1][y] == 1 or sea[x][y + 1] == 1 or sea[x][y - 1] == 1 or sea[x + 1][
            y + 1] == 1 or sea[x + 1][y - 1] == 1 or sea[x - 1][y + 1] == 1 or sea[x - 1][y - 1] == 1:
            return False
        else:
            return True"""

    """def all_ships_destroyed(self):
        if sea[x + 1][y] == 1 or sea[x - 1][y] == 1 or sea[x][y + 1] == 1 or sea[x][y - 1] == 1 or sea[x + 1][
            y + 1] == 1 or sea[x + 1][y - 1] == 1 or sea[x - 1][y + 1] == 1 or sea[x - 1][y - 1] == 1:
            return True
        else:
            return False"""

    """def draw_cell(x, y, w, h, color, sea):
        x = 0
        y = 0
        w = 10
        h = 10
        sea()
        can_be_placed()
        set_ships()
        color = (0, 0, 255)
        sea = Sea()
        pygame.init()
        SCREEN = pygame.display.set_mode((size, size))
        pygame.display.set_caption("Морской бой")
        square = pygame.Rect(x, y, w, h)
        SCREEN.fill((color))
        running = True
        pygame.event.get()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            for i in range(1, 10 + 1):
                for j in range(1, 10 + 1):
                    square = pygame.Rect(x + j * 10, y + i * 10, w, h)
                    if can_be_placed() == 'True':
                        pygame.draw.rect(SCREEN, (0, 100, 255), squere, 8)
            pygame.display.flip()
        pygame.quit()"""

    """def draw_sea(weidth, height):
        weidth = size
        height = size
        draw_cell()
        can_be_placed()
        set_ships()
        p = draw_cell(0, 0, 10, 10)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            for i in range(1, 10 + 1):
                for j in range(1, 10 + 1):
                    square = pygame.Rect(x + j * 10, y + i * 10, w, h)
                    if can_be_placed() == 'True':
                        pygame.draw.rect(SCREEN, (0, 100, 255), squere, 8)
                    if can_be_placed() == 'False':
                        pygame.draw.rect(SCREEN, (10, 10, 255), squere, 8)
                    if set_ships() == 'True':
                        pygame.draw.rect(SCREEN, (0, 10, 55), squere, 8)
            pygame.display.flip()
        pygame.quit()"""

    """def mouse_pos_to_sea_coordinate(x, y):
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = mouse_pos_to_coordinate(pg.mouse.get_pos())
            make_shot(x, y)
            return x, y"""


def __main__():
    sea = Sea()
    sea.set_ships()
    sea.draw_with_ships()

    x = 0
    y = 0
    w = 50
    h = 50
    color = (0, 0, 255)
    size = 600

    def draw_cell():
        pygame.init()
        screen = pygame.display.set_mode((size, size))
        pygame.display.set_caption("Морской бой")
        screen.fill((color))
        running = True
        pygame.event.get()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            for i in range(1, 10 + 1):
                for j in range(1, 10 + 1):
                    x = j * 50
                    y = i * 50
                    if sea.sea[i - 1][j - 1] == 1:
                        square = pygame.Rect(x, y, w, h)
                        pygame.draw.rect(screen, (100, 100, 155), square, 10000000)
                    else:
                        square = pygame.Rect(x, y, w, h)
                        pygame.draw.rect(screen, (0, 10, 55), square, 1)
            pygame.display.flip()
        pygame.quit()

    draw_cell()



if __name__ == "__main__":
    __main__()
