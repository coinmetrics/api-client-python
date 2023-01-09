from typing import Dict, List, Any
from requests import HTTPError, Response
from urllib.parse import urlparse, parse_qs
from functools import reduce


class CoinMetricsClientQueryParamsException(HTTPError):
    """
    Raised when a request is made that will return an error due to the logic or contents of the request
    """

    def __init__(self, response: Response, *args: Any, **kwargs: Any):
        if response.status_code != 414:
            response.raise_for_status()
        parsed_query_params: Dict[str, List[str]] = parse_qs(
            str(urlparse(url=response.request.url).query)
        )
        get_sum_of_lengths = lambda strings: reduce(lambda a, b: a + len(b), strings, 0)
        param_length_dict = {"Total characters": 0}
        for param, values in parsed_query_params.items():
            sum_of_param_lengths = get_sum_of_lengths(values)
            param_length_dict[param] = sum_of_param_lengths
            param_length_dict["Total characters"] += sum_of_param_lengths
        exception_message = (
            "This request failed because the request URL is too long, consider reducing the length "
            f"of the params.\n 414 errors may get returned as total characters in query params exceed 5000"
            f"\nLength of the params provided for reference:\n {param_length_dict}"
        )
        self.msg = exception_message
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return self.msg