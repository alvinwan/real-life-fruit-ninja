"""Game of ninja for geometric shapes."""

import numpy as np
import cv2


def dist(x1, x2, y1, y2):
    return ((x2 - x1) ** 2. + (y2 - y1) ** 2.) ** 0.5


class Ninja:

    frame_name = 'ninja'

    def __init__(self, width: int, height: int):
        self.shapes = []
        self.garbage = []
        self.probability_shape_spawn = 0.05
        self.height = height
        self.width = width

    def update(self):
        for i, shape in enumerate(self.shapes):
            shape['y'] += shape['vy']
            if shape['y'] > self.height:
                self.garbage.append(shape)

        if np.random.random() < self.probability_shape_spawn:
            x = int(np.random.random() * self.width)
            self.add_circle(x, 10)

        for shape in self.garbage:
            if shape in self.shapes:
                self.shapes.remove(shape)
        self.garbage = []

    def draw(self, frame: np.array):
        for shape in self.shapes:
            shape['draw'](frame, shape['y'])

    def check(self, mag, ang, frame):
        """Check if any of the shapes have been touched.

        (In the future, check if any have been sliced.)
        """
        ys, xs = np.nonzero(mag > 35)
        self.any_strike(xs, ys)
        for x, y in zip(xs, ys):
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    def add_circle(self, x: int, r: int, color: tuple=(0, 0, 255), vy: int=10):
        self.shapes.append({
            'x': x,
            'y': 0,
            'vy': vy,
            'draw': lambda frame, y: cv2.circle(frame, (x, y), r, color, -1),
            'any_touch': lambda x, y, shape: \
                (dist(x, shape['x'], y, shape['y']) <= r).any(),
        })

    def any_strike(self, x, y):
        for i, shape in enumerate(self.shapes):
            if shape['any_touch'](x, y, shape):
                self.garbage.append(shape)

    def on_mouse(self, event, x, y, flags, param):
        self.any_strike(x, y)

    def bind_mouse_callback(self):
        cv2.namedWindow(self.frame_name)
        cv2.setMouseCallback(self.frame_name, self.on_mouse)


if __name__ == '__main__':
    game = Ninja(420, 640)
    cap = cv2.VideoCapture(0)
    game.bind_mouse_callback()

    while True:
        _, frame = cap.read()
        frame = cv2.resize(frame, (640, 420))

        game.update()
        game.draw(frame)
        cv2.imshow(game.frame_name, frame)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
