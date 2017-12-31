"""Main game script for real-life fruit ninja."""

from ninja import Ninja
import numpy as np
import cv2


def main():
    game = Ninja(420, 640)
    cap = cv2.VideoCapture(0)

    # setup optical flow
    _, frame1 = cap.read()
    frame1 = cv2.resize(frame1, (640, 360))
    prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[..., 1] = 255

    while True:
        _, frame = cap.read()
        frame = cv2.resize(frame, (640, 360))

        # compute optical flow
        next = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(
            prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        frame = frame + bgr

        game.update()
        game.check(mag, ang, frame)
        game.draw(frame)
        cv2.imshow(game.frame_name, frame)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break


if __name__ == '__main__':
    main()
