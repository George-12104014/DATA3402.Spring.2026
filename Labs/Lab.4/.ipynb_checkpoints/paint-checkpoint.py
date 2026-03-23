import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle as MplRectangle, Circle as MplCircle, Polygon


class Canvas:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.items = []

    def add(self, shape):
        self.items.append(shape)

    def paint(self):
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_aspect("equal")
        ax.grid(True)

        for item in self.items:
            item.paint(ax)

        plt.show()


class Shape:
    def area(self):
        raise NotImplementedError

    def perimeter(self):
        raise NotImplementedError

    def get_points(self, n=16):
        raise NotImplementedError

    def contains_point(self, x, y):
        raise NotImplementedError

    def overlaps(self, other):
        for px, py in self.get_points():
            if other.contains_point(px, py):
                return True

        for px, py in other.get_points():
            if self.contains_point(px, py):
                return True

        return False


class Rectangle(Shape):
    def __init__(self, length, width, x, y):
        self.length = length
        self.width = width
        self.x = x
        self.y = y

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * (self.length + self.width)

    def get_points(self, n=16):
        points = [
            (self.x, self.y),
            (self.x + self.length, self.y),
            (self.x + self.length, self.y + self.width),
            (self.x, self.y + self.width)
        ]
        return points[:16]

    def contains_point(self, x, y):
        return self.x <= x <= self.x + self.length and self.y <= y <= self.y + self.width

    def paint(self, ax):
        ax.add_patch(MplRectangle((self.x, self.y), self.length, self.width, fill=False))

    def __repr__(self):
        return f"Rectangle({repr(self.length)}, {repr(self.width)}, {repr(self.x)}, {repr(self.y)})"


class Circle(Shape):
    def __init__(self, radius, x, y):
        self.radius = radius
        self.x = x
        self.y = y

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius

    def get_points(self, n=16):
        points = []
        n = min(n, 16)

        for i in range(n):
            angle = 2 * math.pi * i / n
            px = self.x + self.radius * math.cos(angle)
            py = self.y + self.radius * math.sin(angle)
            points.append((px, py))

        return points

    def contains_point(self, x, y):
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.radius ** 2

    def paint(self, ax):
        ax.add_patch(MplCircle((self.x, self.y), self.radius, fill=False))

    def __repr__(self):
        return f"Circle({repr(self.radius)}, {repr(self.x)}, {repr(self.y)})"


class Triangle(Shape):
    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3

    def area(self):
        return abs(
            self.x1 * (self.y2 - self.y3)
            + self.x2 * (self.y3 - self.y1)
            + self.x3 * (self.y1 - self.y2)
        ) / 2

    def perimeter(self):
        side1 = math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)
        side2 = math.sqrt((self.x3 - self.x2) ** 2 + (self.y3 - self.y2) ** 2)
        side3 = math.sqrt((self.x1 - self.x3) ** 2 + (self.y1 - self.y3) ** 2)
        return side1 + side2 + side3

    def get_points(self, n=16):
        points = [
            (self.x1, self.y1),
            (self.x2, self.y2),
            (self.x3, self.y3)
        ]
        return points[:16]

    def contains_point(self, x, y):
        denominator = ((self.y2 - self.y3) * (self.x1 - self.x3) +
                       (self.x3 - self.x2) * (self.y1 - self.y3))

        if denominator == 0:
            return False

        a = ((self.y2 - self.y3) * (x - self.x3) +
             (self.x3 - self.x2) * (y - self.y3)) / denominator

        b = ((self.y3 - self.y1) * (x - self.x3) +
             (self.x1 - self.x3) * (y - self.y3)) / denominator

        c = 1 - a - b

        return 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1

    def paint(self, ax):
        ax.add_patch(Polygon([(self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3)], fill=False))

    def __repr__(self):
        return f"Triangle({repr(self.x1)}, {repr(self.y1)}, {repr(self.x2)}, {repr(self.y2)}, {repr(self.x3)}, {repr(self.y3)})"


class CompoundShape(Shape):
    def __init__(self, shapes=None):
        if shapes is None:
            self.shapes = []
        else:
            self.shapes = shapes

    def add(self, shape):
        self.shapes.append(shape)

    def area(self):
        total = 0
        for shape in self.shapes:
            total += shape.area()
        return total

    def perimeter(self):
        total = 0
        for shape in self.shapes:
            total += shape.perimeter()
        return total

    def get_points(self, n=16):
        points = []
        for shape in self.shapes:
            points.extend(shape.get_points(n))
        return points[:16]

    def contains_point(self, x, y):
        for shape in self.shapes:
            if shape.contains_point(x, y):
                return True
        return False

    def paint(self, ax):
        for shape in self.shapes:
            shape.paint(ax)

    def __repr__(self):
        return f"CompoundShape({repr(self.shapes)})"


class RasterDrawing:
    def __init__(self, width=10, height=10, shapes=None):
        self.width = width
        self.height = height
        if shapes is None:
            self.shapes = []
        else:
            self.shapes = shapes

    def add_shape(self, shape):
        self.shapes.append(shape)

    def remove_shape(self, index):
        del self.shapes[index]

    def paint(self):
        canvas = Canvas(self.width, self.height)
        for shape in self.shapes:
            canvas.add(shape)
        canvas.paint()

    def save(self, filename):
        f = open(filename, "w")
        f.write(repr(self))
        f.close()

    def __repr__(self):
        return f"RasterDrawing({repr(self.width)}, {repr(self.height)}, {repr(self.shapes)})"


def load_drawing(filename):
    f = open(filename, "r")
    drawing = eval(f.read())
    f.close()
    return drawing
