from pyghthouse import Pyghthouse, VerbosityLevel
from config import UNAME, TOKEN


def clip(val, min_val, max_val):
    if val < min_val:
        return min_val
    if val > max_val:
        return max_val
    return val


def main_loop():
    x = 0
    y = 0
    p = Pyghthouse(UNAME, TOKEN, verbosity=VerbosityLevel.NONE)
    p.start()
    while True:
        img = p.empty_image()
        img[y][x] = [255, 255, 255]
        p.set_image(img)
        s = input()
        for c in s.upper():
            if c == 'A':
                x -= 1
            elif c == 'D':
                x += 1
            elif c == 'W':
                y -= 1
            elif c == 'S':
                y += 1
        x = clip(x, 0, 27)
        y = clip(y, 0, 13)


if __name__ == '__main__':
    main_loop()
