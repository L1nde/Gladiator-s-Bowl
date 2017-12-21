from bot import *
from random import choice
from keras import initializers
from keras.models import Sequential, Input
from keras.layers import Dense, Activation, Flatten

class lBot(bot):

    def __init__(self, x, y, entitymanager):
        super().__init__(x, y, entitymanager)

        self.eyes = [eye(200, radians(30), radians(12), self), eye(200, radians(30), radians(0), self)]
        self.brain = Brain()
        self.hunger = 5

    def update(self, delta):
        super().update(delta)
        self.reload(delta)

        output = self.brain.getOutputs(self.getInput())
        self.direction += radians(output[0]*360) *delta
        self.speed = output[1] * 10
        self.x += self.speed * cos(self.direction) * delta
        self.y += self.speed * sin(self.direction) * delta
        if self.x > 800 or self.x < 0:
            self.reset()
        if self.y > 800 or self.y < 0:
            self.reset()
        if output[1] > 0.5:
            self.shoot()



    def reset(self):
        super().reset()
        bot1, bot2 = self.em.getTwoRandomHighScoreLBots()
        self.brain.mutate(bot1.brain, bot2.brain)



    def draw(self, w):
        self.drawEyes(w)
        pygame.draw.circle(w, (129, 255, 129), (int(self.x), int(self.y)), 13)
        pygame.draw.circle(w, (255, 0, 0), (int(self.x + 8*cos(self.direction)), int(self.y + 8*sin(self.direction))), 3)

    def drawEyes(self, w):
        for eye in self.eyes:
            eye.draw(w)

    def getInput(self):
        inputs = []
        for eye in self.eyes:
            inputs.append(eye.canSeeEnemy(self.em.bots))
        return inputs

class Brain:

    def __init__(self):
        self.model = Sequential()
        self.model.add(Dense(12, input_dim=1, activation='relu', kernel_initializer=initializers.RandomUniform(minval=-1, maxval=1, seed=None)))
        self.model.add(Dense(8, activation='relu', kernel_initializer=initializers.RandomUniform(minval=-1, maxval=1, seed=None)))
        self.model.add(Dense(2, activation='sigmoid', kernel_initializer=initializers.RandomUniform(minval=-1, maxval=1, seed=None)))
        self.model.compile(optimizer='adam', loss='mean_squared_error')

    def getOutputs(self, inputs):
        return np.sum(self.model.predict(inputs), axis=0)

    def mutate(self, brain1, brain2):
        weights1 = brain1.model.get_weights()
        weights2 = brain2.model.get_weights()
        for i in range(len(weights1)):
            for j in range(len(weights1[i])):
                weights1[i][j] += choice([weights1[i][j], weights2[i][j]])

        self.model.set_weights(weights1)



