import matplotlib.pyplot as plt

from button import *


class ui():
    def __init__(self, em):
        self.x0 = 1000
        self.y0 = 0
        self.x1 = 1200
        self.y1 = 800
        self.buttons = []
        self.buttons.append(button(1010, 25, 190, 25, "Show hit plot", self.drawHitPlot))
        self.buttons.append(button(1010, 60, 190, 25, "Show avg scores", self.drawScorePlot))
        self.em = em

    def draw(self, w):
        pygame.draw.rect(w, (200, 200, 200), (self.x0, self.y0, self.x1, self.y1))
        for button in self.buttons:
            button.draw(w)

    def update(self, event):
        if (event.type == pygame.MOUSEBUTTONDOWN):
            clickPos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.onClick(clickPos)

    def drawScorePlot(self):
        yValues = self.em.scores[0]
        xValues = []
        for i in range(len(yValues)):
            xValues.append((i + 1) * 10)
        plt.plot(xValues, yValues)
        plt.show()

    def drawHitPlot(self):

        data = self.em.firedHitBulletHistory
        xValues = []
        yValues = []
        for datum in data:
            xValues.append(datum[0])
            yValues.append(datum[1] / 100)
        plt.plot(xValues, yValues)
        plt.show()
