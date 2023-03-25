from tkinter import *

import math

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