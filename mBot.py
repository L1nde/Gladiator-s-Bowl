import math
from keras import Sequential, Input
from keras.layers import Dense, Activation, Flatten

from bot import *


class mBot(bot):
    def __init__(self, x, y, entityManager):
        super().__init__(x, y, entityManager)

        self.eyes = [eye(200, radians(30), radians(12), self), eye(200, radians(30), radians(-12), self), eye(200, radians(50), radians(50), self), eye(200, radians(50), radians(-50), self)]
        self.brain = brain()

    def update(self, delta):
        super().update(delta)
        outputs = self.brain.getOutputs(self.getInputs())
        self.speed = outputs[0] * 1000
        self.direction = outputs[1] * delta * 500

        self.xSpeed = self.speed * cos(self.direction)
        self.ySpeed = self.speed * sin(self.direction)
        newX = self.x + self.xSpeed * delta
        newY = self.y + self.ySpeed * delta

        if (newX > 1000 - self.radius):
            newX = 1000 - self.radius
        elif (newX < self.radius):
            newX = self.radius

        if (newY > 800 - self.radius):
            newY = 800 - self.radius
        elif (newY < self.radius):
            newY = self.radius

        self.x = newX
        self.y = newY

        self.reload(delta)
        if (outputs[2] > 0.5):
            self.shoot()

    def draw(self, w):
        #self.drawEyes(w)
        pygame.draw.circle(w, (0, 0, 255), (int(self.x), int(self.y)), 13)
        pygame.draw.circle(w, (255, 0, 0), (int(self.x + 8*cos(self.direction)), int(self.y + 8*sin(self.direction))), 3)


    def drawEyes(self, w):
        for eye in self.eyes:
            eye.draw(w)

    def getInputs(self):
        inputs = []
        for eye in self.eyes:
            inputs.append(eye.canSeeEnemy(self.em.bots))

        inputs.append(sigmoid(self.getDistanceFromCentre()) - 0.25)
        return inputs

    def getDistanceFromCentre(self):
        return distance.euclidean(self.getPos(), (500,400))

#I have no idea what I'm doing
class brain:

    def __init__(self):
        self.model = Sequential()
        self.x1 = Dense(12, input_dim=1)
        self.model.add(self.x1)
        self.x2 = Dense(3)
        self.model.add(self.x2)
        self.model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

    def getOutputs(self, inputs):
        inputs.append(1)
        return np.sum(self.model.predict(inputs), axis=0)


def sigmoid(x):
  return 1 / (1 + math.exp(-x))


