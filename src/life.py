from enum import Flag

# Game of Life cell state (dead or alive).
class CellState(Flag):
    DEAD = 0
    LIVE = 1

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

    # Returns whether or not the `Cell` is dead.
    def is_dead(self) -> bool:
        return self.state == CellState.DEAD

    # Returns whether or not the `Cell` is alive.
    def is_live(self) -> bool:
        return self.state == CellState.LIVE

    # Evolves the `Cell` by one generation.
    def evolve(self, live_neighbours: int):
        match live_neighbours:
            case 3: self.state = CellState.LIVE
            case 2: pass
            case _: self.state = CellState.DEAD

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
    # Creates board with all cells dead.
    def __init__(self, width: int, height: int):
        # if we directly multiply the lists, all elements of a row point to the
        # same `Cell` , which is not what we want
        self.board = [[
            Cell(CellState.DEAD) for _ in range(width)
        ] for _ in range(height)]

        self.width = width
        self.height = height

    # Evolves the `Game` by one generation.
    def evolve(self):
        # deep copy of the board
        next = [[
            c.copy() for c in l
        ] for l in self.board]

        # evolve each cell of the new board
        for x in range(self.width):
            for y in range(self.height):
                live = self.live_neighbours(x, y)
                next[y][x].evolve(live)

        self.board = next

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
    # compares game boards
    def eq(a: list[list[Cell]], b: list[list[Cell]]) -> bool:
        assert len(a) == len(b)
        assert len(a[0]) == len(b[0])

        for x in range(len(a)):
            for y in range(len(a[0])):
                if a[y][x] != b[y][x]:
                    return False

        return True

    g = Game(3, 3)

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
