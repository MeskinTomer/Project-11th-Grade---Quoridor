class Wall:
    def __init__(self, x: int, y: int, side: str):
        self.x = x
        self.y = y
        self.side = side

    def get_coordinates(self) -> tuple:
        return self.x, self.y
