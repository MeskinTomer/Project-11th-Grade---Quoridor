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

    def get_wall_status(self, side: str) -> str:
        ret_val = 'Invalid'
        if side == 'up':
            ret_val = self.up
        elif side == 'down':
            ret_val = self.down
        elif side == 'right':
            ret_val = self.right
        elif side == 'left':
            ret_val = self.left
        return ret_val
