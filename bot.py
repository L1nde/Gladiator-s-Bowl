import pygame
from math import pi, atan2, radians, cos, sin

from scipy.spatial import distance
from theano.gradient import np


class bot:
    def __init__(self, x, y, entityManager):
        self.x = x
        self.y = y
        self.hp = 1
        self.direction = 0  # radians
        self.cooldown = 2 # seconds
        self.speed = 50
        self.currentCooldown = 0
        self.score = 0
        self.radius = 13
        self.em = entityManager


    def update(self, delta):
        if self.hp <= 0:
            self.em.killBot(self)

    def draw(self, w):
        pygame.draw.circle(w, (0, 0, 255), (self.x, self.y), self.radius)

    def reload(self, delta):
        if (self.currentCooldown > 0):
            self.currentCooldown -= delta

    def shoot(self):
        if (self.currentCooldown <= 0):
            self.em.createBullet(self)
            self.currentCooldown = self.cooldown

    def getPos(self):
        return (self.x, self.y)

    def getDirection(self):
        return self.direction

class eye:
    def __init__(self, range, spread, direction, bot):
        self.range = range
        self.spread = spread
        self.direction = direction
        self.bot = bot

    # returns if eye can see given point
    def canSeeEnemy(self, bots):
        for botSet in bots:
            for bot in botSet:
                if (self.bot != bot):
                    if (self.isInSight(bot.getPos())):
                        return 1
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
        if self.range > distance.euclidean(self.bot.getPos(), targetPos):
            return True
        return False

    def draw(self, w):
        dir = self.bot.direction + self.direction
        pygame.draw.line(w, (0, 0, 0), (cos(dir + self.spread / 2) * self.range + self.bot.x,
                                        sin(dir + self.spread / 2) * self.range + self.bot.y), self.bot.getPos())
        pygame.draw.line(w, (0, 0, 0), (cos(dir - self.spread / 2) * self.range + self.bot.x,
                                        sin(dir - self.spread / 2) * self.range + self.bot.y), self.bot.getPos())

