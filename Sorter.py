import requests as rq
import json
import os
import sys
from fuzzywuzzy import fuzz
from random import sample
import pathlib
from Character import Character

sys.tracebacklimit = 0


class MergeExitException(Exception):
    pass


class PersonNotFound(Exception):
    pass


class Sorter:
    def __init__(self, user_input, path, user_list):
        # * Retrieve information
        self.user_input = user_input
        self.path = path
        self.user_list = user_list

    # * Gets list from memory
    def get_list(self):
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
            "id": self.user_input,
            "page": 1
        }
        url = 'https://graphql.anilist.co'

        char_list = []

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
                char_list.append((name, pic, gender))

            if not data["pageInfo"]["hasNextPage"]:
                break
            else:
                variables["page"] += 1

        user = response["data"]["User"]["name"]
        new_user = open(self.path / f'{user}.txt', "w")
        new_user.write(json.dumps(char_list, indent=2))
        return user, char_list

    # * Searches memory
    def fetch(self):
        for user in self.user_list:
            username = os.path.splitext(user.name)[0]
            comparison = fuzz.partial_ratio(username, self.user_input)
            if comparison > 80:
                user_in_memory = open(user)
                char_list = json.load(user_in_memory)
                break
        else:
            print("User not in memory  \n Searching Anilist")
            username, char_list = self.get_list()
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
    user_input = input("Enter Account name: ").strip()
    path = pathlib.Path("Users")
    user_list = list(filter(lambda p: p.is_file(), path.glob("*.txt")))
    sort = Sorter(user_input, path, user_list)
    # * Lists
    username, char_list = sort.fetch()
    object_dict = {char[0]: Character(char[0], char[1], char[2]) for char in char_list}
