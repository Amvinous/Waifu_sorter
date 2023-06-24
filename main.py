# * imports
import requests as rq
import json
import pathlib
import os
from fuzzywuzzy import fuzz
from random import sample
from PIL import Image
from io import BytesIO
# * pygame
import pygame


class Character:
    def __init__(self, name, pic, gender):
        self.name = name
        self.pic = pic
        self.gender = gender


class MergeExitException(Exception):
    pass


##
class Sorter:
    def __init__(self, user_input, path, user_list):
        # * Retrieve information
        self.user_input = user_input
        self.path = path
        self.user_list = user_list

    # * Gets list from memory
    def get_list(self, user_input):
        # ?returns 2 variables
        query = """
    query ($id: String, $page: Int){
                User(search: $id){
                    name
                    favourites {
                        characters (page : $page){
                            pageInfo{
                            hasNextPage
                        }
                        nodes {
                            name {
                              full
                            }
                            image {
                              medium
                            }
                            gender
                        }
                    }
                }
            }
        }
        """

        variables = {
            "id": user_input,
            "page": 1
        }
        url = 'https://graphql.anilist.co'

        char_list = []

        while True:
            response = rq.post(url, json={'query': query, 'variables': variables}).json()
            data = response['data']["User"]["favourites"]["characters"]

            for character in data["nodes"]:
                name = character["name"]["full"]
                pic = character["image"]["medium"]
                gender = character["gender"]

                # ? add more attributes to the dictionary here and in class
                char_list.append((name, pic, gender))

            if not data["pageInfo"]["hasNextPage"]:
                break
            else:
                variables["page"] += 1

        user = response["data"]["User"]["name"]
        new_user = open(path / f'{user}.txt', "w")
        new_user.write(json.dumps(char_list, indent=2))
        return user, char_list

    # * Searches memory
    def fetch(self, user_input: str):
        for user in user_list:
            username = os.path.splitext(user.name)[0]
            comparison = fuzz.partial_ratio(username, user_input)
            if comparison > 80:
                f = open(user)
                char_list = json.load(f)
                break
        else:
            print("User not in memory  \n Searching Anilist")
            username, char_list = self.get_list(user_input)
            print("Found")
        return username, char_list

    # * Sorting
    def merge_sort(self, array):
        if len(array) < 2:
            return array
        mid = len(array) // 2
        left = self.merge_sort(array[:mid])
        right = self.merge_sort(array[mid:])

        if left is None or right is None:
            return None
        return self.merge(left, right)

    def merge(self, left, right):
        if not len(left) or not len(right):
            return left or right
        left_index, right_index = 0, 0
        result = []

        while len(result) < len(left) + len(right):
            print(f'{left[left_index]} or {right[right_index]}')
            user_input = input("0 or 1")
            if user_input == 'exit':
                raise MergeExitException
            elif int(user_input) == 0:
                result.append(left[left_index])
                left_index += 1
            elif int(user_input) == 1:
                result.append(right[right_index])
                right_index += 1
            if left_index == len(left) or right_index == len(right):
                result.extend(left[left_index:] or right[right_index:])
                break
        return result


if __name__ == '__main__':
    # * Inputs
    # user_input = input("Enter Account name: ").strip()
    path = pathlib.Path("Users")
    user_list = list(filter(lambda p: p.is_file(), path.glob("*.txt")))
    Sort = Sorter("Amvi", path, user_list)
    # Sort = Sorter(user_input, path, user_list)
    # * Lists
    username, char_list = Sort.fetch(Sort.user_input)
    object_dict = {char[0]: Character(char[0], char[1], char[2]) for char in char_list}

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

image1 = pygame.image.load(BytesIO(rq.get(object_dict["Miku Nakano"].pic).content))
image2 = pygame.image.load(BytesIO(rq.get(object_dict["Kana Arima"].pic).content))

# ? loop

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

    screen.fill(background_color)

    screen.blit(image1, (50, 50))
    screen.blit(image2, (200, 50))
    pygame.display.update()

pygame.quit()
