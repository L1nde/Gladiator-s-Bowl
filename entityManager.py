from bullet import bullet
from mBot import *

class entityManager:

    def __init__(self):
        self.bulletPool = []
        self.deadBulletPool = []
        self.bot = mBot(400, 400, self)

    def update(self, delta):
        self.bot.update(delta)
        self.updateBullets(delta)

    def draw(self, w):
        self.bot.draw(w)
        self.drawBullets(w)

    def createBullet(self, shooter):
        if (len(self.deadBulletPool) != 0):
            b = self.deadBulletPool.pop()
        else:
            b = bullet()
        print("b created")
        b.init(shooter)
        self.bulletPool.append(b)

    def updateBullets(self, delta):
        for bullet in self.bulletPool:
            if (bullet.dead):
                print("b dead")
                self.deadBulletPool.append(bullet)
                self.bulletPool.remove(bullet)
                continue
            bullet.update(delta)

    def drawBullets(self, w):
        for bullet in self.bulletPool:
            bullet.draw(w)
