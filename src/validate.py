import ast
from typing import Union


def can_parse(source: str) -> bool:
    """
    Return true if given string can be parsed as a python object
    """
    try:
        ast.parse(source)
        return True
    except SyntaxError:
        return False


def can_eval(source: str) -> bool:
    """
    Return true if given string can be evaluated as python code.py

    Parsing can miss RuntimeErrors so literal eval is also checkted
    """
    try:
        ast.literal_eval(source)
        return True
    except (SyntaxError, ValueError):
        return False


def make_dict(source: str) -> Union[dict, bool]:
    """
    Helper for creating dict from source string

    Return `False` if can't be evaluated as dict.
    """
    try:
        data = ast.literal_eval(source)
        assert isinstance(data, dict)
        return data
    except (SyntaxError, ValueError, AssertionError):
        return False
