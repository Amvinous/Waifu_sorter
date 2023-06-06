import requests as rq
import json
import pathlib
from fuzzywuzzy import fuzz
import os
from random import sample


class Character:
    def __init__(self, name, pic, score=1):
        self.name = name
        self.pic = pic
        self.score = score


##
# * Retrieve information

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


##
# * Sends query to anilist if person not in memory
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


##
# * Sorting logic
def merge_sort(array):
    mid = len(array) // 2
    left = array[:mid]
    right = array[mid:]
    return merge(left, right)

            #merge_sort(left)
            #merge_sort(right)
def merge(left, right):
        left_index = right_index = 0
        result = []

        while left_index < len(left) and right_index < len(right):
            print(f'{left[left_index]} or {right[right_index]}')
            user_input = input("0 or 1")
            if user_input =='exit':
                return result
            elif int(user_input) == 0:
                result.append(left[left_index])
                left_index += 1
            elif int(user_input) == 1:
                result.append(right[right_index])
                right_index += 1

        return result


if __name__ == '__main__':
    user_input = input("Enter Account name: ").strip()
    username, char_list = fetch(user_input)
##
    object_dict = {char[0]: Character(char[0], char[1]) for char in char_list}
    name_list = [char[0] for char in char_list]
    random_list = sample(name_list, len(name_list))
    sorted_list = list(reversed(merge_sort(random_list)))
