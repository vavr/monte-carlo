from tkinter import *

import random

need_stop = False
R = 300
x_center = 100 + R
y_center = 100 + R
N = 1000000

def main():
    rootWindow = Tk()
    rootWindow.title("PI via monte carlo method")
    rootWindow.geometry("800x800")

    panel = Frame(rootWindow)
    drawArea = Canvas(rootWindow, bg="white")

    def set_center():
        global x_center, y_center
        x_center = 100 + R
        y_center = 100 + R

    def startupPosition():
        global need_stop
        need_stop = False

        set_center()
        drawArea.create_rectangle(100, 100, R * 2 + 100, R * 2 + 100, fill="", outline="black", width=2)
        drawArea.create_oval(100, 100, R * 2 + 100, R * 2 + 100, fill="", outline="black", width=2)

    def in_circle(x, y):
        return (x - x_center) ** 2 + (y - y_center) ** 2 <= R ** 2

    def drawPoint(x, y):

        if in_circle(x, y):
            color = "green"
        else:
            color = "red"

        drawArea.create_oval(x-1, y-1, x+1, y+1, fill=color, outline=color)
        drawArea.update()

    def start():
        clear()
        global need_stop, N
        need_result = 0
        for i in range(N):
            if need_stop:
                return
            x = random.uniform(100, R * 2 + 100)
            y = random.uniform(100, R * 2 + 100)
            if in_circle(x, y):
                need_result += 1
            drawPoint(x, y)
            if i % 1000 == 0:
                piValue['text'] = (need_result / (i + 1)) * 4
            iterValue['text'] = i

    def stop():
        global need_stop
        need_stop = True

    def clear():
        drawArea.delete("all")
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

    startButton = Button(panel, text="Start", command=start)
    stopButton = Button(panel, text="Stop", command=stop)
    clearButton = Button(panel, text="Clear", command=clear)

    piValueText = Label(panel, text="?????????????? ?????????????????????? PI: ")
    piValue = Label(panel, text="0")

    iterValueText = Label(panel, text="??????-???? ????????????????: ")
    iterValue = Label(panel, text="0")

    piValue.pack(side=RIGHT)
    piValueText.pack(side=RIGHT)

    iterValue.pack(side=RIGHT)
    iterValueText.pack(side=RIGHT)

    panel.pack(fill=X, padx=4, pady=4)
    clearButton.pack(side=LEFT)
    startButton.pack(side=LEFT)
    stopButton.pack(side=LEFT)

    radiusValue = Entry(panel, width=5)
    radiusValue.bind("<Return>", change_radius)
    radiusLabel = Label(panel, text="????????????: ")
    radiusLabel.pack(side=LEFT)
    radiusValue.pack(side=LEFT)

    nValue = Entry(panel, width=10)
    nValue.bind("<Return>", change_n)
    nLabel = Label(panel, text="??-???? ????????????????: ")
    nLabel.pack(side=LEFT)
    nValue.pack(side=LEFT)

    drawArea.pack(fill=BOTH, side=TOP, expand=True, padx=4, pady=4)

    radiusValue.insert(0, R)
    nValue.insert(1000, N)

    startupPosition()

    rootWindow.mainloop()

if __name__ == "__main__":
    main()
