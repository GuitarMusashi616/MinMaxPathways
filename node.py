class Node:
    def __init__(self, parent):
        self.parent = parent
        self.children = []
        self.coord = None
        self.win_loss_draw = None
        self.grid = None
        self.depth = None
        self.pick = None
        self.choices = None
        self.func = None

    def __repr__(self):
        if self.win_loss_draw is None:
            return f"NODE @ depth: {self.depth}"
        elif self.win_loss_draw >= 1:
            return f"WIN @ depth: {self.depth}"
        elif self.win_loss_draw <= -1:
            return f"LOSS @ depth: {self.depth}"
        elif self.win_loss_draw == 0:
            return f"DRAW @ depth: {self.depth}"
