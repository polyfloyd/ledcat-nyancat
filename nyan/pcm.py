#!/usr/bin/env python3

from nyancat import Nyancat

INTERVAL = 1 / 20
WAVE_FACTOR = 3

class NyancatSignal(Nyancat):
    def __init__(self, w, h, signal):
        super().__init__(w, h)
        self.signal = signal
        self.samples_history = [[0] * int(INTERVAL * signal.sample_rate * WAVE_FACTOR)] * 6

    def plot_tail(self, width):
        # Calculate the wave
        samples = self.signal.get_signal(INTERVAL)
        samples_offset = 0
        smallest_diff = float('inf')
        # Find a part in the new sample window that resembles the previous one.
        for i in range(min(len(samples), len(self.samples_history[-1])) - width * WAVE_FACTOR):
            z = zip(self.samples_history[-1][0:width], samples[i:i + width * WAVE_FACTOR])
            diff = sum(map(lambda t: (t[0] - t[1]) ** 2, z))
            if diff < smallest_diff:
                samples_offset = i
                smallest_diff = diff
        assert samples_offset + width * WAVE_FACTOR < len(samples), 'w=%d < len=%d' % (samples_offset + width * WAVE_FACTOR, len(samples))
        self.samples_history.append(samples[samples_offset:samples_offset + width * WAVE_FACTOR])
        self.samples_history.pop(0)

        # Render the tail
        for x in range(width):
            amplitude = sum(map(lambda hist: hist[x * WAVE_FACTOR], self.samples_history)) / len(self.samples_history) * 3
            yield int((amplitude * .5 - .5) * self.height) + self.height
