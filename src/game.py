from enum import Flag

# supports `~` for inverse
class Cell(Flag):
    DEAD = 0
    LIVE = 1

    def dead(self) -> bool:
        return self == Cell.DEAD

    def live(self) -> bool:
        return self == Cell.LIVE

    # next generation of cell
    def next(self, live_neighbours: int):# -> Cell:
        match live_neighbours:
            case 3: return Cell.LIVE
            case 2: return self
            case _: return Cell.DEAD

    def __str__(self):
        match self:
            case Cell.DEAD:
                return "X"
            case Cell.LIVE:
                return "O"

class Life:
    # creates board with all cells dead
    # TODO: test for size 0
    def __init__(self, width: int, height: int):
        self.board = [[Cell.DEAD] * width for _ in range(height)]
        self.width = width
        self.height = height

    # cell at coords x, y
    def cell(self, x: int, y: int) -> Cell:
        return self.board[y][x]

    def toggle_cell(self, x: int, y: int):
        self.board[y][x] = ~self.board[y][x]

    # evolve board to next generation
    def evolve(self):
        next = Life(self.width, self.height).board

        for x in range(self.width):
            for y in range(self.height):
                c = self.board[y][x]
                live_neighbours = self.live_neighbours(x, y)
                next[y][x] = c.next(live_neighbours)

        self.board = next

    # number of live neighbours
    def live_neighbours(self, x: int, y: int) -> int:
        result = 0

        for c in self.neighbours(x, y):
            if c.live(): result += 1

        return result

    # neighbour (list of neighbouring cells)
    #   3 * 3 grid around central passed cell
    # does not consider passed central cell
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
                if not (x_offset == 0 and y_offset == 0):
                    result.append(self.cell(
                        x + x_offset,
                        y + y_offset
                    ))

        return result

    def __str__(self):
        return '\n'.join([' '.join([
            str(c) for c in l
        ]) for l in self.board])
