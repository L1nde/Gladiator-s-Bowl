from bullet import bullet
from lBot import *
from mBot import *
from player import *


class entityManager:
    def __init__(self):
        self.bulletPool = []
        self.deadBulletPool = []
        self.maxBotCount = 10  # per bot type
        self.bots = [[], [], []]
        self.mBotsPoolSize = 50
        self.mBotsGen = 0
        self.createMBots()
        self.createLBots()


        # Statistics
        self.bulletsFired = 0
        self.bulletsHit = 0
        self.firedHitBulletHistory = []
        self.scores = [[], []]

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
        self.deadMBots = []
        self.mBotsPool = []
        for i in range(self.mBotsPoolSize):
            self.mBotsPool.append(mBot(randint(100, 900), randint(100, 700), self))
        for i in range(self.maxBotCount):
            self.bots[0].append(self.mBotsPool.pop(randint(0, len(self.mBotsPool) - 1)))


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

    def killBot(self, bot):
        if (bot in self.bots[0]):
            self.killMBot(bot)
        if (bot in self.bots[1]):
            self.scores[1].append(bot.score)
            bot.reset()
        if (bot in self.bots[2]):
            self.createPlayer()
            self.bots[2].remove(bot)

    def killMBot(self, bot):
        self.bots[0].remove(bot)
        self.deadMBots.append(bot)
        self.bots[0].append(self.mBotsPool.pop(randint(0, len(self.mBotsPool) - 1)))

        if (len(self.mBotsPool) == 0):
            self.scores[0].append(self.getAvgMBotScores())
            self.mutateMBots()
            self.fillMBotsPool()
            self.mBotsGen += 1


    def mutateMBots(self):
        parentCount = 10  # must be divisible by 2
        childrenPerParentPair = 6
        sortedDeadMBots = sorted(self.deadMBots, key=lambda mBot: mBot.score, reverse=True)
        parents = sortedDeadMBots[:parentCount]
        otherBots = sortedDeadMBots[parentCount:]
        self.deadMBots = []
        for parent in parents:
            parent.reset()
            self.mBotsPool.append(parent)

        for i in range(0, parentCount, 2):
            parent1 = parents[i]
            parent2 = parents[i + 1]
            for j in range(childrenPerParentPair):
                if (len(otherBots) == 0):
                    return

                newBot = sortedDeadMBots.pop()
                newBot.reset()
                newBot.brain.mutate(parent1.brain.model, parent2.brain.model)
                self.mBotsPool.append(newBot)

    def fillMBotsPool(self):
        while (len(self.mBotsPool) < self.mBotsPoolSize):
            self.mBotsPool.append(mBot(randint(100, 900), randint(100, 700), self))

    def getTwoRandomHighScoreMBots(self):
        mbots = self.bots[0]
        sortedMBots = sorted(mbots, key=lambda mBot: mBot.score, reverse=True)
        return sortedMBots[0], sortedMBots[1]

    def getTwoRandomHighScoreLBots(self):
        lbots = self.bots[1]
        sortedLBots = sorted(lbots, key=lambda lBot: lBot.score, reverse=True)
        return sortedLBots[0], sortedLBots[1]

    def getAvgMBotScores(self):
        s = 0
        for bot in self.bots[0]:
            s += bot.score
        return s / len(self.bots[0])
