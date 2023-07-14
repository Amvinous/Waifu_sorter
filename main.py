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
import threading


class RunWindow:

    def __init__(self):
        self.button2 = Button(210, 450, 140, 50, (21, 31, 46))
        self.button1 = Button(50, 450, 140, 50, (21, 31, 46))
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
        while self.running:
            self.clock.tick(5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.button1.click(mouse_pos):
                            self.button1.is_clicked = True
                            threading.Thread(target=sort.sorting(self.button1), args=("left",)).start()
                        elif self.button2.click(mouse_pos):
                            self.button2.is_clicked = True
                            threading.Thread(target=sort.sorting(self.button2), args=("right",)).start()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.button1.is_clicked = False
                        self.button2.is_clicked = False
            pygame.draw.rect(self.screen, (0, 255, 0) if self.button1.is_clicked else (0, 150, 0), self.button1)
            pygame.draw.rect(self.screen, (255, 0, 0) if self.button2.is_clicked else (150, 0, 0), self.button2)
            self.display.flip()

        pygame.quit()


if __name__ == '__main__':
    sort = Sorter()

    # * Lists

    sort.get_list()

    # * Run Window

    window = RunWindow()
    window.main_loop()
