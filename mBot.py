import math
from random import random

from keras.layers import Dense, initializers
from keras.models import Sequential

from bot import *


class mBot(bot):
    def __init__(self, x, y, entityManager, model):
        super().__init__(x, y, entityManager)

        self.eyes = [eye(400, radians(10), radians(4), self), eye(400, radians(10), radians(-4), self)]
        self.radar = radar(self)
        self.brain = brain(model)
        self.selfDestructTime = 10
        self.currentSelfDestructTime = 10


    def update(self, delta):
        super().update(delta)
        outputs = self.brain.getOutputs(self.getInputs(delta))[0]
        self.speed = outputs[0] * 200
        if (abs(self.speed) < 50):
            self.dealWithBadBehaviour(delta)
        self.direction += outputs[1] * delta * 3

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
        self.currentSelfDestructTime -= delta / 30
        self.reload(delta)
        if (sigmoid(outputs[2]) > 0):
            self.shoot()

        if (self.currentSelfDestructTime <= 0):
            self.em.killBot(self)

    def dealWithBadBehaviour(self, delta):
        self.currentSelfDestructTime -= delta
        self.score -= delta / 10

    def reset(self):
        super().reset()
        self.currentSelfDestructTime = self.selfDestructTime

    def draw(self, w):
        # self.drawEyes(w)
        pygame.draw.circle(w, (0, 0, 255), (int(self.x), int(self.y)), 13)
        pygame.draw.circle(w, (255, 0, 0),
                           (int(self.x + 8 * cos(self.direction)), int(self.y + 8 * sin(self.direction))), 3)

    def drawEyes(self, w):
        for eye in self.eyes:
            eye.draw(w)

    def getInputs(self, delta):
        inputs = []

        # eyes
        c = 0
        for i in self.eyes:
            if (c < 2):
                sight = i.canSeeEnemy(self.em.bots)
                if (sight == 1):
                    self.score += delta
            else:
                sight = i.canSeeEnemyBullet(self.em.bulletPool)

            inputs.append(sight)
            c += 1

        # Radar
        closestBullet = self.radar.getClosestBullet(self.em.bulletPool)
        if closestBullet is None:
            inputs.append(0)
            inputs.append(0)
        else:
            distFromBullet = math.sqrt((self.x - closestBullet[0]) ** 2 + (self.y - closestBullet[1]) ** 2)
            if (distFromBullet <= 200):
                inputs.append(1 - distFromBullet / 200)
                targetVector = np.subtract(closestBullet, self.getPos())
                dirUnitVector = (sin(self.direction), cos(self.direction))
                if np.dot(targetVector, dirUnitVector) < 0:
                    inputs.append(-1)
                else:
                    inputs.append(1)
            else:
                inputs.append(0)
                inputs.append(0)

        #Other
        if (self.currentCooldown <= 0):
            inputs.append(1)
        else:
            inputs.append(0)
        return inputs


# I have no idea what I'm doing
class brain:
    def __init__(self, model):
        if (model == None):
            self.model = Sequential()
            self.model.add(
                Dense(8, activation="tanh", input_dim=6,
                      kernel_initializer=initializers.RandomUniform(minval=-1, maxval=1, seed=None)))
            self.model.add(
                Dense(3, activation="tanh",
                      kernel_initializer=initializers.RandomUniform(minval=-1, maxval=1, seed=None)))
            self.model.compile(loss='mean_squared_error', optimizer='adam')
        else:
            self.model = model

    def getOutputs(self, inputs):
        inputs.append(1)
        return self.model.predict(np.asarray([inputs]))

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
                    k = 0
                    if random() < 0.1:
                        k = randint(-100, 100) / 100

                    if (r < 0.4):
                        w.append(b1weights[n][m] + k)
                    elif r > 0.6:
                        w.append(b2weights[n][m] + k)
                    else:
                        w.append((b1weights[n][m] + b2weights[n][m]) / 2 + k)

                newWeights.append(w)
            newBrain.append(newWeights)
            newBrain.append(self.model.get_weights()[i + 1])
        self.model.set_weights(newBrain)

def sigmoid(x):
    return 1 / (1 + math.exp(-x))
