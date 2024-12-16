import pathlib
from datetime import date, datetime, timezone
from enum import Enum
from functools import wraps
from logging import getLogger
from os.path import expanduser
from time import sleep
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, Set
from coinmetrics._typing import FilePathOrBuffer, UrlParamTypes
from pandas import Timestamp

logger = getLogger("cm_client_utils")


def transform_url_params_values_to_str(
    params: Dict[str, UrlParamTypes]
) -> Dict[str, str]:
    processed_params = {}
    for param_name, param_value in params.items():
        if param_value is None:
            continue
        if isinstance(param_value, (datetime, date, Timestamp)):
            if isinstance(param_value, Timestamp):
                param_value = param_value.to_pydatetime()

            if isinstance(param_value, datetime):
                param_value = param_value.astimezone(timezone.utc).replace(tzinfo=None)

            if isinstance(param_value, date) and not isinstance(param_value, datetime):
                param_value = datetime(param_value.year, param_value.month, param_value.day)

            assert isinstance(param_value, datetime)
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


def get_keys_from_catalog(d: Dict[str, str]) -> Set[str]:
    keys = []
    for k, v in d.items():
        if isinstance(v, list):
            for nested_dict in v:
                keys.extend(get_keys_from_catalog(nested_dict))
        else:
            keys.append(k)
    return set(keys)


def deprecated(endpoint: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        message = f"Function {func.__name__} is deprecated. "
        if endpoint == 'catalog':
            message += "Use 'catalog-v2' and 'reference-data' instead. For more information, see: https://docs.coinmetrics.io/tutorials-and-examples/user-guides/how-to-migrate-from-catalog-v1-to-catalog-v2 "
            message += "\nNote: markets are truncated to 170,000 entries. Data may be out of date."

        docstring = func.__doc__ or ""
        deprecation_note = f"\n\nDeprecated: {message}\n"
        func.__doc__ = deprecation_note + docstring

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.warning(message)
            return func(*args, **kwargs)

        return wrapper

    return decorator
