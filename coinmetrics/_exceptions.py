from typing import Dict, List, Any
from requests import HTTPError, Response
from urllib.parse import urlparse, parse_qs
from functools import reduce


class CoinMetricsClientNotFoundError(Exception):
    """Raised when a CoinMetricsClient instance is not found."""
    def __init__(self, message="CoinMetricsClient not found"):
        self.message = message
        super().__init__(self.message)


class CoinMetricsClientBadParameterError(HTTPError):
    """
    Raised when a request is made with bad parameters (HTTP 400).
    """
    def __init__(self, response: Response, *args: Any, **kwargs: Any):
        if response.status_code != 400:
            response.raise_for_status()
        self.response = response
        self.request = response.request
        error_message = "Bad Parameter: The request contains invalid parameters."
        self.msg = error_message
        super().__init__(response=response, request=response.request, *args, **kwargs)

    def __str__(self) -> str:
        return self.msg


class CoinMetricsClientUnauthorizedError(HTTPError):
    """
    Raised when a request is unauthorized due to invalid or missing API key (HTTP 401).
    """
    def __init__(self, response: Response, *args: Any, **kwargs: Any):
        if response.status_code != 401:
            response.raise_for_status()
        self.response = response
        self.request = response.request
        error_message = "Unauthorized: The API key is invalid or missing."
        self.msg = error_message
        super().__init__(response=response, request=response.request, *args, **kwargs)

    def __str__(self) -> str:
        return self.msg


class CoinMetricsClientForbiddenError(HTTPError):
    """
    Raised when a request is forbidden due to insufficient permissions (HTTP 403).
    """
    def __init__(self, response: Response, *args: Any, **kwargs: Any):
        if response.status_code != 403:
            response.raise_for_status()
        self.response = response
        self.request = response.request
        error_message = "Forbidden: The API key does not have permission to access this resource."
        self.msg = error_message
        super().__init__(response=response, request=response.request, *args, **kwargs)

    def __str__(self) -> str:
        return self.msg


