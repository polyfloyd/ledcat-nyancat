#!/usr/bin/env python3

import math
import os
import sys
import time
from audio import PCMSource
from nyancat import Nyancat
from pcm import NyancatSignal

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


if len(sys.argv) == 1 or sys.argv[1] == 'wave':
    cat = NyancatWave(DISP_WIDTH, DISP_HEIGHT)
elif sys.argv[1] == 'pcm':
    _split = list(sys.argv[3].split(':'))
    if len(_split) != 3:
        print('usage: %s pcm <pipe> <rate>:<bits>:<channels>' % sys.argv[0], file=sys.stderr)
        sys.exit(1)
    sample_rate = int(_split[0])
    sample_bits = int(_split[1])
    num_channels = int(_split[2])
    pipe = sys.stdin.buffer if sys.argv[2] == '-' else sys.argv[2]

    signal = PCMSource(pipe, sample_rate, sample_bits, num_channels)
    cat = NyancatSignal(DISP_WIDTH, DISP_HEIGHT, signal)

else:
    print('usage: %s <wave>|<pcm>' % sys.argv[0], file=sys.stderr)
    sys.exit(1)

while True:
    cat.render()
