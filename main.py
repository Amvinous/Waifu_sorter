import requests as rq
import json
import pathlib
from fuzzywuzzy import fuzz
import os


class Character:
    def __init__(self, name, pic, score=1):
        self.name = name
        self.pic = pic
        self.score = score


# Inputs
path = pathlib.Path("Users")
user_list = list(filter(lambda p: p.is_file(), path.glob("*.txt")))


def get_list(user_input):
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
            # ? add more attributes to the dictionary here and in class
            char_list.append((name, pic))

        if not data["pageInfo"]["hasNextPage"]:
            break
        else:
            variables["page"] += 1

    user = response["data"]["User"]["name"]
    new_user = open(path / f'{user}.txt', "w")
    new_user.write(json.dumps(char_list, indent=2))
    return user, char_list


#
def fetch(user_input: str):
    for user in user_list:
        username = os.path.splitext(user.name)[0]
        comparison = fuzz.partial_ratio(username, user_input)
        if comparison > 80:
            f = open(user)
            char_list = json.load(f)
            break
    else:
        print("User not in memory  \n Searching Anilist")
        username, char_list = get_list(user_input)
        print("Found")
    return username, char_list


def merge_sort(array):
    while len(array) > 1:
        mid = len(array) // 2
        left = array[:mid]
        right = array[mid:]

        merge_sort(left)
        merge_sort(right)

        left_index = right_index = array_index = 0

        while left_index < len(left) and right_index < len(right):
            print(left[left_index][0], right[right_index][0])
            user_input = input("0 or 1")
            if user_input == 0:
                array[array_index] = left[left_index]
                left_index += 1
            else:
                array[array_index] = right[right_index]
                right_index += 1
            array_index += 1

        while left_index < len(left):
            array[array_index] = left[left_index]
            left_index += 1
            array_index += 1

        while right_index < len(right):
            array[array_index] = right[right_index]
            right_index += 1
            array_index += 1

        sorted_list = left+right
        return sorted_list


if __name__ == '__main__':
    user_input = input("Enter Account name: ").strip()
    username, char_list = fetch(user_input)

    object_dict = {char[0]: Character(char[0], char[1]) for char in char_list}

    sorted_list = reversed(merge_sort(char_list))

