from pydantic import BaseSettings


class Config(BaseSettings):
    title: str = "TypedDict API"
    description: str = (
        "This API is used for generating TypedDict class from dictionaries"
    )
