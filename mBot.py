from bot import *


class mBot(bot):
    def __init__(self, x, y, entityManager):
        super().__init__(x, y, entityManager)

        self.eyes = [eye(200, radians(30), radians(12), self), eye(200, radians(30), radians(-12), self), eye(200, radians(50), radians(50), self), eye(200, radians(50), radians(-50), self),
                     eye(200, radians(70), radians(120), self), eye(200, radians(70), radians(-120), self)]

    def update(self, delta):
        super().update(delta)
        self.reload(delta)
        self.shoot()

    def draw(self, w):
        #self.drawEyes(w)
        pygame.draw.circle(w, (0, 0, 255), (self.x, self.y), 13)
        pygame.draw.circle(w, (255, 0, 0), (self.x + round(8*cos(self.direction)), self.y + round(8*sin(self.direction))), 3)


    def drawEyes(self, w):
        for eye in self.eyes:
            eye.draw(w)

    def createModel(self):
        self.model = Sequential()
