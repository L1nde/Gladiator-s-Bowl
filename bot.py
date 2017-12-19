import pygame


class bot:

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.direction = 0

    def update(self, delta):
        pass

    def draw(self, w):
        pygame.draw.circle(w, (0,0,255), (self.x, self.y), 13)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getDirection(self):
        return self.direction


class eye:

    def __init__(self, range, spread, direction, bot):
        self.range = range
        self.spread = spread
        self.direction = direction
        self.bot = bot

    def isInSight(self, targetX, targetY, relDir):
        dir = self.direction + relDir
