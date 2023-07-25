# * imports
import sys
from io import BytesIO

import fonts.ttf as fonts
# * pygame
import pygame
import requests as rq
# * images
from PIL import Image

from Anilist import Anilist
from Button import Button
# * my modules
from Sorter import Sorter, Selection


class RunWindow:

    def __init__(self):
        self.right_button = Button(210, 400, 140, 50)
        self.left_button = Button(50, 400, 140, 50)
        pygame.init()
        pygame.font.init()
        self.initialized = False
        self.display = pygame.display
        self.background_color = (11, 22, 34)
        self.second_color = (21, 31, 46)
        self.screen = None
        self.text_color = (250, 250, 250)
        self.image1 = None
        self.image2 = None
        self.init_window()

    def init_window(self):
        # + create the actual window
        width, height = 400, 700
        self.screen = self.display.set_mode((width, height))
        self.display.set_caption("Anilist Sorter")
        self.screen.fill(self.background_color)
        # + add different aspect to the window
        self.add_icon()
        # + initialize
        self.initialized = True

    def add_icon(self):
        icon_image_rgba = Image.open(BytesIO(rq.get("https://i.imgur.com/9iPDCuY.png").content)).convert("RGBA")
        image_data_bytes = icon_image_rgba.tobytes()
        image_data_size = icon_image_rgba.size
        new_icon = pygame.image.frombytes(image_data_bytes, image_data_size, "RGBA")
        self.display.set_icon(new_icon)

    def add_image(self, image, width, height):
        image = pygame.image.load(BytesIO(image.pic)).convert()
        image = pygame.transform.scale(image, (width, height))
        return image

    def make_label(self, x, y, width, height, color, label, font_size):
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        font_data = fonts.font_files.get("Roboto")
        font = pygame.font.Font(font_data, font_size)
        text = font.render(label, True, self.text_color)
        text_rect = text.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text, text_rect)

    def get_name(self):
        base_font = pygame.font.Font(None, 36)
        user_text = ''

        input_rect = pygame.Rect(25, 150, 350, 75)

        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                        self.screen.fill(self.background_color)
                        return user_text

                    else:
                        user_text += event.unicode

            self.screen.fill(self.background_color)
            self.make_label(25, 25, 350, 75, self.second_color, "Type in Anilist Username and press Enter", 24)
            pygame.draw.rect(self.screen, self.second_color, input_rect)
            text_surface = base_font.render(user_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (input_rect.x + 25, input_rect.y + 25))
            self.display.flip()

    def start_sorting(self):
        self.make_label(25, 25, 350, 87, self.second_color, anilist.user, 36)
        sorting = sort.merge_sort()
        try:
            sort_stage = next(sorting)
        except StopIteration:
            return sorting
        left_pick = sort_stage[0]
        right_pick = sort_stage[1]
        while True:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.left_button.click(event.pos)
                    self.right_button.click(event.pos)

                    if self.left_button.is_clicked:
                        sort.select(Selection.LEFT)
                        self.left_button.is_clicked = False

                    if self.right_button.is_clicked:
                        sort.select(Selection.RIGHT)
                        self.right_button.is_clicked = False

                    try:
                        sort_stage = next(sorting)
                    except StopIteration:
                        return sort.sorted_list

                    left_pick = sort_stage[0]
                    right_pick = sort_stage[1]

            if self.initialized:
                self.left_button.draw(self.screen, self.second_color)
                self.right_button.draw(self.screen, self.second_color)
                self.screen.blit(self.add_image(left_pick, 140, 210), (50, 150))
                self.screen.blit(self.add_image(right_pick, 140, 210), (210, 150))

            self.display.flip()

    def display_results(self, char_list):
        self.screen.fill(self.background_color)
        height = 30
        for char in char_list:
            self.screen.blit(self.add_image(char, 60, 90), (30, height))
            self.make_label(100, height, 125, 25, self.background_color, char.name, 26)

            height += 110

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            self.display.flip()

    def main_loop(self):
        sorted_list = self.start_sorting()
        if sorted_list is not None:
            self.display_results(sorted_list)

        # ? self.results

        pygame.quit()


if __name__ == '__main__':
    # ! initialize with the list
    window = RunWindow()
    anilist = Anilist(window.get_name())
    sort = Sorter(anilist.get_list())

    window.main_loop()

    # * Run Window
