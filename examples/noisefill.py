import numpy as np
from random import random

from config import UNAME, TOKEN
from pyghthouse import Pyghthouse


def image_gen():
    image = np.zeros((14, 28, 3))
    yield image
    while True:
        for y in range(28):
            for j in range(3):
                image[0, y, j] = int(random() * 255)
            yield image
        image = np.roll(image, 1, 0)
        image *= 0.85
        yield image


g = image_gen()


def callback(*args, **kwargs):
    return next(g)


if __name__ == '__main__':
    p = Pyghthouse(UNAME, TOKEN, image_callback=callback, frame_rate=60)
    print("Starting... use CTRL+C to stop.")
    p.start()
