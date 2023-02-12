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
        for decks in [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]:
            while True:
                ship = Ship(randint(0, self.size - decks), randint(0, self.size - decks), choice([H, V]), decks)
                if self.can_be_placed(ship):
                    self.place_ship(ship)
                    break

    def get_cell(self, x, y):
        return self.sea[x][y]

    def make_shot(self, x, y):
        if self.sea[x][y] in [0, 4]:
            self.sea[x][y] = 3
            return MISS
        """if self.sea[x][y] == 1:
            self.sea[x][y] = 8
            if self.ship_was_destroyed(self, x, y):
                return HIT
            if not self.ship_was_destroyed(self, x, y):
                return KILLED"""


    """def ship_was_destroyed(self, x, y):
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


def mouse_pos_to_coordinate(coord):
    y, x = coord
    x = (x // 50) - 1
    y = (y // 50) - 1
    return (x, y)

def __main__():
    sea = Sea()
    sea.set_ships()
    sea.draw_with_ships()

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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_, y_ = mouse_pos_to_coordinate(pygame.mouse.get_pos())
                    sea.make_shot(x_, y_)
            for i in range(1, 10 + 1):
                for j in range(1, 10 + 1):
                    x = j * 50
                    y = i * 50
                    if sea.sea[i - 1][j - 1] == 1:
                        square = pygame.Rect(x, y, w, h)
                        pygame.draw.rect(screen, (100, 100, 155), square)
                    elif sea.sea[i - 1][j - 1] == 3:
                        pygame.draw.rect(screen, (0, 0, 0), square)
                    else:
                        square = pygame.Rect(x, y, w, h)
                        pygame.draw.rect(screen, (0, 10, 55), square, 1)
            pygame.display.flip()
        pygame.quit()

    draw_cell()



if __name__ == "__main__":
    __main__()
