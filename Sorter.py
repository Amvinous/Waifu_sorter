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

from enum import Enum


class Selection(Enum):
    LEFT = 0
    RIGHT = 1


class Sorter:
    def __init__(self, ):
        self.button = None
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

    def select(self, selection: Selection):
        self.button = selection

    def merge_sort(self, _name_list=None):

        if _name_list is None:
            _name_list = self.name_list

        if len(_name_list) > 1:
            mid = len(_name_list) // 2
            left = _name_list[:mid]
            right = _name_list[mid:]

            yield from self.merge_sort(left)
            yield from self.merge_sort(right)

            list_index = 0
            left_index = 0
            right_index = 0

            while left_index < len(left) and right_index < len(right):

                yield [left[left_index], right[right_index]]
                match self.button:
                    case Selection.LEFT:
                        _name_list[list_index] = left[left_index]
                        left_index += 1
                        list_index += 1
                    case Selection.RIGHT:
                        _name_list[list_index] = right[right_index]
                        right_index += 1
                        list_index += 1

            # + Not discard the non-picked value
            while left_index < len(left):
                _name_list[list_index] = left[left_index]
                left_index += 1
                list_index += 1

            while right_index < len(right):
                _name_list[list_index] = right[right_index]
                right_index += 1
                list_index += 1

            return _name_list

        # ! add random.sample
        # ! Maybe replace this with object_dict and make name_list not needed
