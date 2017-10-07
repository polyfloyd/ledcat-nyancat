import os.path as path
import random
import sys
import time
from PIL import Image # Requires the Pillow library

background_color = (0x0f, 0x4d, 0x8f)
tail_colors = [
    (0xff, 0x00, 0x00),
    (0xff, 0x99, 0x00),
    (0xff, 0xff, 0x00),
    (0x00, 0xff, 0x00),
    (0x00, 0x99, 0xff),
    (0x66, 0x33, 0xff),
]

anim_cat = []
for i in range(0, 6):
    frame = Image.open('%s/cat/%d.png' % (path.dirname(__file__), i))
    assert (32, 16) == frame.size
    anim_cat.append(frame)
anim_sparkle = []
for i in range(0, 5):
    frame = Image.open('%s/sparkle/%d.png' % (path.dirname(__file__), i))
    anim_sparkle.append(frame)


class Sparkle(object):
    def __init__(self, w, h):
        half_h = anim_sparkle[0].size[1] // 2
        self.x = random.randint(0, w)
        self.y = random.randint(half_h, h - half_h)
        self.frame_index = 0

class Nyancat(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.frame_index = 0
        self.sparkles = []

    def render(self):
        self.frame_index = (self.frame_index + 1) % len(anim_cat)
        anim_frame = anim_cat[self.frame_index]

        if len(self.sparkles) < 32:
            self.sparkles.append(Sparkle(self.width, self.height))

        frame = bytearray(self.width * self.height * 3)
        # Render the background
        for i in range(self.width * self.height):
            frame[i*3:i*3+3] = background_color

        # Render the tail
        for (x, tail_y) in enumerate(self.plot_tail(self.width - 10)):
            for (y, color) in enumerate(tail_colors, tail_y - len(tail_colors) // 2):
                if 0 <= y < self.height:
                    i = y * self.width + x
                    frame[i*3:i*3+3] = color

        # Copy animated frame
        for anim_x in range(anim_frame.size[0]):
            for anim_y in range(anim_frame.size[1]):
                pix = anim_frame.getpixel((anim_x, anim_y))
                if pix[3] != 0: # Test for alpha
                    x = (self.width - anim_frame.size[0]) + anim_x
                    y = (self.height // 2 - anim_frame.size[1] // 2) + anim_y
                    i = ((y * self.width) + x) * 3
                    frame[i:i+3] = pix[:3]

        # Render and update the sparkles
        for sp in self.sparkles:
            for x in range(anim_sparkle[0].size[0]):
                for y in range(anim_sparkle[0].size[1]):
                    pix_x = sp.x + x - anim_sparkle[0].size[0] // 2
                    pix_y = sp.y + y - anim_sparkle[0].size[1] // 2
                    if 0 <= pix_x < self.width and 0 <= pix_y < self.height:
                        i = pix_y * self.width + pix_x
                        pix = anim_sparkle[sp.frame_index].getpixel((x, y))
                        if pix[3] != 0:
                            frame[i*3:i*3+3] = pix[:3]
            sp.x -= 3
            sp.frame_index += 1
        # Remove expired sparkles
        self.sparkles = list(filter(lambda sp: sp.frame_index < len(anim_sparkle), self.sparkles))

        sys.stdout.buffer.write(frame)
        self.sleep()

    def sleep(self):
        time.sleep(1 / 30)

    def plot_tail(self, width):
        pass # Virtual
