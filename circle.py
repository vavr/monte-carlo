from tkinter import *
from typing import List, Any

from R2Graph import *


def main():
    rootWindow = Tk()
    rootWindow.title("Triangle")
    rootWindow.geometry("800x600")

    points = []

    panel = Frame(rootWindow)
    drawArea = Canvas(rootWindow, bg="white")

    def clear():
        drawArea.delete("all")
        points.clear()

    clearButton = Button(panel, text="Clear", command=clear)

    def drawTriangle():
        if len(points) >= 3:
            # drawArea.delete("all")
            drawArea.create_line(
                points[0].x, points[0].y,
                points[1].x, points[1].y,
                points[2].x, points[2].y,
                points[0].x, points[0].y,
                fill="blue", width=2
            )
            (center, radius, bisectrixes) = inCircle(points)
            # Draw an inscribed circle
            drawArea.create_oval(
                center.x - radius, center.y - radius,
                center.x + radius, center.y + radius,
                fill="", outline="red", width=2
            )

            # Draw bisectrixes
            for i in range(3):
                drawArea.create_line(
                    points[i].x, points[i].y,
                    bisectrixes[i].x, bisectrixes[i].y,
                    fill="darkGreen", width=1
                )
            # Draw the center of circle
            drawArea.create_oval(
                center.x - 4, center.y - 4,
                center.x + 4, center.y + 4,
                fill="red", outline="red"
            )

    drawButton = Button(panel, text="Draw", command=drawTriangle)

    panel.pack(fill=X, padx=4, pady=4)
    clearButton.pack(side=LEFT)
    drawButton.pack(side=LEFT)
    drawArea.pack(fill=BOTH, side=TOP, expand=True, padx=4, pady=4)

    def click(e):
        if len(points) >= 3:
            clear()
        points.append(R2Point(e.x, e.y))
        drawArea.create_line(
            e.x - 8, e.y, e.x + 8, e.y, fill="red", width=3
        )
        drawArea.create_line(
            e.x, e.y - 8, e.x, e.y + 8, fill="red", width=3
        )

    drawArea.bind("<Button-1>", click)

    rootWindow.mainloop()


# Compute bisectrixes of triangle and
# a center & radius of inscribed circle
def inCircle(vertices):
    bisectrixes = []
    for i in range(3):
        iPrev = i - 1
        if iPrev < 0:
            iPrep = 2
        iNext = i + 1
        if iNext >= 3:
            iNext = 0
        vPrev = (vertices[iPrev] - vertices[i]).normalized()
        vNext = (vertices[iNext] - vertices[i]).normalized()
        b = vPrev + vNext  # The direction vector of i-th bisectrix

        # The point of bisectrix is calculated as intersection of 2 lines,
        # where a line is defined by a point and a direction vector
        (_, bisectrix) = intersectLines(
            vertices[i], b,  # line of bisectrix
            vertices[iPrev],  # side of triangle
            vertices[iNext] - vertices[iPrev]
        )
        bisectrixes.append(bisectrix)

    # A circle center is an intersection of 2 bisectrixes
    (_, center) = intersectLines(
        vertices[0], bisectrixes[0] - vertices[0],
        vertices[1], bisectrixes[1] - vertices[1]
    )
    # The circle radius equals to the distance from the center
    # to the first side of triangle
    radius = center.distanceToLine(
        vertices[0], vertices[1] - vertices[0]
    )
    return (center, radius, bisectrixes)


if __name__ == "__main__":
    main()
