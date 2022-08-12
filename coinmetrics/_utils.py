import pathlib
from datetime import date, datetime
from enum import Enum
from functools import wraps
from logging import getLogger
from os.path import expanduser
from time import sleep
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from coinmetrics._typing import FilePathOrBuffer, UrlParamTypes

logger = getLogger("cm_client_utils")


def transform_url_params_values_to_str(
    params: Dict[str, UrlParamTypes]
) -> Dict[str, str]:
    processed_params = {}
    for param_name, param_value in params.items():
        if param_value is None:
            continue
        if isinstance(param_value, (datetime, date)):
            if param_name.endswith("_time"):
                processed_params[param_name] = param_value.isoformat()
            else:
                raise ValueError(
                    "`{}` doesn't support {} objects".format(
                        param_name, type(param_value)
                    )
                )
        elif isinstance(param_value, (list, tuple)):
            processed_params[param_name] = ",".join(param_value)
        elif isinstance(param_value, Enum):
            processed_params[param_name] = param_value.value
        elif isinstance(param_value, bool):
            processed_params[param_name] = "true" if param_value else "false"
        else:
            processed_params[param_name] = str(param_value)
    return processed_params


def get_file_path_or_buffer(filepath_or_buffer: FilePathOrBuffer) -> FilePathOrBuffer:
    if isinstance(filepath_or_buffer, (str, bytes, pathlib.Path)):
        return _stringify_path(filepath_or_buffer)

    if not _is_file_like(filepath_or_buffer):
        msg = "Invalid file path or buffer object type: {}".format(
            type(filepath_or_buffer)
        )
        raise ValueError(msg)

    return filepath_or_buffer


def _stringify_path(filepath_or_buffer: FilePathOrBuffer) -> FilePathOrBuffer:
    if hasattr(filepath_or_buffer, "__fspath__"):
        # https://github.com/python/mypy/issues/1424
        return filepath_or_buffer.__fspath__()  # type: ignore
    elif isinstance(filepath_or_buffer, pathlib.Path):
        return str(filepath_or_buffer)
    return _expand_user(filepath_or_buffer)


def _expand_user(
    filepath_or_buffer: FilePathOrBuffer,
) -> FilePathOrBuffer:
    if isinstance(filepath_or_buffer, str):
        return expanduser(filepath_or_buffer)
    return filepath_or_buffer


def _is_file_like(obj: Any) -> bool:
    if not (hasattr(obj, "read") or hasattr(obj, "write")):
        return False

    if not hasattr(obj, "__iter__"):
        return False

    return True


def retry(
    error_cls: Union[List[Any], Tuple[Any], Any],
    retries: int = 5,
    wait_time_between_retries: int = 30,
    message: Optional[str] = None,
    fail: bool = True,
    error_str: Optional[str] = None,
) -> Callable[..., Any]:
    def retry_wrapper(f: Any) -> Any:
        @wraps(f)
        def wrapper(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
            for n in range(1, retries + 1):
                try:
                    return f(*args, **kwargs)
                except error_cls as error:  # type: ignore
                    if (
                        n == retries
                        or (error_str is not None and error_str not in str(error))
                    ) and fail:
                        raise
                    if callable(wait_time_between_retries):
                        wait_time = wait_time_between_retries()
                    else:
                        wait_time = wait_time_between_retries
                    if message:
                        logger.info(
                            "%s. Retrying in: %s sec. Iteration: %s",
                            message,
                            wait_time,
                            n,
                        )

                    sleep(wait_time)

        return wrapper

    return retry_wrapper
