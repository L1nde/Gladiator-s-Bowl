from random import random, choice

from keras import initializers
from keras.layers import Dense
from keras.models import Sequential

from bot import *


class lBot(bot):
    def __init__(self, x, y, entitymanager, model):
        super().__init__(x, y, entitymanager)
        r = randint(-180,180)
        # self.direction = radians(r)
        self.eyes = [eye(500, radians(10), radians(2.5), self), eye(500, radians(10), radians(-2.5), self)]
        self.brain = Brain(model)
        self.baseAge = 15
        self.age = self.baseAge

    def update(self, delta):
        super().update(delta)
        self.reload(delta)
        self.age -= delta

        output = self.brain.getOutputs(self.getInput())[0]
        self.direction += radians(output[0] * 180) * delta
        self.speed = output[1] * 200
        if abs(self.speed) < 50:
            self.score -= delta
        self.x += self.speed * cos(self.direction) * delta
        self.y += self.speed * sin(self.direction) * delta
        if self.x > 1000 or self.x < 0:
            self.score -= 13
            self.age -= self.baseAge
        if self.y > 800 or self.y < 0:
            self.score -= 13
            self.age -= self.baseAge
        if output[2] > 0:
            self.shoot()

        if self.age < 0:
            self.em.killBot(self)

    def reset(self):
        super().reset()
        self.age = self.baseAge
        # plot_model(bot1.brain.model, to_file="model.png")
        parents = self.em.getRandomLParents()
        self.brain.breed(parents[0].brain, parents[1].brain)

    def shoot(self):
        if super().shoot():
            self.score -= 1


    def draw(self, w):
        # self.drawEyes(w)
        pygame.draw.circle(w, (129, 255, 129), (int(self.x), int(self.y)), 13)
        pygame.draw.circle(w, (255, 0, 0), (int(self.x + 8*cos(self.direction)), int(self.y + 8*sin(self.direction))), 3)

    def drawEyes(self, w):
        for eye in self.eyes:
            eye.draw(w)

    def getInput(self):
        inputs = [1 if self.currentCooldown == 0 else 0, sigmoid(self.distanceFromCentre())]
        for eye in self.eyes:
            sight = eye.canSeeEnemy(self.em.bots)
            inputs.append(sight)
            self.score += sight/10
            inputs.append(eye.canSeeEnemyBullet(self.em.bulletPool))
        return inputs

    def distanceFromCentre(self):
        return np.linalg.norm(np.asarray(self.getPos())-np.asarray((500,400)))

class Brain:
    def __init__(self, model):
        if (model == None):
            self.model = Sequential()
            self.model.add(Dense(12, input_dim=6, activation="tanh",
                                 kernel_initializer=initializers.RandomUniform(minval=-1, maxval=1, seed=None)))

            # self.model.add(Dense(20, activation="tanh",
            #                      kernel_initializer=initializers.RandomUniform(minval=-1, maxval=1, seed=None)))
            # self.model.add(Dense(20, activation="tanh",
            #                      kernel_initializer=initializers.RandomUniform(minval=-1, maxval=1, seed=None)))
            # self.model.add(Dense(20, activation="tanh",
            #                      kernel_initializer=initializers.RandomUniform(minval=-1, maxval=1, seed=None)))
            self.model.add(Dense(3, activation="tanh",
                                 kernel_initializer=initializers.RandomUniform(minval=-1, maxval=1, seed=None)))
            self.model.compile(optimizer='sgd', loss='mean_squared_error')
        else:
            self.model = model

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
                        genome = choice([b1weights[j][k], b2weights[j][k]])
                        w.append(genome + randint(-100, 100)/1000)
                    else:
                        w.append(choice([b1weights[j][k], b2weights[j][k]]))
                newWeights.append(w)
            newBrain.append(newWeights)
            newBrain.append(self.model.get_weights()[i + 1])
        self.model.set_weights(newBrain)
