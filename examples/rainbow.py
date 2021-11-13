from pyghthouse import Pyghthouse
from pyghthouse.utils._color import from_hsv
from config import UNAME, TOKEN


def rainbow_generator():
    while True:
        for i in range(180):
            yield [from_hsv((i / 180 + j / (14 * 28)) % 1.0, 1.0, 1.0) for j in range(14 * 28)]


rainbow = rainbow_generator()


def callback():
    return next(rainbow)


if __name__ == '__main__':
    p = Pyghthouse(UNAME, TOKEN, image_callback=callback)
    print("Starting... use CTRL+C to stop.")
    p.start()

