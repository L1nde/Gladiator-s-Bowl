from random import choice

from keras import initializers
from keras.layers import Dense
from keras.models import Sequential

from bot import *


class lBot(bot):
    def __init__(self, x, y, entitymanager):
        super().__init__(x, y, entitymanager)
        r = randint(0,360)
        self.direction = radians(180)
        self.eyes = [eye(200, radians(30), radians(-7.5), self), eye(200, radians(30), radians(7.5), self)]
        self.brain = Brain()
        self.hunger = 5

    def update(self, delta):
        super().update(delta)
        self.reload(delta)

        output = self.brain.getOutputs(self.getInput())
        self.direction = radians(output[0]*360) *delta
        self.speed = output[1] * 100
        self.x += self.speed * cos(self.direction) * delta
        self.y += self.speed * sin(self.direction) * delta
        if self.x > 1000 or self.x < 0:
            self.reset()
            self.score -= 3
        if self.y > 800 or self.y < 0:
            self.reset()
            self.score -= 3
        if output[2] > 0.5:
            self.shoot()
            self.score -= 1

    def reset(self):
        super().reset()
        bot1, bot2 = self.em.getTwoRandomHighScoreLBots()
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
            inputs.append(eye.canSeeEnemy(self.em.bots))
        return np.asarray(inputs)

class Brain:
    def __init__(self):
        self.model = Sequential()
        self.model.add(Dense(5, input_dim=1, activation='relu', kernel_initializer=initializers.RandomUniform(minval=-1, maxval=1, seed=None), bias_initializer=initializers.RandomUniform(minval=-10, maxval=10, seed=None)))
        self.model.add(Dense(12, activation='relu', kernel_initializer=initializers.RandomUniform(minval=-1, maxval=1, seed=None), bias_initializer=initializers.RandomUniform(minval=-10, maxval=10, seed=None)))
        self.model.add(Dense(3, activation='sigmoid', kernel_initializer=initializers.RandomUniform(minval=-1, maxval=1, seed=None), bias_initializer=initializers.RandomUniform(minval=-10, maxval=10, seed=None)))
        self.model.compile(optimizer='sgd', loss='mean_squared_error')

    def getOutputs(self, inputs):
        return np.sum(self.model.predict(inputs), axis=0)

    def breed(self, brain1, brain2):
        weights1 = np.asarray(brain1.model.get_weights())
        weights2 = np.asarray(brain2.model.get_weights())
        shape = np.shape(weights1)
        fweights1 = weights1.flatten()
        fweights2 = weights2.flatten()
        r = randint(-350, 350)/1000
        chance = randint(-100,100)/100
        for i in range(len(fweights1)):
            fweights1[i] = choice([fweights1[i], fweights2[i]])
            if chance > 0.5:
                fweights1[i] *= chance
        weights1.reshape(shape)

        self.model.set_weights(weights1)
