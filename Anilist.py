# * Get list
import io
import json
import os
import pathlib

import requests as rq
from PIL import Image
from fuzzywuzzy import fuzz

# * My modules
from Character import Character
from Exceptions import *


class Anilist:
    def __init__(self):
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

        # ! Add id of characters and user and use that instead

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
                              large
                            }
                            gender
                            id
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
                pic = character["image"]["large"]
                gender = character["gender"]
                char_id = character["id"]

                # ? add more attributes to the dictionary here and in class
                self.char_list.append([name, pic, gender, char_id])

            if not data["pageInfo"]["hasNextPage"]:
                break
            else:
                variables["page"] += 1

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

            if comparison > 70:
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
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="png")
            image_bytes.seek(0)
            char[1] = image_bytes.getvalue()

        # + Makes object dictionary with key as name and value object containing all information
        """
        self.object_dict = {char[0]: Character(
            name=char[0], pic=char[1], gender=char[2], id=char[3]) for char in
            self.char_list}
        """
        self.object_dict = [Character(
            name=char[0], pic=char[1], gender=char[2], id=char[3]) for char in
            self.char_list]
        return self.object_dict
