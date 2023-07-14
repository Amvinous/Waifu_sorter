# * Get list
import os
import json
import pathlib
import requests as rq
from fuzzywuzzy import fuzz
from PIL import Image

# * Sorting
import pygame
# from random import sample

# * My modules
from Character import Character
from Exceptions import *


class Sorter:
    def __init__(self, ):
        self.clock = None
        self.button1 = None
        self.button2 = None
        self.screen = None
        self.object_dict = None
        self.name_list = None
        self.char_list = []
        self.user = None
        self.path = pathlib.Path("Users")
        self.user_path = pathlib.Path()

        # ! Automatic input
        self.user_input = input("Enter Account name: ").strip()
        # ! Manual input
        # self.user_input = "Amvi"

        # + Searches each sub-folder in path for .txt and make a list of all users in storage
        self.user_list = list(filter(lambda p: p.is_file(), self.path.rglob("**/*.txt")))

    def download_image(self, file_name, url):
        response = rq.get(url)

        # + response code 200 is success
        if response.status_code == 200:
            with open(self.user_path / f'{file_name}.png', "wb") as file:
                picture = file.write(response.content)
            return picture

        else:
            raise ImagesDownloadFailed

    # * Requests a list from anilist
    def anilist_request(self):

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
            "id": self.user_input,
            "page": 1
        }
        url = 'https://graphql.anilist.co'

        while True:
            response = rq.post(url, json={'query': query, 'variables': variables}).json()

            if response["data"]["User"] is None:
                raise PersonNotFound

            data = response['data']["User"]["favourites"]["characters"]

            for character in data["nodes"]:
                name = character["name"]["full"]
                pic = character["image"]["medium"]
                gender = character["gender"]

                # ? add more attributes to the dictionary here and in class
                self.char_list.append([name, pic, gender])

            if not data["pageInfo"]["hasNextPage"]:
                break
            else:
                variables["page"] += 1

        # ! Can maybe redefine userpath to path

        user = response["data"]["User"]["name"]
        self.user = user
        self.user_path = self.path / f"{user}"
        self.user_path.mkdir(parents=True, exist_ok=True)

        # + Saves all information about each character in a .txt
        new_user = open(self.user_path / f'{user}.txt', "w")
        new_user.write(json.dumps(self.char_list, indent=2))
        print("Downloading images")

        # + Downloads images to a sub-folder of user
        for character in self.char_list:
            self.download_image(character[0], character[1])

        return response

    # * Gets list from memory

    def get_list(self):

        # + Checks if input is in memory
        for user in self.user_list:

            # + fuzzy searching
            username = os.path.splitext(user.name)[0]
            comparison = fuzz.partial_ratio(username, self.user_input)

            if comparison > 80:
                self.user = username
                user_in_memory = open(user)
                self.char_list = json.load(user_in_memory)
                break

        else:

            print("User not in memory  \n Searching Anilist")
            self.anilist_request()
            print("Found")

        # + Replaces picture url with a picture object
        for char in self.char_list:
            image = Image.open(self.path / self.user / f'{char[0]}.png')
            image_data = image.copy()
            char[1] = image_data

        # + Makes object dictionary with key as name and value object containing all information
        self.object_dict = {char[0]: Character(char[0], char[1], char[2]) for char in self.char_list}
        self.name_list = [char[0] for char in self.char_list]

    # * Sorting algorithm

    def merge_sort(self, char_list):

        if len(char_list) > 1:
            mid = len(char_list) // 2
            left = char_list[:mid]
            right = char_list[mid:]

            self.merge_sort(left)
            self.merge_sort(right)

            list_index = 0
            left_index = 0
            right_index = 0

            while left_index < len(left) and right_index < len(right):

                print(left[left_index], right[right_index])

                self.clock.tick(5)
                self.button1.is_clicked = False
                self.button2.is_clicked = False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.button1.click(event.pos)
                        self.button2.click(event.pos)

                self.button1.draw(self.screen)
                self.button2.draw(self.screen)

                pygame.display.flip()

                if self.button1.is_clicked:
                    char_list[list_index] = left[left_index]
                    left_index += 1
                    list_index += 1

                elif self.button2.is_clicked:
                    char_list[list_index] = right[right_index]
                    right_index += 1
                    list_index += 1

            # + Not discard the non-picked value
            while left_index < len(left):
                char_list[list_index] = left[left_index]
                left_index += 1
                list_index += 1

            while right_index < len(right):
                char_list[list_index] = right[right_index]
                right_index += 1
                list_index += 1

            return char_list

    # * Sorting
    def sorting(self, clock, screen, button1, button2):
        self.clock = clock
        self.screen = screen
        self.button1 = button1
        self.button2 = button2
        # ! add sample
        # ! Maybe replace this with object_dict and make name_list not needed
        self.name_list = self.merge_sort(self.name_list)


"""
if __name__ == '__main__':
    # * Inputs
    user_input = input("Enter Account name: ").strip()
    user_path = pathlib.Path("Users")
    user_list = list(filter(lambda p: p.is_file(), user_path.rglob("**/*.txt")))
    sort = Sorter(user_input, user_path, user_list)
    # * Lists
    sort.fetch()
    
    sort = Sorter()
"""
