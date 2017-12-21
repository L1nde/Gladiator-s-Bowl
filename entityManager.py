from bullet import bullet
from mBot import *
from lBot import *
from player import *
from random import randint

class entityManager:
    def __init__(self):
        self.bulletPool = []
        self.deadBulletPool = []
        self.maxBotCount = 10
        self.bots = [[], [], []]
        self.createMBots()
        self.createLBots()
        # self.createPlayer()

        # Statistics
        self.bulletsFired = 0
        self.bulletsHit = 0
        self.firedHitBulletHistory = []

        self.scoreRecordTime = 10
        self.timeTillRecordTime = self.scoreRecordTime
        self.scores = [[], []]

    def update(self, delta):
        self.updateBots(delta)
        self.updateBullets(delta)
        self.dealWithScores(delta)


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

    def createLBots(self):
        while len(self.bots[1]) <= self.maxBotCount:
            self.bots[1].append(lBot(randint(100,900), randint(100,700), self))

    def createPlayer(self):
        self.bots[2].append(player(randint(100,900), randint(100,700), self))

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
        if (bot in self.bots[1]):
            bot.reset()
        if (bot in self.bots[2]):
            self.createPlayer()
            self.bots[2].remove(bot)

    def getTwoRandomHighScoreMBots(self):
        mbots = self.bots[0]
        sortedMBots = sorted(mbots, key=lambda mBot: mBot.score, reverse=True)
        return sortedMBots[0], sortedMBots[1]

    def getTwoRandomHighScoreLBots(self):
        lbots = self.bots[1]
        sortedLBots = sorted(lbots, key=lambda lBot: lBot.score, reverse=True)
        return sortedLBots[0], sortedLBots[1]

    def dealWithScores(self, delta):
        self.timeTillRecordTime -= delta
        if (self.timeTillRecordTime < 0):
            self.scores[0].append(self.getAvgMBotScores())
            self.timeTillRecordTime = self.scoreRecordTime

    def getAvgMBotScores(self):
        s = 0
        for bot in self.bots[0]:
            s += bot.score
        return s / len(self.bots[0])
