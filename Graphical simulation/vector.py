import math
class Vec2D():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if type(other) == type(1) or type(other) == type(1.0):
            return Vec2D(self.x * other, self.y * other)
        return self.x * other.x + self.y * other.y

    def __truediv__(self, other):
        return Vec2D(self.x/other, self.y/other)

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return '(%g, %g)' % (self.x, self.y)

    def __divmod__(self, other):
        return Vec2D(self)

    def __ne__(self, other):
        return not self.__eq__(other)

    def norm(self, int):
        if int == 2:
            result = (self.x**2 + self.y**2)**0.5
        else:
            result = (self.x**4 + self.y**4)**0.25
        return result
