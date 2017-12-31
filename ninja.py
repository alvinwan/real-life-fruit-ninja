"""Game of ninja for geometric shapes."""

import numpy as np
import cv2


class Ninja:

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
                self.garbage.append(i)

        if np.random.random() < self.probability_shape_spawn:
            x = int(np.random.random() * self.width)
            self.add_circle(x, 50)

        for i in self.garbage:
            self.shapes.pop(i)
        self.garbage = []

    def draw(self, frame: np.array):
        for shape in self.shapes:
            shape['draw'](frame, shape['y'])

    def add_circle(self, x: int, r: int, color: tuple=(0, 0, 255), vy: int=10):
        self.shapes.append({
            'y': 0,
            'vy': vy,
            'draw': lambda frame, y: cv2.circle(frame, (x, y), r, color, -1)
        })


if __name__ == '__main__':
    game = Ninja(420, 640)
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 420))
        game.update()
        game.draw(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break