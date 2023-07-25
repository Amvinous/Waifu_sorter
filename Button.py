import pygame


class Button:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.is_clicked = False

    def draw(self, surface, color):
        pygame.draw.rect(surface, color, self.rect)

    def click(self, pos):
        if self.rect.collidepoint(pos):
            self.is_clicked = True
