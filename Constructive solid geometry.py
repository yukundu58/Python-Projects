from abc import ABC, abstractmethod
import tkinter as tk


CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500


class Drawable(ABC):
    @abstractmethod
    def __contains__(self, point):
        pass

    def __and__(self, other):
        return Intersection(self, other)

    def __or__(self, other):
        return Union(self, other)

    def __sub__(self, other):
        return Difference(self, other)

    def draw(self, canvas):
        height = int(canvas['height'])
        width = int(canvas['width'])

        for y_tk in range(height):
            y = height/2 - y_tk
            for x_tk in range(width):
                x = -height/2 + x_tk
                if (x, y) in self:
                    draw_pixel(canvas, x_tk, y_tk)


class Circle(Drawable):
    def __init__(self, x=0.0, y=0.0, r=1.0):
        self.x = float(x)
        self.y = float(y)
        self.r = float(r)

    def __contains__(self, point):
        x, y = point
        return (x - self.x)**2 + (y - self.y)**2 - self.r**2 < 0

    def __repr__(self):
        return 'Circle(x={0.x}, y={0.y}, r={0.r})'.format(self)


class Rectangle(Drawable):
    def __init__(self, x0, y0, x1, y1):
        self.x0, self.y0 = float(x0), float(y0)
        self.x1, self.y1 = float(x1), float(y1)

    def __contains__(self, point):
        x0, y0 = point
        return (self.x0 <= x0 <= self.x1) and (self.y0 <= y0 <= self.y1)

    def __repr__(self):
        return 'Rectangle(LL=({0.x0},{0.y0}), UR=({0.x1},{0.y1}))'.format(self)


class Intersection(Drawable):
    def __init__(self, shape1, shape2):
        self.shape1 = shape1
        self.shape2 = shape2

    def __contains__(self, point):
        return (point in self.shape1) and (point in self.shape2)

    def __repr__(self):
        return '({0.shape1} & {0.shape2})'.format(self)


class Union(Drawable):
    def __init__(self, shape1, shape2):
        self.shape1 = shape1
        self.shape2 = shape2

    def __contains__(self, point):
        return (point in self.shape1) or (point in self.shape2)

    def __repr__(self):
        return '({0.shape1} | {0.shape2})'.format(self)


class Difference(Drawable):
    def __init__(self, shape1, shape2):
        self.shape1 = shape1
        self.shape2 = shape2

    def __contains__(self, point):
        return (point in self.shape1) and (point not in self.shape2)

    def __repr__(self):
        return '({0.shape1} - {0.shape2})'.format(self)


def draw_pixel(canvas, x, y, color='blue'):
    """Draw a pixel at (x,y) on the given canvas"""
    x1, y1 = x - 1, y - 1
    x2, y2 = x + 1, y + 1
    canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)


def main(shape):
    """Create a main window with a canvas to draw on"""
    master = tk.Tk()
    master.title("Drawing")
    canvas = tk.Canvas(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
    canvas.pack(expand=tk.YES, fill=tk.BOTH)

    # Render the user-defined shape
    shape.draw(canvas)

    # Start the Tk event loop (in this case, it doesn't do anything other than
    # show the window, but we could have defined "event handlers" that intercept
    # mouse clicks, keyboard presses, etc.)
    tk.mainloop()


if __name__ == '__main__':
    # Create a "happy" face by subtracting two eyes and a mouth from a head
    head = Circle(0, 0, 200)
    left_eye = Circle(-70, 100, 20)
    right_eye = Circle(70, 100, 20)
    mouth = Rectangle(-90, -80, 90, -60)
    happy_face = head - left_eye - right_eye - mouth

    # Draw the happy face
    main(happy_face)
