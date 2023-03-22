import math
import random
from tkinter import *

need_stop = False
need_to_draw = True
R = 50
N = 1000000


class GraphResults:
    def __init__(self, graph_iter_width):

        rootWindow = Tk()
        rootWindow.title("PI graph results via monte carlo method")

        # getting screen width and height of display
        width = rootWindow.winfo_screenwidth() - 50
        height = rootWindow.winfo_screenheight() - 50
        # setting tkinter window size
        rootWindow.geometry("%dx%d" % (width, height))

        frame = Frame(rootWindow, width=width, height=height)
        frame.pack(expand=True, fill=BOTH)

        canvasGraph = Canvas(frame, width=width, height=height, bg="white", scrollregion=(0, 0, width * 2, height))

        xbar = Scrollbar(frame, orient=HORIZONTAL)
        xbar.pack(side=BOTTOM, fill=X)
        xbar.config(command=canvasGraph.xview)

        ybar = Scrollbar(frame, orient=VERTICAL)
        ybar.pack(side=RIGHT, fill=Y)
        ybar.config(command=canvasGraph.yview)

        self.window = rootWindow
        self.canvas = canvasGraph
        self.graph_iter_width = graph_iter_width

        self.width = width
        self.height = height

        self.canvas.config(width=width, height=height)
        self.canvas.config(xscrollcommand=xbar.set, yscrollcommand=ybar.set)

        self.bottom_pad = 100
        self.top_pad = 10
        self.left_pad = 30

    def drawStartPosition(self):

        # вычитаем отсуп снизу и сверху
        height = self.height - self.top_pad - self.bottom_pad

        # ось y
        self.canvas.create_line(self.left_pad, self.height - self.top_pad, self.left_pad, self.top_pad, width=2,
                                arrow=LAST)
        # ось x
        self.canvas.create_line(0, self.height - self.bottom_pad, self.width - self.top_pad,
                                self.height - self.bottom_pad, width=2, arrow=LAST)
        self.canvas.create_line(self.width - self.top_pad, self.height - self.bottom_pad, self.width * 2 - self.top_pad,
                                self.height - self.bottom_pad, width=2, arrow=LAST)

        pi_line_y = (height / 2) + self.top_pad
        # линия рисуюшая PI
        self.canvas.create_line(0, pi_line_y, self.width * 2, pi_line_y, width=2, fill='red')
        self.canvas.create_text(self.left_pad + 30, pi_line_y - self.top_pad, text=str(math.pi)[0:8], fill="purple",
                                font=("Helvectica", "10"))

        step = height / (2 * math.pi)
        # рисуем по y значения
        for i in range(7):
            need_y = self.height - self.bottom_pad - i * step
            self.canvas.create_line(self.left_pad - 3, need_y, self.left_pad + 3, need_y, width=2, fill='black')
            self.canvas.create_text(self.left_pad + 8, need_y, text=str(i), fill="black", font=("Helvectica", "10"))

        self.canvas.pack()

    def drawValueOnGraph(self, iteration, pi_value):

        need_pow = len(str(iteration)) - 1

        need_to_draw = False
        if iteration % (10 ** need_pow) == 0:
            need_to_draw = True

        mod_iteration = iteration // (10 ** need_pow)
        if need_pow > 1:
            iteration_text = str(mod_iteration) + '*10^' + str(need_pow)
        else:
            iteration_text = str(iteration)

        if need_to_draw:
            already_draw = (10 * need_pow + (iteration // 10 ** need_pow) - need_pow)

            # 60 - так как отсуп снизу 50 + 10 сверху
            height = self.height - self.top_pad - self.bottom_pad

            need_y = self.height - self.bottom_pad - (height / (math.pi * 2)) * pi_value
            need_x = self.left_pad + already_draw * self.graph_iter_width

            # print(pi_value, need_y, iteration_text, iteration, already_draw)

            self.canvas.create_oval(need_x, need_y, need_x + 3, need_y + 3, fill='black')
            # if already_draw % 3 == 0:
            self.canvas.create_text(need_x, self.height - self.bottom_pad + 10, text=str(iteration_text),
                                    fill="purple",
                                    font=("Helvectica", "10"))
            self.canvas.update()

    def clear(self):
        self.canvas.delete("all")


def main():
    rootWindow = Tk()
    rootWindow.title("PI via monte carlo method")
    rootWindow.geometry("800x800")

    panel = Frame(rootWindow)
    drawArea = Canvas(rootWindow, bg="white")
    graphResults = GraphResults(50)

    def startupPosition():
        global need_stop
        need_stop = False

        for i in range(800 // R):
            drawArea.create_line(i * R, 0, i * R, 800, width=1)
        graphResults.drawStartPosition()

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
            x2 = x1 + R * math.cos(math.radians(rand_alpha))
            y2 = y1 + R * math.sin(math.radians(rand_alpha))

            if is_line_crossed(x1, x2):
                need_result += 1
            drawNeedle(x1, y1, x2, y2)
            if need_result != 0:
                pi_value = (2 * (i + 1)) / need_result
            else:
                pi_value = 0
            if i % 1000 == 0:
                if need_result != 0:
                    piValue['text'] = pi_value
                drawArea.update()
            graphResults.drawValueOnGraph(i, pi_value)

            iterValue['text'] = i

    def stop():
        global need_stop
        need_stop = True

    def clear():
        drawArea.delete("all")
        graphResults.clear()
        startupPosition()
        iterValue['text'] = 0
        piValue['text'] = 0

    def change_radius(e):
        global R, need_stop
        R = int(e.widget.get())
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

    nValue = Entry(panel, width=10)
    nValue.bind("<Return>", change_n)
    nLabel = Label(panel, text="К-во итераций: ")
    nLabel.pack(side=LEFT)
    nValue.pack(side=LEFT)

    drawArea.pack(fill=BOTH, side=TOP, expand=True, padx=4, pady=4)

    radiusValue.insert(0, R)
    nValue.insert(1000, N)

    startupPosition()

    rootWindow.mainloop()
    graphResults.window.mainloop()


if __name__ == "__main__":
    main()
