# * imports
import requests as rq
# * images
from PIL import Image
from io import BytesIO
# * pygame
import pygame
import fonts.ttf as fonts
# * my modules
from Sorter import Sorter, Selection
from Button import Button
import threading


class RunWindow:

    def __init__(self):
        self.right_button = Button(210, 450, 140, 50, (21, 31, 46))
        self.left_button = Button(50, 450, 140, 50, (21, 31, 46))
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

    def start_sorting(self):
        sorting = sort.merge_sort()
        sort_stage = next(sorting)
        print(sort_stage)
        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:

                        self.left_button.click(event.pos)
                        self.right_button.click(event.pos)

                        if self.left_button.is_clicked:
                            sort.select(Selection.LEFT)

                        if self.right_button.is_clicked:
                            sort.select(Selection.RIGHT)

                        try:
                            sort_stage = next(sorting)
                        except StopIteration:
                            return
                        print(sort_stage)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            self.left_button.is_clicked = False
                            self.right_button.is_clicked = False

            if self.initialized:
                self.left_button.draw(self.screen)
                self.right_button.draw(self.screen)
            self.display.flip()


    def main_loop(self):
        self.init_window()
        #get user name
        #get the list
        self.start_sorting()

        #self.results

        pygame.quit()


if __name__ == '__main__':
    #! initialize with the list
    sort = Sorter()

    # * Lists

    sort.get_list()

    # * Run Window

    window = RunWindow()
    window.main_loop()
