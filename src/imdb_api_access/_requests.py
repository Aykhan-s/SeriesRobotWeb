from requests import get
from typing import (Union,
                    Dict)
from .exceptions import *


def get_request(url: str) -> Union[
        StatusCodeError,
        APIError,
        MaximumUsageError,
        InvalidAPIKey,
        Dict
    ]:

    raw_data = get(url, timeout=7)

    if raw_data.status_code != 200:
        raise StatusCodeError(raw_data.status_code)
    data = raw_data.json()

    if data['errorMessage']:
        if 'Maximum usage' in data['errorMessage']:
            raise MaximumUsageError(data['errorMessage'])

        elif 'Upgrade your account to use the service' in data['errorMessage']:
            raise InvalidAPIKey()

        raise APIError(data['errorMessage'])

    return data