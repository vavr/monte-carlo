import random
from tkinter import *

need_stop = False
triangle_size = 400
N = 10000
screen_size = 1200


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def main():
    rootWindow = Tk()
    rootWindow.title("triangle magic")
    rootWindow.geometry("1400x1400")

    panel = Frame(rootWindow)
    drawArea = Canvas(rootWindow, bg="white")

    def get_triangle_height():
        return triangle_size * 3 ** 0.5 / 2

    def get_startup_points():
        h = get_triangle_height()

        start_position_x1 = (screen_size - triangle_size) / 2
        start_position_y1 = (screen_size - triangle_size) / 2 + h - 100

        start_position_x2 = (start_position_x1 + triangle_size / 2)
        start_position_y2 = start_position_y1 - h

        start_position_x3 = start_position_x1 + triangle_size
        start_position_y3 = start_position_y1
        return Point(start_position_x1, start_position_y1), Point(start_position_x2, start_position_y2), Point(
            start_position_x3, start_position_y3)

    def startupPosition():
        global need_stop
        need_stop = False

        point1, point2, point3 = get_startup_points()

        drawArea.create_line(point1.x, point1.y, point2.x, point2.y, width=1)
        drawArea.create_line(point2.x, point2.y, point3.x, point3.y, width=1)
        drawArea.create_line(point1.x, point1.y, point3.x, point3.y, width=1)

    def drawPoint(x, y, color="red"):
        drawArea.create_oval(x, y, x + 1, y + 1, fill=color, outline=color, width=1)
        drawArea.update()

    def pick_next_vertex():

        points = get_startup_points()

        return random.choice(points)

    def startup_random_point():
        point1, point2, point3 = get_startup_points()

        x = random.uniform(point1.x, point3.x)
        print(x)

        if x >= point2.x:
            max_y = ((x - point2.x) * (point3.y - point2.y)) / ((point3.x - point2.x)) + point2.y
        else:
            max_y = ((x - point1.x) * (point2.y - point1.y)) / ((point2.x - point1.x)) + point1.y

        y = random.uniform(max_y, point1.y)
        drawPoint(x, y, "red")
        return Point(x, y)

    def next_point(vertex: Point, current_point: Point):

        if vertex.x > current_point.x:
            x = (vertex.x - current_point.x) / 2 + current_point.x
        else:
            x = (current_point.x - vertex.x) / 2 + vertex.x

        if vertex.y > current_point.y:
            y = (vertex.y - current_point.y) / 2 + current_point.y
        else:
            y = (current_point.y - vertex.y) / 2 + vertex.y

        result = Point(x, y)

        return result

    def start():
        clear()
        start_point = startup_random_point()
        current_point = start_point
        global need_stop, N
        for i in range(N):
            if need_stop:
                return

            vertex = pick_next_vertex()
            current_point = next_point(vertex, current_point)
            drawPoint(current_point.x, current_point.y, "red")

            iterValue['text'] = i

    def stop():
        global need_stop
        need_stop = True

    def clear():
        drawArea.delete("all")
        startupPosition()
        iterValue['text'] = 0

    def change_triangle_size(e):
        global triangle_size, need_stop
        triangle_size = int(e.widget.get())
        need_stop = True
        clear()

    def change_n(e):
        global N, need_stop
        N = int(e.widget.get())
        need_stop = True
        clear()

    startButton = Button(panel, text="Start", command=start)
    stopButton = Button(panel, text="Stop", command=stop)
    clearButton = Button(panel, text="Clear", command=clear)

    iterValueText = Label(panel, text="Кол-во итераций: ")
    iterValue = Label(panel, text="0")

    iterValue.pack(side=RIGHT)
    iterValueText.pack(side=RIGHT)

    panel.pack(fill=X, padx=4, pady=4)
    clearButton.pack(side=LEFT)
    startButton.pack(side=LEFT)
    stopButton.pack(side=LEFT)

    radiusValue = Entry(panel, width=5)
    radiusValue.bind("<Return>", change_triangle_size)
    radiusLabel = Label(panel, text="Размер треугольника: ")
    radiusLabel.pack(side=LEFT)
    radiusValue.pack(side=LEFT)

    nValue = Entry(panel, width=10)
    nValue.bind("<Return>", change_n)
    nLabel = Label(panel, text="К-во итераций: ")
    nLabel.pack(side=LEFT)
    nValue.pack(side=LEFT)

    drawArea.pack(fill=BOTH, side=TOP, expand=True, padx=4, pady=4)

    radiusValue.insert(0, triangle_size)
    nValue.insert(1000, N)

    startupPosition()

    rootWindow.mainloop()


if __name__ == "__main__":
    main()
