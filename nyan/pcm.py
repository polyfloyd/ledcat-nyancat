#!/usr/bin/env python3

import math
import sys
from nyancat import Nyancat

INTERVAL = 1 / 20
FACTOR = 3
AMPLIFICATION = 3
HISTORY_SIZE = 4

class NyancatSignal(Nyancat):
    def __init__(self, w, h, signal):
        super().__init__(w, h)
        self.signal = signal
        self.samples_history = [[0] * int(INTERVAL * signal.sample_rate * FACTOR)] * HISTORY_SIZE

    def plot_tail(self, width):
        # Calculate the wave
        samples = self.signal.get_signal(INTERVAL)
        samples_offset = 0
        smallest_diff = float('inf')
        # Find a part in the new sample window that resembles the previous one,
        # this makes the wave seem stand still.
        for i in range(min(len(samples), len(self.samples_history[-1])) - width * FACTOR):
            z = zip(self.samples_history[-1][0:width], samples[i:i + width * FACTOR])
            diff = sum(map(lambda t: (t[0] - t[1]) ** 2, z))
            if diff < smallest_diff:
                samples_offset = i
                smallest_diff = diff
        assert samples_offset + width * FACTOR < len(samples), 'w=%d < len=%d' % (samples_offset + width * FACTOR, len(samples))

        selected_window = samples[samples_offset:samples_offset + width * FACTOR]
        # Make sure the mean of the selected window is equal to 0, this
        # lowers vertical stuttering.
        win_avg = sum(selected_window) / len(selected_window)
        stabilized_window = [sample + win_avg for sample in selected_window]
        # Append to the history.
        self.samples_history.append(stabilized_window)
        self.samples_history.pop(0)

        for x in range(width):
            amplitude = sum([samples[x * FACTOR] for samples in self.samples_history]) / len(self.samples_history) * AMPLIFICATION
            yield int((amplitude * .5 + .5) * self.height)

    def sleep(self):
        pass # Handled by a blocking read from the audio source
