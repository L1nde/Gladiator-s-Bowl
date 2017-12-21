from math import atan2

from bot import *


class player(bot):

    def __init__(self, x, y, entitymanager):
        super().__init__(x, y, entitymanager)
        self.speed = 100
        self.hp = 10
        # self.cooldown = 0

        self.eyes = [eye(0, 0, 0, self)]

    def update(self, delta):
        super().update(delta)
        self.reload(delta)
        self.direction = atan2(self.y -pygame.mouse.get_pos()[1], self.x-pygame.mouse.get_pos()[0])+ radians(180)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed * delta
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed * delta
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed * delta
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed * delta
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            self.shoot()

    def draw(self, w):
        pygame.draw.circle(w, (241, 255, 33), (int(self.x), int(self.y)), 13)
        pygame.draw.circle(w, (255, 0, 0),
                           (int(self.x + 8 * cos(self.direction)), int(self.y + 8 * sin(self.direction))), 3)
