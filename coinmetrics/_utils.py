import pathlib
import warnings
from datetime import date, datetime, timezone
from enum import Enum
from functools import wraps
from logging import getLogger
from os.path import expanduser
from time import sleep
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, Set, Type
from coinmetrics._typing import FilePathOrBuffer, UrlParamTypes
from pandas import Timestamp
import polars as pl
import pandas as pd

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
                if param_value.tzinfo is not None:
                    param_value = param_value.astimezone(timezone.utc)
                param_value = param_value.replace(tzinfo=None)

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
    exponential_backoff: bool = True,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
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
                    elif exponential_backoff:
                        # Calculate exponential backoff with jitter
                        import random
                        delay = min(base_delay * (2 ** (n - 1)), max_delay)
                        jitter = random.uniform(0, 0.1) * delay
                        wait_time = delay + jitter
                    else:
                        wait_time = wait_time_between_retries

                    if message:
                        logger.info(
                            "%s. Retrying in: %.2f sec. Iteration: %s",
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


def deprecated_optimize_pandas_types(func: Callable[..., Any]) -> Callable[..., Any]:
    """Warn on deprecated named argument"""
    @wraps(func)
    def decorator(*args: Any, **kwargs: Any) -> Any:
        if "optimize_pandas_types" in kwargs:
            logger.warning(
                f"Function {func.__name__} argument 'optimize_pandas_types' "
                "is deprecated. Use 'optimize_dtypes' instead."
            )
            if "optimize_dtypes" not in kwargs:
                kwargs["optimize_dtypes"] = kwargs["optimize_pandas_types"]
            del kwargs["optimize_pandas_types"]
        return func(*args, **kwargs)

    return decorator


PANDAS_TO_POLARS_DTYPE_MAP: Dict[str, pl.DataType] = {
    # Numeric types
    'int8': pl.Int8(),
    'int16': pl.Int16(),
    'int32': pl.Int32(),
    'int64': pl.Int64(),
    'uint8': pl.UInt8(),
    'uint16': pl.UInt16(),
    'uint32': pl.UInt32(),
    'uint64': pl.UInt64(),
    'float32': pl.Float32(),
    'float64': pl.Float64(),
    'Int8': pl.Int8(),
    'Int16': pl.Int16(),
    'Int32': pl.Int32(),
    'Int64': pl.Int64(),
    'UInt8': pl.UInt8(),
    'UInt16': pl.UInt16(),
    'UInt32': pl.UInt32(),
    'UInt64': pl.UInt64(),
    'Float32': pl.Float32(),
    'Float64': pl.Float64(),

    # Boolean
    'bool': pl.Boolean(),
    'boolean': pl.Boolean(),

    # String/Object types
    'object': pl.String(),
    'string': pl.String(),

    # DateTime types
    'datetime64[ns]': pl.Datetime(),
    'datetime64[ms]': pl.Datetime('ms'),
    'datetime64[us]': pl.Datetime('us'),
    'datetime64[ns, UTC]': pl.Datetime('ns', time_zone='UTC'),
    'datetime64[ms, UTC]': pl.Datetime('ms', time_zone='UTC'),
    'datetime64[us, UTC]': pl.Datetime('us', time_zone='UTC'),

    # Categorical
    'category': pl.Categorical(),
    'categorical': pl.Categorical(),

    # Date
    'date': pl.Date(),

    # Time
    'time': pl.Time(),

    # Null type
    'null': pl.Null(),
}


def convert_pandas_dtype_to_polars(pandas_dtype: Union[str, pd.api.types.CategoricalDtype]) -> pl.DataType:
    """
    Convert a pandas dtype to its equivalent Polars dtype.

    Parameters
    ----------
    pandas_dtype : str or CategoricalDtype
        The pandas dtype to convert. Can be a string representation or a pandas dtype object.

    Returns
    -------
    pl.DataType
        The equivalent Polars dtype.

    Examples
    --------
    >>> convert_pandas_dtype_to_polars('int64')
    <class 'polars.datatypes.Int64'>
    >>> convert_pandas_dtype_to_polars('object')
    <class 'polars.datatypes.String'>

    Raises
    ------
    ValueError
        If the pandas dtype has no direct equivalent in Polars.
    """
    dtype_str = str(pandas_dtype)

    if isinstance(pandas_dtype, pd.api.types.CategoricalDtype):
        return pl.Categorical()

    dtype_str = dtype_str.replace('numpy.', '').replace('pandas.', '')

    polars_dtype = PANDAS_TO_POLARS_DTYPE_MAP.get(dtype_str)

    if polars_dtype is None:
        raise ValueError(f"No direct Polars equivalent found for pandas dtype: {dtype_str}")

    return polars_dtype


# =============================================================================
# Function Alias Utilities
# =============================================================================

def alias(
    canonical_name: str,
    warning_message: Optional[str] = None,
    category: Type[Warning] = DeprecationWarning,
    stacklevel: int = 2
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Create a function alias that routes to a canonical function with a deprecation warning.

    Parameters
    ----------
    canonical_name : str
        The canonical name of the function this alias should route to.
    warning_message : str, optional
        Custom warning message. If None, a default message will be generated.
    category : Type[Warning], default DeprecationWarning
        The warning category to use.
    stacklevel : int, default 2
        The stack level for the warning (how many frames up to show in traceback).

    Returns
    -------
    Callable
        A decorator that creates the alias function.

    Examples
    --------
    >>> class MyClass:
    ...     def get_data(self):
    ...         return "data"
    ...
    ...     @alias("get_data")
    ...     def data(self):
    ...         return self.get_data()

    When `data()` is called, it will route to `get_data()` and show a deprecation warning.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        # Generate warning message if not provided
        msg = warning_message
        if msg is None:
            msg = (
                f"Function '{func.__name__}' is deprecated and will be removed in a future version. "
                f"Please use '{canonical_name}' instead."
            )

        # Update docstring to include deprecation notice
        original_doc = func.__doc__ or ""
        deprecation_note = f"\n\n.. deprecated::\n   Use :meth:`{canonical_name}` instead.\n"
        func.__doc__ = original_doc + deprecation_note

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Issue the deprecation warning
            warnings.warn(
                msg,
                category=category,
                stacklevel=stacklevel
            )

            # Log the warning as well
            logger.warning(
                f"Deprecated function '{func.__name__}' called. "
                f"Please use '{canonical_name}' instead."
            )

            # Call the original function
            return func(*args, **kwargs)

        # Mark the wrapper as an alias
        setattr(wrapper, '_is_alias', True)
        setattr(wrapper, '_canonical_name', canonical_name)
        setattr(wrapper, '_original_func', func)

        return wrapper

    return decorator


class AliasManager:
    """
    Manager class for handling function aliases in a class.

    This class provides methods to create, manage, and validate function aliases
    within a class context.
    """

    def __init__(self, target_class: Type[Any]) -> None:
        """
        Initialize the alias manager for a target class.

        Parameters
        ----------
        target_class : Type[Any]
            The class to manage aliases for.
        """
        self.target_class = target_class
        self._aliases: Dict[str, str] = {}
        self._reverse_aliases: Dict[str, str] = {}

    def add_alias(self, alias_name: str, canonical_name: str) -> None:
        """
        Add an alias mapping.

        Parameters
        ----------
        alias_name : str
            The alias function name.
        canonical_name : str
            The canonical function name.
        """
        self._aliases[alias_name] = canonical_name
        self._reverse_aliases[canonical_name] = alias_name

    def get_canonical_name(self, alias_name: str) -> Optional[str]:
        """
        Get the canonical name for an alias.

        Parameters
        ----------
        alias_name : str
            The alias function name.

        Returns
        -------
        Optional[str]
            The canonical name if the alias exists, None otherwise.
        """
        return self._aliases.get(alias_name)

    def get_aliases(self, canonical_name: str) -> list[str]:
        """
        Get all aliases for a canonical function name.

        Parameters
        ----------
        canonical_name : str
            The canonical function name.

        Returns
        -------
        list[str]
            List of alias names for the canonical function.
        """
        return [alias for alias, canonical in self._aliases.items()
                if canonical == canonical_name]

    def create_alias_method(self, alias_name: str, canonical_name: str) -> Callable[..., Any]:
        """
        Create an alias method that routes to the canonical method.

        Parameters
        ----------
        alias_name : str
            The alias method name.
        canonical_name : str
            The canonical method name.

        Returns
        -------
        Callable
            The alias method.
        """
        def alias_method(self: Any, *args: Any, **kwargs: Any) -> Any:
            # Get the canonical method
            canonical_method = getattr(self, canonical_name, None)
            if canonical_method is None:
                raise AttributeError(
                    f"Canonical method '{canonical_name}' not found for alias '{alias_name}'"
                )

            # Issue deprecation warning
            warning_message = (
                f"Method '{alias_name}' is deprecated and will be removed in a future version. "
                f"Please use '{canonical_name}' instead."
            )
            warnings.warn(warning_message, DeprecationWarning, stacklevel=2)
            logger.warning(f"Deprecated method '{alias_name}' called. Use '{canonical_name}' instead.")

            # Call the canonical method
            return canonical_method(*args, **kwargs)

        # Set method attributes
        alias_method.__name__ = alias_name
        alias_method.__qualname__ = f"{self.target_class.__name__}.{alias_name}"
        setattr(alias_method, '_is_alias', True)
        setattr(alias_method, '_canonical_name', canonical_name)

        # Add to aliases
        self.add_alias(alias_name, canonical_name)

        return alias_method

    def apply_aliases(self) -> None:
        """
        Apply all registered aliases to the target class.

        This method should be called after all aliases have been registered.
        """
        for alias_name, canonical_name in self._aliases.items():
            if hasattr(self.target_class, canonical_name):
                alias_method = self.create_alias_method(alias_name, canonical_name)
                setattr(self.target_class, alias_name, alias_method)
            else:
                logger.warning(
                    f"Cannot create alias '{alias_name}' for '{canonical_name}': "
                    f"canonical method not found in {self.target_class.__name__}"
                )


def create_function_alias(
    canonical_func: Callable[..., Any],
    alias_name: str,
    warning_message: Optional[str] = None
) -> Callable[..., Any]:
    """
    Create a standalone function alias.

    Parameters
    ----------
    canonical_func : Callable
        The canonical function to alias.
    alias_name : str
        The name for the alias function.
    warning_message : str, optional
        Custom warning message.

    Returns
    -------
    Callable
        The alias function.
    """
    if warning_message is None:
        warning_message = (
            f"Function '{alias_name}' is deprecated and will be removed in a future version. "
            f"Please use '{canonical_func.__name__}' instead."
        )

    @wraps(canonical_func)
    def alias_func(*args: Any, **kwargs: Any) -> Any:
        warnings.warn(warning_message, DeprecationWarning, stacklevel=2)
        logger.warning(f"Deprecated function '{alias_name}' called. Use '{canonical_func.__name__}' instead.")
        return canonical_func(*args, **kwargs)

    alias_func.__name__ = alias_name
    setattr(alias_func, '_is_alias', True)
    setattr(alias_func, '_canonical_name', canonical_func.__name__)

    return alias_func


def is_alias(func: Callable[..., Any]) -> bool:
    """
    Check if a function is an alias.

    Parameters
    ----------
    func : Callable
        The function to check.

    Returns
    -------
    bool
        True if the function is an alias, False otherwise.
    """
    return getattr(func, '_is_alias', False)


def get_canonical_name(func: Callable[..., Any]) -> Optional[str]:
    """
    Get the canonical name of an alias function.

    Parameters
    ----------
    func : Callable
        The function to get the canonical name for.

    Returns
    -------
    Optional[str]
        The canonical name if the function is an alias, None otherwise.
    """
    return getattr(func, '_canonical_name', None)
