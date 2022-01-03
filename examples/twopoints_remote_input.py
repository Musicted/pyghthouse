from random import random

import numpy as np
from PIL import Image, ImageDraw

from pyghthouse.utils import from_hsv
from pyghthouse import Pyghthouse, KeyEvent

from config import UNAME, TOKEN

SPEED_FACTOR = 0.02
COLOR_SPEED = 0.01


class BouncyPoint:

    def __init__(self):
        self.x = random()
        self.y = random()
        self.vx = SPEED_FACTOR * (random() + 0.5)
        self.vy = SPEED_FACTOR * (random() + 0.5)

    def update(self):
        self.x += self.vx
        self.y += self.vy

        if self.x < 0:
            self.vx *= -1
            self.x *= -1
        elif self.x > 1:
            self.vx *= -1
            self.x = 2 - self.x
        if self.y < 0:
            self.vy *= -1
            self.y *= -1
        elif self.y > 1:
            self.vy *= -1
            self.y = 2 - self.y


class ImageMaker:

    def __init__(self):
        self.p1 = BouncyPoint()
        self.p2 = BouncyPoint()
        self.img = Image.new('RGB', (280, 140))
        self.draw = ImageDraw.Draw(self.img)
        self.hue = 0.0
        self.pressed_keys = {'l': False, 'u': False, 'r': False, 'd': False,
                             'L': False, 'U': False, 'R': False, 'D': False}

    def callback(self, events):
        for e in filter(lambda x: x is not None and isinstance(x, KeyEvent), events):
            if e.code == 37:
                self.pressed_keys['l'] = e.down
            if e.code == 38:
                self.pressed_keys['u'] = e.down
            if e.code == 39:
                self.pressed_keys['r'] = e.down
            if e.code == 40:
                self.pressed_keys['d'] = e.down
            if e.code == 65:
                self.pressed_keys['L'] = e.down
            if e.code == 87:
                self.pressed_keys['U'] = e.down
            if e.code == 68:
                self.pressed_keys['R'] = e.down
            if e.code == 83:
                self.pressed_keys['D'] = e.down

        self.p1.vx = (self.pressed_keys['r'] - self.pressed_keys['l']) * SPEED_FACTOR
        self.p1.vy = (self.pressed_keys['d'] - self.pressed_keys['u']) * SPEED_FACTOR
        self.p2.vx = (self.pressed_keys['R'] - self.pressed_keys['L']) * SPEED_FACTOR
        self.p2.vy = (self.pressed_keys['D'] - self.pressed_keys['U']) * SPEED_FACTOR
        self.p1.update()
        self.p2.update()
        self.hue += COLOR_SPEED
        self.draw.line([(self.p1.x * 280, self.p1.y * 140), (self.p2.x * 280, self.p2.y * 140)], width=10,
                       fill=tuple(from_hsv(self.hue, 1, 1)))

        output = self.img.copy()
        draw2 = ImageDraw.Draw(output)
        draw2.rectangle((self.p1.x * 280 - 6, self.p1.y * 140 - 6, self.p1.x * 280 + 6, self.p1.y * 140 + 6),
                        fill=(255, 255, 255), outline=(255, 255, 255))
        draw2.rectangle((self.p2.x * 280 - 6, self.p2.y * 140 - 6, self.p2.x * 280 + 6, self.p2.y * 140 + 6),
                        fill=(0, 0, 0), outline=(0, 0, 0))
        output.thumbnail((28, 14))
        return np.asarray(output)


if __name__ == '__main__':
    i = ImageMaker()
    p = Pyghthouse(UNAME, TOKEN, image_callback=i.callback, frame_rate=60, stream_remote_inputs=True)
    p.start()
