# * imports
import requests as rq
# * images
from PIL import Image
from io import BytesIO
# * pygame
import pygame
import fonts.ttf as fonts
# * my modules
from Sorter import Sorter
from Button import Button


class RunWindow:

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.initialized = False
        self.display = pygame.display
        self.background_color = (11, 22, 34)
        self.screen = None
        self.text_color = (250, 250, 250)
        self.clock = pygame.time.Clock()
        self.image1 = None
        self.image2 = None
        self.running = True

    def init_window(self):
        # + create the actual window
        width, height = 400, 700
        self.screen = self.display.set_mode((width, height))
        self.display.set_caption("Anilist Sorter")
        self.screen.fill(self.background_color)
        # + add different aspect to the window
        self.make_label(25, 25, width - 50, height / 8, (21, 31, 46), sort.user)
        # self.add_images()
        self.add_icon()
        # + initialize
        self.initialized = True

    def add_icon(self):
        icon_image_rgba = Image.open(BytesIO(rq.get("https://i.imgur.com/9iPDCuY.png").content)).convert("RGBA")
        image_data_bytes = icon_image_rgba.tobytes()
        image_data_size = icon_image_rgba.size
        new_icon = pygame.image.frombytes(image_data_bytes, image_data_size, "RGBA")
        self.display.set_icon(new_icon)

    def add_images(self):
        pass
        # self.image1 = pygame.image.load(BytesIO(sort.object_dict["left"].pic)).convert()
        # self.image2 = pygame.image.load(BytesIO(sort.object_dict["right"].pic)).convert()

    def make_label(self, x, y, width, height, color, label):
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        font_data = fonts.font_files.get("Roboto")
        font = pygame.font.Font(font_data, 36)
        text = font.render(label, True, self.text_color)
        text_rect = text.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text, text_rect)

    def main_loop(self):

        self.init_window()
        button1 = Button(50, 450, 140, 50, (21, 31, 46))
        button2 = Button(210, 450, 140, 50, (21, 31, 46))
        sort.sorting(self.clock, self.screen, button1, button2)
        print(sort.name_list)
        while self.running:
            self.clock.tick(5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            if self.initialized:
                # self.screen.blit(self.image1, (50, 150))
                # self.screen.blit(self.image2, (200, 150))
                button1.draw(self.screen)
                button2.draw(self.screen)
            self.display.flip()

        pygame.quit()


if __name__ == '__main__':
    sort = Sorter()

    # * Lists

    sort.get_list()

    # * Run Window

    window = RunWindow()
    window.main_loop()
