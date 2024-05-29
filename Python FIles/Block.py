class Block:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.player = 0
        self.up = 'clear'
        self.down = 'clear'
        self.right = 'clear'
        self.left = 'clear'

    def update_position(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def get_position(self) -> tuple:
        return self.x, self.y

    def update_player(self, player: int) -> None:
        self.player = player

    def update_wall(self, side: str) -> None:
        if side == 'up':
            self.up = 'blocked'
        elif side == 'down':
            self.down = 'blocked'
        elif side == 'right':
            self.right = 'blocked'
        elif side == 'left':
            self.left = 'blocked'

    def restart_block(self) -> None:
        self.player = 0
        self.up = 'clear'
        self.down = 'clear'
        self.right = 'clear'
        self.left = 'clear'
