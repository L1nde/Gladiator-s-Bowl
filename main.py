import pygame
import time
import bot
import random
from math import sqrt, cos, sin, pi
import matplotlib.pyplot as plt

pygame.init()
screenSize = (1200, 800)
w = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Gladiators' bowl")
w.fill((255, 255, 255))
pygame.display.flip()
time0 = time.clock()

bot = bot.bot(100, 100)

def update(delta):
    event = pygame.event.poll()


def draw():
    w.fill((255, 255, 255))
    drawUI()
    bot.draw(w)
    pygame.display.flip()


def drawUI():
    pygame.draw.rect(w, (100,100,100), (1000,0, 1200, 800))


while True:
    update(time.clock() - time0)
    time0 = time.clock()
    draw()

