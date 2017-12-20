from entityManager import *
from userinterface import ui

pygame.init()
pygame.font.init()
screenSize = (1200, 800)
w = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Gladiators' bowl")
w.fill((255, 255, 255))
pygame.display.flip()
em = entityManager()
ui = ui(em)
c = pygame.time.Clock()

def update(delta):
    event = pygame.event.poll()
    em.update(delta)
    ui.update(event)

def draw():
    w.fill((255, 255, 255))
    em.draw(w)
    ui.draw(w)
    pygame.display.flip()

while True:
    c.tick()
    update(c.get_time() / 1000)
    draw()
