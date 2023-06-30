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
        self.running = True
        self.image1 = None
        self.image2 = None

    def init_window(self):
        self.screen = self.display.set_mode((1280, 720))
        self.display.set_caption("Anilist Sorter")
        self.screen.fill(self.background_color)

        self.make_label(50, 50, 200, 100, sort.user)
        self.add_images()
        self.add_icon()

        self.initialized = True

    def add_icon(self):
        icon_image = Image.open(BytesIO(rq.get("https://i.imgur.com/9iPDCuY.png").content))
        icon_image_rgba = icon_image.convert("RGBA")
        image_data_rgba = icon_image_rgba.tobytes()
        image_data_size = icon_image_rgba.size
        new_icon = pygame.image.frombytes(image_data_rgba, image_data_size, "RGBA")
        self.display.set_icon(new_icon)

    def add_images(self):
        dict_iter = iter(sort.object_dict.values())

        self.image1 = pygame.image.load(BytesIO(rq.get(next(dict_iter).pic).content)).convert()
        self.image2 = pygame.image.load(BytesIO(rq.get(next(dict_iter).pic).content)).convert()


    def make_label(self, x, y, width, height, label):
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, width, height))
        font = pygame.font.SysFont("Arial", 24)
        text = font.render(label, True, self.text_color)
        text_rect = text.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text, text_rect)

    def main_loop(self):

        self.init_window()

        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if self.initialized:


                self.screen.blit(self.image1, (50, 150))
                self.screen.blit(self.image2, (200, 150))
                self.display.flip()

        pygame.quit()


if __name__ == '__main__':
    # * Inputs
    user_input = input("Enter Account name: ").strip()
    path = pathlib.Path("Users")
    user_list = list(filter(lambda p: p.is_file(), path.glob("*.txt")))
    #! Automatic input
    # sort = Sorter("Amvi", path, user_list)
    #! Manual input
    sort = Sorter(user_input, path, user_list)

    # * Lists
    char_list = sort.fetch()
    name_list = [char[0] for char in char_list]
    random_list = sample(name_list, len(name_list))
    # sorted_list = list(
    #    Sort.merge_sort(sample([char[0] for char in char_list], len([char[0] for char in char_list]))))

    #* Run Window

    window = RunWindow()
    window.main_loop()
