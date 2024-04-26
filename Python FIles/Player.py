class Player:
    def __init__(self, x: int, y: int, block: list):
        self.x = x
        self.y = y
        self.block = block

    def get_coordinates(self) -> tuple:
        return self.x, self.y

    def move_up(self) -> None:
        self.y -= 80
        self.block[0] -= 1

    def move_down(self) -> None:
        self.y += 80
        self.block[0] += 1

    def move_right(self) -> None:
        self.x += 80
        self.block[1] += 1

    def move_left(self) -> None:
        self.x -= 80
        self.block[1] -= 1
