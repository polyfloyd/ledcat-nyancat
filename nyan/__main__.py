#!/usr/bin/env python3

import math
import os
import time
from nyancat import Nyancat

_geometry = os.getenv('LEDCAT_GEOMETRY', '150x16').split('x')
DISP_WIDTH  = int(_geometry[0])
DISP_HEIGHT = int(_geometry[1])

class NyancatWave(Nyancat):
    def __init__(self, w, h):
        super().__init__(w, h)

    def plot_tail(self, width):
        t = time.time()
        for x in range(width):
            yield (DISP_HEIGHT // 2) + int(math.sin(x / 6 + t * math.pi) * 4 * math.sin(t * 8))


cat = NyancatWave(DISP_WIDTH, DISP_HEIGHT)
while True:
    cat.render()
