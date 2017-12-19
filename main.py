import pygame
import time
from bot import *
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

bot = bot(400, 400)

def update(delta):
    event = pygame.event.poll()
    if event.type == pygame.MOUSEBUTTONDOWN:
        bot.eye.isInSight(pygame.mouse.get_pos())


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

