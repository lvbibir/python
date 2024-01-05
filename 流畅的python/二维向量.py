from math import hypot


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Vector({self.x}, {self.y})'

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        """
        自定义的布尔值, 默认情况下, 我们自己定义的类的实例总被认为是 True
        bool(x) 的背后是调用 x.__bool__(), 如果不存在则调用 x.__len__()
        """
        # return bool(self.x or self.y)
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)


v1 = Vector(2, 4)
v2 = Vector(2, 1)
print(v1 + v2)
v = Vector(3, 4)
print(v * 3)
print(abs(v * 3))
