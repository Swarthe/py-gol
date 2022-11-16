import pygame as pg

import random as rand

from enum import Flag


COLOUR_DEAD = (0,   0,   0  )
COLOUR_LIVE = (255, 255, 255)

# Arc-dark hehe
COLOUR_TEXT = (102, 168, 246)
COLOUR_BG   = (0 ,  0,   0  )

# Game of Life cell state (dead or alive).
class CellState(Flag):
    DEAD = 0
    LIVE = 1

    def colour(self) -> (int, int, int):
        '''
        Returns the corresponding colour.
        '''
        match self:
            case CellState.DEAD:
                return COLOUR_DEAD
            case CellState.LIVE:
                return COLOUR_LIVE

    def __str__(self):
        match self:
            case CellState.DEAD:
                return "X"
            case CellState.LIVE:
                return "O"

class Cell:
    '''
    Game of Life cell.
    '''
    def __init__(self, state: CellState):
        self.state = state

    def evolve(self, live_neighbours: int):
        '''
        Evolves the `Cell` by one generation.
        '''
        match live_neighbours:
            case 3: self.state = CellState.LIVE
            case 2: pass
            case _: self.state = CellState.DEAD

    def colour(self) -> (int, int, int):
        '''
        Returns the colour corresponding to the state of the `Cell`.
        '''
        return self.state.colour()

    def is_dead(self) -> bool:
        '''
        Returns whether or not the `Cell` is dead.
        '''
        return self.state == CellState.DEAD

    def is_live(self) -> bool:
        '''
        Returns whether or not the `Cell` is alive.
        '''
        return self.state == CellState.LIVE

    def toggle(self):
        '''
        Switches the state of the cell.
        '''
        self.state = ~self.state

    def copy(self):
        return Cell(self.state)

    def __eq__(self, rhs):
        return self.state == rhs.state

    def __str__(self):
        return str(self.state)

