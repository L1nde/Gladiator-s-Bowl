from bullet import bullet
from mBot import *
from random import randint

class entityManager:

    def __init__(self):
        self.bulletPool = []
        self.deadBulletPool = []
        self.maxBotCount = 10
        self.bots = []

    def update(self, delta):
        self.updateBots(delta)
        self.updateBullets(delta)

    def draw(self, w):
        self.drawBots(w)
        self.drawBullets(w)

    def createBullet(self, shooter):
        if (len(self.deadBulletPool) != 0):
            b = self.deadBulletPool.pop()
        else:
            b = bullet()

        b.init(shooter)
        self.bulletPool.append(b)

    def createBots(self):
        while len(self.bots) <= self.maxBotCount:
            self.bots.append(mBot(randint(100,900), randint(100,700), self))

    def updateBullets(self, delta):
        for bullet in self.bulletPool:
            if (bullet.dead):
                self.deadBulletPool.append(bullet)
                self.bulletPool.remove(bullet)
                continue
            bullet.update(delta, self.bots)

    def updateBots(self, delta):
        self.createBots()
        for bot in self.bots:
            bot.update(delta)

    def drawBullets(self, w):
        for bullet in self.bulletPool:
            bullet.draw(w)

    def drawBots(self, w):
        for bot in self.bots:
            bot.draw(w)

    def killBot(self, bot):
        self.bots.remove(bot)