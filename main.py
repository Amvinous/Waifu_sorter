# * imports
import requests as rq
import pathlib
from random import sample
# * images
from PIL import Image
from io import BytesIO
# * pygame
import pygame
# * my modules
from Sorter import Sorter


class Button:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.is_clicked = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def click(self, pos):
        self.is_clicked = self.rect.collidepoint(pos)


class RunWindow:

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.initialized = False
        self.display = pygame.display
        self.background_color = (30, 30, 30)
        self.screen = None
        self.text_color = (250, 250, 250)
        self.clock = pygame.time.Clock()
        self.image1 = None
        self.image2 = None
        self.running = True

    def init_window(self):
        # * create the actual window
        width, height = 400, 600
        self.screen = self.display.set_mode((width, height))
        self.display.set_caption("Anilist Sorter")
        self.screen.fill(self.background_color)
        # * add different aspect to the window
        self.make_label(50, 25, width * 0.8, height / 8, sort.user)
        # self.add_images()
        self.add_icon()
        # * initialize
        self.initialized = True

    def add_icon(self):
        icon_image_rgba = Image.open(BytesIO(rq.get("https://i.imgur.com/9iPDCuY.png").content)).convert("RGBA")
        image_data_bytes = icon_image_rgba.tobytes()
        image_data_size = icon_image_rgba.size
        new_icon = pygame.image.frombytes(image_data_bytes, image_data_size, "RGBA")
        self.display.set_icon(new_icon)

    def add_images(self):

        self.image1 = pygame.image.load(BytesIO(sort.object_dict["left"].pic)).convert()
        self.image2 = pygame.image.load(BytesIO(sort.object_dict["right"].pic)).convert()

    def make_label(self, x, y, width, height, label):
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, width, height))
        font = pygame.font.SysFont("Arial", 24)
        text = font.render(label, True, self.text_color)
        text_rect = text.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text, text_rect)

    def main_loop(self):

        self.init_window()
        button1 = Button(50, 350, 100, 50, (222, 136, 24))
        button2 = Button(200, 350, 100, 50, (222, 136, 24))
        sort.sorting(self.clock, button1, button2, self.screen)
        print(sort.name_list)
        while self.running:
            self.clock.tick(5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            if self.initialized:
                self.screen.blit(self.image1, (50, 150))
                self.screen.blit(self.image2, (200, 150))
                button1.draw(self.screen)
                button2.draw(self.screen)
            self.display.flip()

        pygame.quit()


if __name__ == '__main__':
    # * Inputs
    user_input = input("Enter Account name: ").strip()
    path = pathlib.Path("Users")
    user_list = list(filter(lambda p: p.is_file(), path.rglob("**/*.txt")))
    # ! Automatic input
    # sort = Sorter("Amvi", path, user_list)
    # ! Manual input
    sort = Sorter(user_input, path, user_list)

    # * Lists
    sort.fetch()

    # * Run Window

    window = RunWindow()
    window.main_loop()
