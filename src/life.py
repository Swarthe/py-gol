import pygame as pg

from enum import Flag

COLOUR_DEAD = (0,   0,   0  )
COLOUR_LIVE = (255, 255, 255)

# Arc-dark hehe
COLOUR_ADVICE = (102, 168, 246)

# Game of Life cell state (dead or alive).
class CellState(Flag):
    DEAD = 0
    LIVE = 1

    # Returns the corresponding colour.
    def colour(self) -> (int, int, int):
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

# Game of Life Cell
class Cell:
    def __init__(self, state: CellState):
        self.state = state

    # Evolves the `Cell` by one generation.
    def evolve(self, live_neighbours: int):
        match live_neighbours:
            case 3: self.state = CellState.LIVE
            case 2: pass
            case _: self.state = CellState.DEAD

    # Returns the colour corresponding to the state of the `Cell`.
    def colour(self) -> (int, int, int):
        return self.state.colour()

    # Returns whether or not the `Cell` is dead.
    def is_dead(self) -> bool:
        return self.state == CellState.DEAD

    # Returns whether or not the `Cell` is alive.
    def is_live(self) -> bool:
        return self.state == CellState.LIVE

    # Switches the state of the cell
    def toggle(self):
        self.state = ~self.state

    def copy(self):
        return Cell(self.state)

    def __eq__(self, rhs):
        return self.state == rhs.state

    def __str__(self):
        return str(self.state)

# Game of Life board
class Game:
    # Creates board with all cells dead. `cell_size` is in pixels.
    def __init__(self, width: int, height: int, cell_size: int):
        # if we directly multiply the lists, all elements of a row point to the
        # same `Cell` , which is not what we want
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
        pg.display.flip()

    # Displays user advice for `start()`.
    def advise_user(self):
        font = pg.font.SysFont(None, 30)

        text = [
            font.render("Cliquez sur la fenêtre pour modifier des cellules",
                        True, COLOUR_ADVICE),
            font.render("Quand vous avez fini, appuyez sur la touche entrée",
                        True, COLOUR_ADVICE)
        ]

        pos = [text[i].get_rect(center = (
            (self.width * self.cell_size)  // 2,
            (self.height * self.cell_size)  // 10 + (i * 30)
        )) for i in range(len(text))]

        for i in range(len(text)):
            self.screen.blit(text[i], pos[i])

        pg.display.flip()

    # Starts interactive board, with `time` in milliseconds between each
    # evolution of the game.
    #
    # At first, the user clicks on the cells they want to toggle. When done,
    # they may press the enter key to begin the game. They may also quit through
    # keyboard shortcuts at this point.
    def start(self, time: int):
        pg.event.clear()

        while True:
            event = pg.event.wait()

            match event.type:
                case pg.QUIT:
                    pg.quit()

                case pg.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos

                    self.toggle(
                        mouse_x // self.cell_size,
                        mouse_y // self.cell_size
                    )

                case pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.__run(time)

    # Iterates through generations of the game every `time` milliseconds.
    def __run(self, time: int):
        while True:
            self.evolve()
            self.clock.tick()
            pg.time.wait(time)

    # Evolves the `Game` by one generation.
    def evolve(self):
        # deep copy of the board
        next = [[
            c.copy() for c in l
        ] for l in self.board]

        self.__clear()

        # evolve each cell of the new board
        for x in range(self.width):
            for y in range(self.height):
                live = self.live_neighbours(x, y)
                next[y][x].evolve(live)
                self.__update(x, y)

        pg.display.flip()

        self.board = next

    # Update a `Cell` of the PyGame window.
    def __update(self, x, y):
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

    # Clears the PyGame window.
    def __clear(self):
        self.screen.fill(COLOUR_DEAD)

    # Toggles `Cell` at coordinates (`x`, `y`)
    def toggle(self, x: int, y: int) -> Cell:
        self.cell(x, y).toggle()
        self.__update(x, y)
        pg.display.flip()

    # Returns `Cell` at coordinates (`x`, `y`)
    def cell(self, x: int, y: int) -> Cell:
        return self.board[y][x]

    # Returns the number of live neighbours of a `Cell`.
    def live_neighbours(self, x: int, y: int) -> int:
        return sum(
            c.is_live() for c in self.neighbours(x, y)
        )

    # Returns a list of the neighbouring of a `Cell`.
    #
    # The cell at coordinates (`x`, `y`) is not included in this list, which
    # will never contain more than 8 cells.
    def neighbours(self, x: int, y: int) -> list[Cell]:
        range_x = range(
            -1 if x > 0 else 0,
            2 if x + 1 < self.width else 1
        )

        range_y = range(
            -1 if y > 0 else 0,
            2 if y + 1 < self.height else 1
        )

        result = []

        for x_offset in range_x:
            for y_offset in range_y:
                # ignore central cell
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

# Basic soundness test
def test():
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
