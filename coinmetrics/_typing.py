from datetime import datetime, date
from pathlib import Path
from typing import Union, IO, AnyStr, Dict, List, Any, Callable, Tuple

from coinmetrics.constants import PagingFrom

FilePathOrBuffer = Union[str, Path, IO[AnyStr]]
DataReturnType = Dict[str, Union[str, Dict[str, str], List[Dict[str, Any]]]]
DataRetrievalFuncType = Callable[[str, Dict[str, Any]], DataReturnType]
UrlParamTypes = Union[
    str, List[str], Tuple[str], PagingFrom, int, datetime, date, bool, None
]
