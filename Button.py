import pygame


class Button:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.is_clicked = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def click(self, pos):
        self.is_clicked = self.rect.collidepoint(pos)
