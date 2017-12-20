import matplotlib.pyplot as plt

from button import *


class ui():
    def __init__(self, em):
        self.x0 = 1000
        self.y0 = 0
        self.x1 = 1200
        self.y1 = 800
        self.statButton = button(1010, 25, 80, 25, "Show stats", self.drawHitPlot)
        self.em = em

    def draw(self, w):
        pygame.draw.rect(w, (200, 200, 200), (self.x0, self.y0, self.x1, self.y1))
        self.statButton.draw(w)

    def update(self, event):
        if (event.type == pygame.MOUSEBUTTONDOWN):
            clickPos = pygame.mouse.get_pos()
            self.statButton.onClick(clickPos)

    def drawHitPlot(self):
        plt.figure(figsize=(12, 9), dpi=80)
        data = self.em.firedHitBulletHistory
        xValues = []
        yValues = []
        for datum in data:
            xValues.append(datum[0])
            yValues.append(datum[1] / 100)
        plt.plot(xValues, yValues)

        plt.show()
