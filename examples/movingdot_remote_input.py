from pyghthouse import Pyghthouse, VerbosityLevel, KeyEvent
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
    p = Pyghthouse(UNAME, TOKEN, verbosity=VerbosityLevel.NONE, stream_remote_inputs=True)
    p.start()
    while True:
        img = p.empty_image()
        img[y][x] = [255, 255, 255]
        p.set_image(img)
        for e in p.get_all_events():
            if isinstance(e, KeyEvent) and e.down:
                if e.code == 65:  # A
                    x -= 1
                elif e.code == 68:  # D
                    x += 1
                elif e.code == 87:  # W
                    y -= 1
                elif e.code == 83:  # S
                    y += 1
        x = clip(x, 0, 27)
        y = clip(y, 0, 13)


if __name__ == '__main__':
    main_loop()
