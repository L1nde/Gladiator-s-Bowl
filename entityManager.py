from bullet import bullet
from mBot import *


class entityManager:
    def __init__(self):
        self.bulletPool = []
        self.deadBulletPool = []
        self.maxBotCount = 10
        self.bots = [[], []]
        self.createMBots()
        self.bulletsFired = 0
        self.bulletsHit = 0
        self.firedHitBulletHistory = []

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
        self.bulletsFired += 1
        if (self.bulletsFired % 100 == 0):
            self.firedHitBulletHistory.append([self.bulletsFired, self.bulletsHit])
            self.bulletsHit = 0


    def createMBots(self):
        while len(self.bots[0]) <= self.maxBotCount:
            self.bots[0].append(mBot(randint(100, 900), randint(100, 700), self))

    def updateBullets(self, delta):
        for bullet in self.bulletPool:
            if (bullet.dead):
                self.deadBulletPool.append(bullet)
                self.bulletPool.remove(bullet)
                continue
            bullet.update(delta, self.bots)

    def updateBots(self, delta):
        for i in self.bots:
            for bot in i:
                bot.update(delta)

    def drawBullets(self, w):
        for bullet in self.bulletPool:
            bullet.draw(w)

    def drawBots(self, w):
        for i in self.bots:
            for bot in i:
                bot.draw(w)

    def createNewMBot(self, bot):
        bot.reset()

    def killBot(self, bot):
        if (bot in self.bots[0]):
            self.createNewMBot(bot)

    def getTwoRandomHighScoreMBots(self):
        mbots = self.bots[0]
        sortedMBots = sorted(mbots, key=lambda mBot: mBot.score, reverse=True)
        return sortedMBots[0], sortedMBots[1]
