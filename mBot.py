import math
from random import random

from keras import Sequential
from keras.layers import Dense

from bot import *


class mBot(bot):
    def __init__(self, x, y, entityManager):
        super().__init__(x, y, entityManager)

        self.eyes = [eye(200, radians(30), radians(12), self), eye(200, radians(30), radians(-12), self),
                     eye(200, radians(50), radians(50), self), eye(200, radians(50), radians(-50), self)]
        self.brain = brain()
        self.selfDestructTime = 3
        self.currentSelfDestructTime = 3


    def update(self, delta):
        super().update(delta)
        outputs = self.brain.getOutputs(self.getInputs())
        self.speed = outputs[0] * 1000
        if (abs(self.speed) < 50):
            self.dealWithBadBehaviour(delta)

        self.direction += outputs[1] * delta * 100

        self.xSpeed = self.speed * cos(self.direction)
        self.ySpeed = self.speed * sin(self.direction)
        newX = self.x + self.xSpeed * delta
        newY = self.y + self.ySpeed * delta

        if (newX > 1000 - self.radius):
            newX = 1000 - self.radius
            self.dealWithBadBehaviour(delta)
        elif (newX < self.radius):
            newX = self.radius
            self.dealWithBadBehaviour(delta)

        if (newY > 800 - self.radius):
            newY = 800 - self.radius
            self.dealWithBadBehaviour(delta)
        elif (newY < self.radius):
            newY = self.radius
            self.dealWithBadBehaviour(delta)

        self.x = newX
        self.y = newY

        self.reload(delta)
        if (outputs[2] > 0):
            self.shoot()

        if (self.currentSelfDestructTime <= 0):
            self.em.killBot(self)

    def dealWithBadBehaviour(self, delta):
        self.currentSelfDestructTime -= delta
        self.score -= delta / 10

    def reset(self):
        super().reset()
        self.createNewBrain()
        self.currentSelfDestructTime = self.selfDestructTime

    def createNewBrain(self):
        if (random() < 0.1):
            self.brain = brain()
        else:
            bot1, bot2 = self.em.getTwoRandomHighScoreMBots()
            self.brain.mutate(bot1.brain.model, bot2.brain.model)

    def draw(self, w):
        # self.drawEyes(w)
        pygame.draw.circle(w, (0, 0, 255), (int(self.x), int(self.y)), 13)
        pygame.draw.circle(w, (255, 0, 0),
                           (int(self.x + 8 * cos(self.direction)), int(self.y + 8 * sin(self.direction))), 3)

    def drawEyes(self, w):
        for eye in self.eyes:
            eye.draw(w)

    def getInputs(self):
        inputs = []
        for eye in self.eyes:
            inputs.append(eye.getVisionB(self.em.bots, self.em.bulletPool))

        inputs.append(sigmoid(self.getDistanceFromCentre()) - 0.25)
        return inputs

    def getDistanceFromCentre(self):
        return distance.euclidean(self.getPos(), (500, 400))


# I have no idea what I'm doing
class brain:
    def __init__(self):
        self.model = Sequential()
        self.model.add(Dense(12, input_dim=1), )
        self.model.add(Dense(12))
        self.model.add(Dense(3))
        self.model.compile(loss='mean_squared_error', optimizer='sgd')

    def getOutputs(self, inputs):
        inputs.append(1)
        return np.sum(self.model.predict(inputs), axis=0)

    def mutate(self, brain1, brain2):
        newBrain = []
        for i in range(0, len(self.model.get_weights()), 2):
            newWeights = []
            b1weights = brain1.get_weights()[i]
            b2weights = brain2.get_weights()[i]
            for n in range(len(b1weights)):
                w = []
                for m in range(len(b1weights[0])):
                    r = random()
                    if (r < 0.45):
                        w.append(b1weights[n][m] + randint(-120, 120) / 1000)
                    elif (r > 0.55):
                        w.append(b2weights[n][m] + randint(-120, 120) / 1000)
                    else:
                        w.append(self.model.get_weights()[i][n][m])
                newWeights.append(w)
            newBrain.append(newWeights)
            newBrain.append(self.model.get_weights()[i + 1])
        self.model.set_weights(newBrain)

def sigmoid(x):
    return 1 / (1 + math.exp(-x))
