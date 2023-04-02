import math

import matplotlib.pyplot as plt


class GraphPlot:
    def __init__(self):
        self.plt = plt
        self.figure = self.plt.figure()

        self.pi_ax = self.figure.add_subplot(211)

        self.delta_ax = self.figure.add_subplot(212)

        self.startup_position()

    def startup_position(self):
        self.pi_ax.axhline(y=math.pi, color='r', linestyle='-')
        self.delta_ax.axhline(y=0, color='r', linestyle='-')
        self.figure.canvas.draw()

    def draw_value(self, i, pi_value):
        if i % 1000 == 0:
            self.pi_ax.plot(i, pi_value, 'bo', ms=3)
            self.pi_ax.set_yscale('log')

            self.delta_ax.plot(i, abs(pi_value - math.pi), 'bo', ms=3)
            self.delta_ax.set_yscale('log')
            if i % 10000 == 0:
                self.figure.canvas.draw()
                # self.figure.canvas.flush_events()

    def clear(self):
        self.pi_ax.clear()
        self.delta_ax.clear()
        self.startup_position()
