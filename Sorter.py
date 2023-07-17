# from random import sample
from enum import Enum


class Selection(Enum):
    LEFT = 0
    RIGHT = 1


class Sorter:
    def __init__(self, character_list: list):
        self.button = None
        self.character_list = character_list

    # * Sorting algorithm

    # ! add random.sample
    # ! Maybe replace this with object_dict and make name_list not needed
    # ! implement slicing of dictionaries and id

    def select(self, selection: Selection):
        self.button = selection

    def merge_sort(self, _character_list=None):

        if _character_list is None:
            _character_list = self.character_list

        if len(_character_list) > 1:
            mid = len(_character_list) // 2
            left = _character_list[:mid]
            right = _character_list[mid:]

            yield from self.merge_sort(left)
            yield from self.merge_sort(right)

            list_index = 0
            left_index = 0
            right_index = 0

            while left_index < len(left) and right_index < len(right):

                yield [left[left_index], right[right_index]]
                match self.button:
                    case Selection.LEFT:
                        _character_list[list_index] = left[left_index]
                        left_index += 1
                        list_index += 1
                    case Selection.RIGHT:
                        _character_list[list_index] = right[right_index]
                        right_index += 1
                        list_index += 1

            # + Not discard the non-picked value
            while left_index < len(left):
                _character_list[list_index] = left[left_index]
                left_index += 1
                list_index += 1

            while right_index < len(right):
                _character_list[list_index] = right[right_index]
                right_index += 1
                list_index += 1

            return _character_list
