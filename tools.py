import functools
import sys
from typing import Any, Callable, Dict, Iterable, Iterator, Type


assert sys.version_info >= (3, 7), 'Python 3.7+ is required'


def map_except(func: Callable,
               *iterables: Iterable,
               fallback: Dict[Type[Exception], Any]
               ) -> Iterator:
    """Similar to built-in `map` but uses `fallback` to replace function calls that raised an exception.

    :param func: Function to me mapped possibly raising exceptions.
    :param iterables: Iterables to be mapped over.
    :param fallback: Dictionary of exception types mapping to values to be used whenever `func` raises.
                     Exception types are considered in order, similar to chaining multiple 'except' clauses.
    :return: `map` object
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            for exc_type, value in fallback.items():
                if isinstance(err, exc_type):
                    return value
            raise
            
    return map(wrapper, *iterables)
