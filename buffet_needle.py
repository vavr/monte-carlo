import math
import random
from tkinter import *

import GraphPlot as gp

need_stop = False
need_to_draw = True
R = 50
L = 1
N = 1000000


def main():
    rootWindow = Tk()
    rootWindow.title("PI via monte carlo method")
    rootWindow.geometry("800x800")

    panel = Frame(rootWindow)
    drawArea = Canvas(rootWindow, bg="white")
    graph = gp.GraphPlot()

    def startupPosition():
        global need_stop
        need_stop = False

        for i in range(800 // R):
            drawArea.create_line(i * R, 0, i * R, 800, width=1)

    def is_line_crossed(x1, x2):
        x_left = (x1 // R) * R
        # nearest right vertical line
        x_right = x_left + R
        # condition of crossing any line
        return (x2 < x_left) or (x2 > x_right)

    def drawNeedle(x1, y1, x2, y2):
        if need_to_draw:
            if is_line_crossed(x1, x2):
                color = "green"
            else:
                color = "red"

            drawArea.create_line(x1, y1, x2, y2, fill=color, width=2)
            drawArea.update()

    def start():
        clear()
        global need_stop, N
        need_result = 0

        for i in range(N):
            if need_stop:
                return

            # random x coordinate the end of needle
            x1 = random.uniform(R, 800 - R)
            y1 = random.uniform(R, 800 - R)
            # random x coordinate the other end of needle
            rand_alpha = random.uniform(0, 360)
            x2 = x1 + L * math.cos(math.radians(rand_alpha))
            y2 = y1 + L * math.sin(math.radians(rand_alpha))

            if is_line_crossed(x1, x2):
                need_result += 1
            drawNeedle(x1, y1, x2, y2)
            if need_result != 0:
                pi_value = (2 * (i + 1) * L) / (need_result * R)
            else:
                pi_value = 0
            if i % 1000 == 0:
                if need_result != 0:
                    piValue['text'] = f"{pi_value:.{8}f}"
                drawArea.update()
                graph.draw_value(i, pi_value)

            iterValue['text'] = i

    def stop():
        global need_stop
        need_stop = True

    def clear():
        drawArea.delete("all")
        graph.clear()
        startupPosition()
        iterValue['text'] = 0
        piValue['text'] = 0

    def change_radius(e):
        global R, need_stop
        R = int(e.widget.get())
        need_stop = True
        clear()

    def change_line_size(e):
        global L, need_stop
        L = int(e.widget.get())
        need_stop = True
        clear()

    def change_n(e):
        global N, need_stop
        N = int(e.widget.get())
        need_stop = True
        clear()

    def switch_draw():
        global need_to_draw
        if need_to_draw:
            need_to_draw = False
        else:
            need_to_draw = True

    startButton = Button(panel, text="Start", command=start)
    stopButton = Button(panel, text="Stop", command=stop)
    clearButton = Button(panel, text="Clear", command=clear)
    drawButton = Button(panel, text="Switch drawing", command=switch_draw)

    piValueText = Label(panel, text="Текущее приближение PI: ")
    piValue = Label(panel, text="0")

    iterValueText = Label(panel, text="Кол-во итераций: ")
    iterValue = Label(panel, text="0")

    piValue.pack(side=RIGHT)
    piValueText.pack(side=RIGHT)

    iterValue.pack(side=RIGHT)
    iterValueText.pack(side=RIGHT)

    panel.pack(fill=X, padx=4, pady=4)
    clearButton.pack(side=LEFT)
    startButton.pack(side=LEFT)
    stopButton.pack(side=LEFT)
    drawButton.pack(side=LEFT)

    radiusValue = Entry(panel, width=5)
    radiusValue.bind("<Return>", change_radius)
    radiusLabel = Label(panel, text="Радиус: ")
    radiusLabel.pack(side=LEFT)
    radiusValue.pack(side=LEFT)

    lSizeValue = Entry(panel, width=5)
    lSizeValue.bind("<Return>", change_line_size)
    lSizeLabel = Label(panel, text="Длина иглы: ")
    lSizeLabel.pack(side=LEFT)
    lSizeValue.pack(side=LEFT)

    nValue = Entry(panel, width=10)
    nValue.bind("<Return>", change_n)
    nLabel = Label(panel, text="К-во итераций: ")
    nLabel.pack(side=LEFT)
    nValue.pack(side=LEFT)

    drawArea.pack(fill=BOTH, side=TOP, expand=True, padx=4, pady=4)

    radiusValue.insert(0, str(R))
    lSizeValue.insert(0, str(L))
    nValue.insert(1000, str(N))

    startupPosition()

    graph.plt.show()
    rootWindow.mainloop()


if __name__ == "__main__":
    main()
