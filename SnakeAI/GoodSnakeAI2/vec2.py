class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def copy(self):
        return Vec2(self.x, self.y)
