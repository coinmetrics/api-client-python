from datetime import datetime, date
from enum import Enum
from typing import Dict

from coinmetrics._client_types import URL_PARAMS_TYPES


def transform_url_params_values_to_str(params: Dict[str, URL_PARAMS_TYPES]) -> Dict[str, str]:
    processed_params = {}
    for param_name, param_value in params.items():
        if param_value is None:
            continue
        if isinstance(param_value, (datetime, date)):
            if param_name.endswith('_time'):
                processed_params[param_name] = param_value.isoformat()
            else:
                raise ValueError(f'`{param_name}` doesn\'t support {type(param_value)} objects')
        elif isinstance(param_value, (list, tuple)):
            processed_params[param_name] = ','.join(param_value)
        elif isinstance(param_value, Enum):
            processed_params[param_name] = param_value.value
        elif isinstance(param_value, bool):
            processed_params[param_name] = 'true' if param_value else 'false'
        else:
            processed_params[param_name] = str(param_value)
    return processed_params
