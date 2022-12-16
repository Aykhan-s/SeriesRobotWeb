from typing import Union


class StatusCodeError(Exception):
    def __init__(self, status_code: Union[int, str] = 404) -> None:
        self.status_code = status_code

    def __str__(self) -> str:
        return f"request response status code: {self.status_code}"

class APIError(Exception):
    def __init__(self, message: str = 'Unknown Error') -> None:
        self.message = message

    def __str__(self) -> str:
        return f"IMDB API: {self.message}"

class MaximumUsageError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self) -> str:
        return f"IMDB API: {self.message}"