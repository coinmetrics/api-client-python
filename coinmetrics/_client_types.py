from datetime import datetime, date
from typing import Callable, Any, Dict, List, Union, Tuple

from coinmetrics.constants import PagingFrom

DATA_RETURN_TYPE = Dict[str, Union[str, Dict[str, str], List[Dict[str, Any]]]]
DATA_RETRIEVAL_FUNC_TYPE = Callable[[str, Dict[str, Any]], DATA_RETURN_TYPE]

URL_PARAMS_TYPES = Union[str, List[str], Tuple[str], PagingFrom, int, datetime, date, bool, None]
