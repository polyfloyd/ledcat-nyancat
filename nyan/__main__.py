#!/usr/bin/env python3

from collections import namedtuple
import math
import os
import os.path as path
import random
import sys
import time
from PIL import Image # Requires the Pillow library

_geometry = os.getenv('LEDCAT_GEOMETRY', '150x16').split('x')
DISP_WIDTH  = int(_geometry[0])
DISP_HEIGHT = int(_geometry[1])


tail_colors = [
    (0xff, 0x00, 0x00),
    (0xff, 0x99, 0x00),
    (0xff, 0xff, 0x00),
    (0x00, 0xff, 0x00),
    (0x00, 0x99, 0xff),
    (0x66, 0x33, 0xff),
]

def read_image(filename):
    img = Image.open(filename)
    return img

anim_cat = []
for i in range(0, 6):
    frame = read_image('%s/cat/%d.png' % (path.dirname(__file__), i))
    assert (32, 16) == frame.size
    anim_cat.append(frame)
anim_sparkle = []
for i in range(0, 5):
    frame = read_image('%s/sparkle/%d.png' % (path.dirname(__file__), i))
    anim_sparkle.append(frame)

class Sparkle(object):
    def __init__(self):
        half_h = anim_sparkle[0].size[1] // 2
        self.x = random.randint(0, DISP_WIDTH)
        self.y = random.randint(half_h, DISP_HEIGHT - half_h)
        self.frame_index = 0

sparkles = []
while True:
    for anim_frame in anim_cat:
        if len(sparkles) < 32:
            sparkles.append(Sparkle())

        frame = bytearray(DISP_WIDTH * DISP_HEIGHT * 3)

        # Render the tail
        for x in range(DISP_WIDTH):
            for y in range(DISP_HEIGHT):
                i = y * DISP_WIDTH + x
                t = time.time()
                col_y = y - (DISP_HEIGHT // 2 - len(tail_colors) // 2) + int(math.sin(x / 6 + t * math.pi) * 4 * math.sin(t * 8))
                if x < (DISP_WIDTH - 10) and 0 <= col_y < len(tail_colors):
                    color = tail_colors[col_y]
                else:
                    color = (0x0f, 0x4d, 0x8f)
                frame[i*3:i*3+3] = color

        # Copy animated frame
        for anim_x in range(anim_frame.size[0]):
            for anim_y in range(anim_frame.size[1]):
                pix = anim_frame.getpixel((anim_x, anim_y))
                if pix[3] != 0: # Test for alpha
                    x = (DISP_WIDTH - anim_frame.size[0]) + anim_x
                    y = (DISP_HEIGHT // 2 - anim_frame.size[1] // 2) + anim_y
                    i = ((y * DISP_WIDTH) + x) * 3
                    frame[i:i+3] = pix[:3]

        # Render and update the sparkles
        for sp in sparkles:
            for x in range(anim_sparkle[0].size[0]):
                for y in range(anim_sparkle[0].size[1]):
                    pix_x = sp.x + x - anim_sparkle[0].size[0] // 2
                    pix_y = sp.y + y - anim_sparkle[0].size[1] // 2
                    if 0 <= pix_x < DISP_WIDTH and 0 <= pix_y < DISP_HEIGHT:
                        i = pix_y * DISP_WIDTH + pix_x
                        pix = anim_sparkle[sp.frame_index].getpixel((x, y))
                        if pix[3] != 0:
                            frame[i*3:i*3+3] = pix[:3]
            sp.x -= 3
            sp.frame_index += 1
        # Remove expired sparkles
        sparkles = list(filter(lambda sp: sp.frame_index < len(anim_sparkle), sparkles))

        sys.stdout.buffer.write(frame)
        time.sleep(1 / 30)
