# * imports
import requests as rq
import pathlib
# * images
from PIL import Image
from io import BytesIO
# * pygame
import pygame
from Character import Character
from Sorter import Sorter
from random import sample

if __name__ == '__main__':
    # * Inputs
    user_input = input("Enter Account name: ").strip()
    path = pathlib.Path("Users")
    user_list = list(filter(lambda p: p.is_file(), path.glob("*.txt")))
    # Sort = Sorter("Amvi", path, user_list)
    Sort = Sorter(user_input, path, user_list)
    # * Lists
    username, char_list = Sort.fetch(Sort.user_input)
    object_dict = {char[0]: Character(char[0], char[1], char[2]) for char in char_list}
    name_list = [char[0] for char in char_list]
    random_list = sample(name_list, len(name_list))
    #sorted_list = list(
    #    Sort.merge_sort(sample([char[0] for char in char_list], len([char[0] for char in char_list]))))

# ? pygame

# ? Configure window

display = pygame.display
background_color = (30, 30, 30)
screen = display.set_mode((1280, 720))
display.set_caption("Anilist Sorter")

# ? add icon

icon_image = Image.open(BytesIO(rq.get("https://i.imgur.com/9iPDCuY.png").content))
icon_image_rgba = icon_image.convert("RGBA")
image_data_rgba = icon_image_rgba.tobytes()
image_data_size = icon_image_rgba.size
new_icon = pygame.image.fromstring(image_data_rgba, icon_image.size, "RGBA")
display.set_icon(new_icon)

# ? add images

image1 = pygame.image.load(BytesIO(rq.get(object_dict["Miku Nakano"].pic).content)).convert()
image2 = pygame.image.load(BytesIO(rq.get(object_dict["Kana Arima"].pic).content)).convert()

# ? loop

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color)

    screen.blit(image1, (50, 50))
    screen.blit(image2, (200, 50))
    display.flip()

pygame.quit()
