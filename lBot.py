from random import random, choice

from keras import initializers
from keras.layers import Dense
from keras.models import Sequential
from keras.utils import plot_model

from bot import *


class lBot(bot):
    def __init__(self, x, y, entitymanager):
        super().__init__(x, y, entitymanager)
        r = randint(-180,180)
        # self.direction = radians(r)
        self.eyes = [eye(350, radians(10), radians(0), self), eye(200, radians(30), radians(10), self), eye(200, radians(30), radians(-10), self)]
        self.brain = Brain()
        self.destructionTime = 15
        self.destruction = self.destructionTime

    def update(self, delta):
        super().update(delta)
        self.reload(delta)
        self.destruction -= delta

        output = self.brain.getOutputs(self.getInput())[0]
        self.direction += radians(output[0] * 180) * delta
        self.speed = output[1] * 50
        self.x += self.speed * cos(self.direction) * delta
        self.y += self.speed * sin(self.direction) * delta
        if self.x > 1000 or self.x < 0:
            self.reset()
            self.score -= 13
        if self.y > 800 or self.y < 0:
            self.reset()
            self.score -= 13
        if output[2] > 0:
            self.shoot()
            self.score -= 1

        if self.destruction < 0:
            self.reset()

    def reset(self):
        super().reset()
        self.destruction = self.destructionTime
        bot1, bot2 = self.em.getTwoRandomHighScoreLBots()
        # plot_model(bot1.brain.model, to_file="model.png")
        self.brain.breed(bot1.brain, bot2.brain)

    def draw(self, w):
        # self.drawEyes(w)
        pygame.draw.circle(w, (129, 255, 129), (int(self.x), int(self.y)), 13)
        pygame.draw.circle(w, (255, 0, 0), (int(self.x + 8*cos(self.direction)), int(self.y + 8*sin(self.direction))), 3)

    def drawEyes(self, w):
        for eye in self.eyes:
            eye.draw(w)

    def getInput(self):
        inputs = [self.x, self.y, self.currentCooldown]
        for eye in self.eyes:
            sight = eye.canSeeEnemy(self.em.bots)
            inputs.append(sight)
            self.score += sight/20
            inputs.append(eye.canSeeEnemyBullet(self.em.bulletPool))
        return inputs

class Brain:
    def __init__(self):
        self.model = Sequential()
        self.model.add(Dense(12, input_dim=9, activation="tanh", kernel_initializer=initializers.RandomUniform(minval=-1, maxval=1, seed=None)))
        self.model.add(Dense(20, activation="tanh", kernel_initializer=initializers.RandomUniform(minval=-1, maxval=1, seed=None)))
        self.model.add(Dense(3, activation="tanh", kernel_initializer=initializers.RandomUniform(minval=-1, maxval=1, seed=None)))
        self.model.compile(optimizer='sgd', loss='mean_squared_error')

    def getOutputs(self, inputs):
        return self.model.predict(np.asarray([inputs]))

    def breed(self, brain1, brain2):
        newBrain = []
        for i in range(0, len(self.model.get_weights()), 2):
            newWeights = []
            b1weights = brain1.model.get_weights()[i]
            b2weights = brain2.model.get_weights()[i]
            for j in range(len(b1weights)):
                w = []
                for k in range(len(b1weights[0])):
                    r = random()
                    if r > 0.8:
                        w.append(randint(-1000, 1000)/1000)
                    else:
                        w.append(choice([b1weights[j][k], b2weights[j][k]]))
                newWeights.append(w)
            newBrain.append(newWeights)
            newBrain.append(self.model.get_weights()[i + 1])
        self.model.set_weights(newBrain)
