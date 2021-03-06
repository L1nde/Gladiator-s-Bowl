from math import radians, cos, sin, exp
from random import randint

import pygame
from theano.gradient import np


class bot:
    def __init__(self, x, y, entityManager):
        self.x = x
        self.y = y
        self.hp = 3
        self.direction = 0  # radians
        self.cooldown = 3  # seconds
        self.speed = 0
        self.currentCooldown = 0
        self.score = 0
        self.radius = 13
        self.em = entityManager

    def reset(self):
        self.x = randint(100, 900)
        self.y = randint(100, 700)
        self.hp = 3
        self.direction = radians(randint(-180, 180))
        self.speed = 0
        self.currentCooldown = 0
        self.score = 0

    def update(self, delta):
        if self.hp <= 0:
            self.em.killBot(self)
            return

    def draw(self, w):
        pygame.draw.circle(w, (0, 0, 255), (self.x, self.y), self.radius)

    def reload(self, delta):
        if (self.currentCooldown > 0):
            self.currentCooldown -= delta

    def shoot(self):
        if (self.currentCooldown <= 0):
            self.em.createBullet(self)
            self.currentCooldown = self.cooldown
            return True
        return False

    def getPos(self):
        return (self.x, self.y)

    def getDirection(self):
        return self.direction

    def rewardForHit(self):
        self.score += 10


class eye:
    def __init__(self, range, spread, direction, bot):
        self.range = range
        self.spread = spread
        self.direction = direction
        self.bot = bot

    # Focuses on bullets
    def getVisionB(self, bots, bullets):
        if (self.canSeeEnemyBullet(bullets)):
            return -1
        return self.canSeeEnemy(bots)

    # Focuses on enemies
    def getVisionE(self, bots, bullets):
        if (self.canSeeEnemy(bots)):
            return 1
        return self.canSeeEnemyBullet(bullets)

    # returns if eye can see given point
    def canSeeEnemy(self, bots):
        for botSet in bots:
            for bot in botSet:
                if (self.bot != bot):
                    if (self.isInSight(bot.getPos())):
                        return 1
        return 0

    def canSeeEnemyBullet(self, bullets):
        for b in bullets:
            if (b.bot != self.bot):
                if (self.isInSight(b.getPos())):
                    return -1
        return 0

    def isInSight(self, targetPos):
        if self.isInRange(targetPos):
            dir = self.bot.direction + self.direction
            edgeVector1 = (sin(dir + self.spread / 2), -cos(dir + self.spread / 2))
            edgeVector2 = (sin(dir - self.spread / 2), -cos(dir - self.spread / 2))
            targetVector = np.subtract(targetPos, self.bot.getPos())
            if np.dot(targetVector, edgeVector2) < 0 and np.dot(targetVector, edgeVector1) > 0:
                return True
        return False

    def isInRange(self, targetPos):
        if self.range ** 2 > (self.bot.x - targetPos[0]) ** 2 + (self.bot.y - targetPos[1]) ** 2:
            return True
        return False

    def draw(self, w):
        dir = self.bot.direction + self.direction
        col = (randint(0, 200), randint(0, 200), randint(0, 200))
        pygame.draw.line(w, col, (cos(dir + self.spread / 2) * self.range + self.bot.x,
                                        sin(dir + self.spread / 2) * self.range + self.bot.y), self.bot.getPos())
        pygame.draw.line(w, col, (cos(dir - self.spread / 2) * self.range + self.bot.x,
                                  sin(dir - self.spread / 2) * self.range + self.bot.y), self.bot.getPos())


# returns to closest bot/bullet pos
class radar:
    def __init__(self, bot):
        self.bot = bot

    def getBulletLocs(self, bullet):
        p = []
        for b in bullet:
            p.append(b.getPos())
        return np.asarray(p)

    def getBotLocs(self, bots):
        p = []
        for b in bots:
            p.append(b.getPos())
        return np.asarray(p)

    def getClosestBullet(self, bullets):
        return self.findClosest(self.getBulletLocs(bullets))

    def getClosestBot(self, bots):
        return self.findClosest(self.getBotLocs(bots))

    def findClosest(self, targets):
        if (len(targets) == 0):
            return None
        dist_2 = np.sum((targets - np.asarray(self.bot.getPos())) ** 2, axis=1)
        return targets[np.argmin(dist_2)]

def sigmoid(x):
    return 1 / (1 + exp(-x))