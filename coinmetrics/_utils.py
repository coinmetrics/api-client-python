import pathlib
from datetime import datetime, date
from enum import Enum
from os.path import expanduser
from typing import Dict, AnyStr

import mmap

from coinmetrics._typing import FilePathOrBuffer, URL_PARAMS_TYPES


def transform_url_params_values_to_str(params: Dict[str, URL_PARAMS_TYPES]) -> Dict[str, str]:
    processed_params = {}
    for param_name, param_value in params.items():
        if param_value is None:
            continue
        if isinstance(param_value, (datetime, date)):
            if param_name.endswith('_time'):
                processed_params[param_name] = param_value.isoformat()
            else:
                raise ValueError('`{}` doesn\'t support {} objects'.format(param_name, type(param_value)))
        elif isinstance(param_value, (list, tuple)):
            processed_params[param_name] = ','.join(param_value)
        elif isinstance(param_value, Enum):
            processed_params[param_name] = param_value.value
        elif isinstance(param_value, bool):
            processed_params[param_name] = 'true' if param_value else 'false'
        else:
            processed_params[param_name] = str(param_value)
    return processed_params


def get_file_path_or_buffer(filepath_or_buffer: FilePathOrBuffer):
    if isinstance(filepath_or_buffer, (str, bytes, pathlib.Path)):
        return _stringify_path(filepath_or_buffer)

    if not _is_file_like(filepath_or_buffer):
        msg = 'Invalid file path or buffer object type: {}'.format(type(filepath_or_buffer))
        raise ValueError(msg)

    return filepath_or_buffer


def _stringify_path(
        filepath_or_buffer: FilePathOrBuffer[AnyStr],
) -> FilePathOrBuffer[AnyStr]:
    if hasattr(filepath_or_buffer, '__fspath__'):
        # https://github.com/python/mypy/issues/1424
        return filepath_or_buffer.__fspath__()  # type: ignore
    elif isinstance(filepath_or_buffer, pathlib.Path):
        return str(filepath_or_buffer)
    return _expand_user(filepath_or_buffer)


def _expand_user(
        filepath_or_buffer: FilePathOrBuffer[AnyStr],
) -> FilePathOrBuffer[AnyStr]:
    if isinstance(filepath_or_buffer, str):
        return expanduser(filepath_or_buffer)
    return filepath_or_buffer


def _is_file_like(obj) -> bool:
    if not (hasattr(obj, 'read') or hasattr(obj, 'write')):
        return False

    if not hasattr(obj, '__iter__'):
        return False

    return True
