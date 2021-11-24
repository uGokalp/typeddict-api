from pydantic import BaseModel, validator
from typing_extensions import Literal

from src.validate import can_eval, can_parse, make_dict

parsing_error_message = "Cannot parse the given input"
evaluating_error_message = "Cannot evaluate the given input"
dict_error_message = "Input is not a dictionary"


class ValidCode(BaseModel):
    """
    Represents a valid code string that can be parsed and interpreted
    """

    code: str

    @validator("code")
    def must_parse(cls, v: str):
        assert can_parse(v), parsing_error_message
        assert can_eval(v), evaluating_error_message
        return v


class DictCode(ValidCode):
    """
    Represents a valid code that can be interpreted as a dictionary
    """

    code: str

    @validator("code")
    def is_dict(cls, v: str):
        assert isinstance(make_dict(v), dict), dict_error_message
        return v

    @property
    def data(self):
        return make_dict(self.code)


class Success(BaseModel):
    """`Success` model that each request takes the shape"""

    data: str
    success: Literal[True] = True
