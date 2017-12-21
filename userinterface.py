import matplotlib.pyplot as plt

import os
from button import *


class ui():
    def __init__(self, em):
        self.x0 = 1000
        self.y0 = 0
        self.x1 = 1200
        self.y1 = 800
        self.font = pygame.font.SysFont('Arial', 16)
        self.em = em
        self.buttons = []
        self.buttons.append(button(1010, 25, 190, 25, "Exit", self.exit, (255, 0, 0)))
        self.buttons.append(button(1010, 60, 190, 25, "Show hit plot", self.drawHitPlot))
        self.buttons.append(button(1010, 95, 190, 25, "Show mbot avg scores", self.drawMBotScorePlot))
        self.buttons.append(button(1010, 130, 190, 25, "Show lbot avg scores", self.drawLBotScorePlot))
        self.buttons.append(button(1010, 200, 190, 25, "Show eyes", self.drawEyes))
        self.buttons.append(button(1010, 235, 190, 25, "Spawn/delete player", self.spawnPlayer))
        self.buttons.append(button(1010, 340, 190, 25, "Save models and weights", self.em.saveModels))
        self.buttons.append(button(1010, 375, 190, 25, "Load models and weights", self.em.loadModels))
        self.eyes = False
        self.player = False


    def draw(self, w):
        if self.eyes:
            self.eyesDrawing(w)
        pygame.draw.rect(w, (200, 200, 200), (self.x0, self.y0, self.x1, self.y1))
        for button in self.buttons:
            button.draw(w)

        self.drawMBotsData(w, 5, 600, 190, 195)


    def update(self, event):
        if (event.type == pygame.MOUSEBUTTONDOWN):
            clickPos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.onClick(clickPos)

    def drawMBotsData(self, w, x0, y0, x1, y1):
        pygame.draw.rect(w, (255, 255, 255), (self.x0 + x0, self.y0 + y0, x1, y1))
        w.blit(self.font.render("MBots info", False, (0, 0, 0)), (self.x0 + x0 + 5, self.y0 + y0))
        w.blit(self.font.render("gen: " + str(self.em.mBotsGen), False, (0, 0, 0)),
               (self.x0 + x0 + 5, self.y0 + y0 + 20))
        w.blit(self.font.render("In pool: " + str(len(self.em.mBotsPool)), False, (0, 0, 0)),
               (self.x0 + x0 + 5, self.y0 + y0 + 40))

    def drawMBotScorePlot(self):
        yValues = self.em.scores[0]
        xValues = []
        for i in range(len(yValues)):
            xValues.append(i)
        plt.plot(xValues, yValues)
        plt.show()

    def drawLBotScorePlot(self):
        yValues = self.em.scores[1]
        xValues = []
        for i in range(len(yValues)):
            xValues.append(i)
        plt.plot(xValues, yValues)
        plt.xlabel('Bots', fontsize=12)
        plt.ylabel('Scores', fontsize=12)
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

    def drawEyes(self):
        self.eyes = not self.eyes

    def eyesDrawing(self, w):
        for botSet in self.em.bots:
            for bot in botSet:
                for eye in bot.eyes:
                    eye.draw(w)

    def spawnPlayer(self):
        self.player = not self.player
        self.spawningPlayer()


    def spawningPlayer(self):
        if self.player:
            self.em.createPlayer()
        else:
            self.em.bots[2] = []

    def exit(self):
        pygame.quit()
        os.sys.exit(0)
