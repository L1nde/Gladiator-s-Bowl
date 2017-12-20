import pygame


class button:
    def __init__(self, x0, y0, x1, y1, text, method):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.text = text
        self.method = method
        self.font = pygame.font.SysFont('Arial', 18)

    def draw(self, w):
        pygame.draw.rect(w, (150, 150, 150), (self.x0, self.y0, self.x1, self.y1))
        w.blit(self.font.render(self.text, False, (0, 0, 0)), (self.x0 + 5, self.y0 + 2))  # fix it

    def onClick(self, clickPos):
        if (clickPos[0] > self.x0 and clickPos[0] < self.x0 + self.x1 and clickPos[1] > self.y0 and clickPos[
            1] < self.y0 + self.y1):
            self.method()