class Game:
    '''
    Game of Life board
    '''
    def __init__(self, width: int, height: int, cell_size: int):
        '''
        Creates board with all cells dead. `cell_size` is in pixels.
        '''
        # if we directly multiply the lists, all elements of a row point to the
        # same `Cell`, which is not what we want
        self.board = [[
            Cell(CellState.DEAD) for _ in range(width)
        ] for _ in range(height)]

        pg.init()
        pg.display.set_caption("Game of Life")

        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.screen = pg.display.set_mode((
            width * cell_size,
            height * cell_size
        ))

        self.clock = pg.time.Clock()

        self.__clear()
        self.evolve()
        pg.display.flip()

    def randomise(self, rand_ratio: float):
        '''
        Randomly toggles a proportion of cells.

        `ratio_live` is a number between 0 and 1 representing the ratio of
        cells to toggle. If it is 0, nothing is done, and a value above 1 is
        considered equivalent to 1. The same cell may be toggled multiple times.
        '''
        if rand_ratio == 0.0:
            return
        elif rand_ratio > 1.0:
            rand_ratio = 1.0

        rand_cells = round(
            rand_ratio * self.width * self.height
        )

        for i in range(rand_cells):
            x, y = (
                rand.randrange(0, self.width),
                rand.randrange(0, self.height)
            )

            self.cell(x, y).toggle()
            self.__display_cell(x, y)

        pg.display.flip()

    def user_edit(self):
        '''
        Allow the user to edit the board.

        At first, the user clicks on the cells they want to toggle. When done,
        they may press the enter key to proceed. They may also quit through
        keyboard shortcuts at this point.
        '''
        self.__advise_user()
        pg.event.clear()

        while True:
            # Wait for user action
            event = pg.event.wait()

            match event.type:
                case pg.QUIT:
                    pg.quit()

                case pg.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos

                    self.toggle(
                        # Derive cell coordinates from mouse position
                        mouse_x // self.cell_size,
                        mouse_y // self.cell_size
                    )

                case pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        return

    def __advise_user(self):
        '''
        Displays user advice for `edit()`.
        '''
        font = pg.font.SysFont(None, 60)
        font_alt = pg.font.SysFont(None, 62)

        text = [
            font.render("Cliquez sur la fenêtre pour modifier des cellules",
                        True, COLOUR_TEXT),
            font.render("Quand vous avez fini, appuyez sur la touche entrée",
                        True, COLOUR_TEXT)
        ]

        pos = [text[i].get_rect(center = (
            # Horizontal middle of the screen.
            (self.width * self.cell_size) // 2,
            # Top of the screen.
            (self.height * self.cell_size) // 10 + (i * 50)
        )) for i in range(len(text))]

        for i in range(len(text)):
            pg.draw.rect(self.screen, COLOUR_BG, pos[i])
            self.screen.blit(text[i], pos[i])

        pg.display.flip()

    def start(self, speed: int):
        '''
        Starts interactive board, with `speed` in milliseconds between each
        evolution of the game.
        '''
        while True:
            self.evolve()
            self.__display_text(f"Cellules vivantes: {self.live_cells()}", 60)
            self.clock.tick()
            pg.time.wait(speed)

    def __display_text(self, text: str, size: int):
        '''
        Renders text to the PyGame display.
        '''
        font = pg.font.SysFont(None, size)
        text = font.render(text, True, COLOUR_TEXT)

        pos = text.get_rect(center = (
            (self.width * self.cell_size) // 2,
            (self.height * self.cell_size) // 10
        ))

        pg.draw.rect(self.screen, COLOUR_BG, pos)
        self.screen.blit(text, pos)
        pg.display.flip()

    def live_cells(self) -> int:
        '''
        Returns total number of live cells.
        '''
        result = 0

        for x in range(self.width):
            for y in range(self.height):
                result += self.cell(x, y).is_live()

        return result

    def evolve(self):
        '''
        Evolves the `Game` by one generation.
        '''
        # Deep copy of the board
        next = [[
            c.copy() for c in l
        ] for l in self.board]

        self.__clear()

        # Evolve each cell of the new board at once
        for x in range(self.width):
            for y in range(self.height):
                live = self.live_neighbours(x, y)
                next[y][x].evolve(live)
                self.__display_cell(x, y)

        pg.display.flip()

        self.board = next

    def __display_cell(self, x, y):
        '''
        Update a `Cell` of the PyGame window.
        '''
        pos = (
            self.cell_size * x,
            self.cell_size * y
        )

        size = (
            self.cell_size,
            self.cell_size
        )

        pg.draw.rect(
            self.screen,
            self.cell(x, y).colour(),
            pg.Rect(pos, size)
        )

    def __clear(self):
        '''
        Clears the PyGame window.
        '''
        self.screen.fill(COLOUR_DEAD)

    def toggle(self, x: int, y: int) -> Cell:
        '''
        Toggles `Cell` at coordinates (`x`, `y`)
        '''
        self.cell(x, y).toggle()
        self.__display_cell(x, y)
        pg.display.flip()

    def cell(self, x: int, y: int) -> Cell:
        '''
        Returns `Cell` at coordinates (`x`, `y`)
        '''
        return self.board[y][x]

    def live_neighbours(self, x: int, y: int) -> int:
        '''
        Returns the number of live neighbours of a `Cell`.
        '''
        return sum(
            c.is_live() for c in self.neighbours(x, y)
        )

    def neighbours(self, x: int, y: int) -> list[Cell]:
        '''
        Returns a list of the neighbouring of a `Cell`.

        The cell at coordinates (`x`, `y`) is not included in this list, which
        will never contain more than 8 cells.
        '''
        # Ignore cells beyond the edge of the board
        range_x = range(
            -1 if x > 0 else 0,
            2 if x + 1 < self.width else 1
        )

        range_y = range(
            -1 if y > 0 else 0,
            2 if y + 1 < self.height else 1
        )

        result = []

        # Iterate through the surrounding cells.
        for x_offset in range_x:
            for y_offset in range_y:
                # Ignore the central cell
                if (x_offset, y_offset) != (0, 0):
                    result.append(self.cell(
                        x + x_offset,
                        y + y_offset
                    ))

        return result

    def __str__(self):
        return '\n'.join([' '.join([
            str(c) for c in l
        ]) for l in self.board])

def test():
    '''
    Basic soundness test.
    '''
    # Compares game boards.
    def eq(a: list[list[Cell]], b: list[list[Cell]]) -> bool:
        assert len(a) == len(b)
        assert len(a[0]) == len(b[0])

        for x in range(len(a)):
            for y in range(len(a[0])):
                if a[y][x] != b[y][x]:
                    return False

        return True

    g = Game(3, 3, 1)

    # 3x1 blinker, oscillates between 2 states every generation
    for i in range(3):
        g.cell(i, 1).toggle()

    assert len(g.neighbours(1, 1)) == 8
    assert len(g.neighbours(1, 2)) == 5
    assert len(g.neighbours(2, 1)) == 5
    assert len(g.neighbours(2, 2)) == 3

    assert g.live_neighbours(1, 2) == 3
    assert g.live_neighbours(1, 1) == 2
    assert g.live_neighbours(2, 2) == 2
    assert g.live_neighbours(2, 1) == 1

    # generations of the game of life
    gens = [g.board]

    # get two more generations
    for _ in range(2):
        g.evolve()
        gens.append(g.board)

    # the blinker should return to its original state after 2 generations
    assert eq(gens[0], gens[2])

    print("Tests passed")
