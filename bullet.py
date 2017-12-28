from math import cos, sin

import pygame
from scipy.spatial import distance


class bullet:
    def __init__(self):
        self.dead = True
        self.speed = 400

    def init(self, bot):
        self.xSpeed = cos(bot.direction) * self.speed
        self.ySpeed = sin(bot.direction) * self.speed
        self.x = cos(bot.direction) * bot.radius + bot.x
        self.y = sin(bot.direction) * bot.radius + bot.y
        self.bot = bot
        self.dead = False

    def update(self, delta, bots):
        self.x += self.xSpeed * delta
        self.y += self.ySpeed * delta
        if (self.x <= 0 or self.x >= 1000 or self.y >= 800 or self.y <= 0):
            self.dead = True

        self.checkCollision(bots)

    def draw(self, w):
        pygame.draw.circle(w, (0, 0, 0), (int(self.x), int(self.y)), 3)

    def getPos(self):
        return self.x, self.y

    # might need optimizing
    def checkCollision(self, bots):
        for botSet in bots:
            for bot in botSet:
                if distance.euclidean((self.x, self.y), bot.getPos()) < bot.radius + 3:
                    if bot != self.bot:
                        bot.hp -= 1
                        bot.score -= 2
                        self.bot.em.bulletsHit += 1
                        self.bot.rewardForHit()
                        self.dead = True
