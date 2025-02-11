from datetime import date, datetime
from pathlib import Path
from typing import Any, Callable, Dict, IO, List, Tuple, Union, Optional
from coinmetrics.constants import PagingFrom
from websocket import WebSocket
import pandas as pd
import polars as pl


DataFrameType = Union[pd.DataFrame, pl.DataFrame]
FilePathOrBuffer = Union[str, Path, IO[str], IO[bytes], None]
DataReturnType = Dict[str, Union[str, Dict[str, str], List[Dict[str, Any]]]]
DataRetrievalFuncType = Callable[[str, Dict[str, Any]], DataReturnType]
UrlParamTypes = Union[
    str, List[str], Tuple[str], PagingFrom, int, datetime, date, bool, None
]
MessageHandlerType = Optional[Callable[[WebSocket, Any], None]]
