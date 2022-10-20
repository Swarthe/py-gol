
class Game:
    def __init__(self, x: int, y: int):
        self.game = [
            # TODO: could be cleaner ?
            [[False] * x for _ in range(y)]
        ]
    
    def __repr__(self):
        # TODO: fix individual lines
        return '\n'.join([str(l) for l in self.game])

t = Game(4,3)
print(t)