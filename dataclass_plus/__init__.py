__version__ = "1.0.8"

import typing

from dataclasses import asdict, fields, MISSING, _process_class
from typing import Any

from collections import defaultdict


def dataclass_plus(cls=None, init=True, repr=True, eq=True, order=False,
                   unsafe_hash=False, frozen=False):
    """Returns the same class as was passed in, with dunder methods
    added based on the fields defined in the class.

    Examines PEP 526 __annotations__ to determine fields.

    If init is true, an __init__() method is added to the class. If
    repr is true, a __repr__() method is added. If order is true, rich
    comparison dunder methods are added. If unsafe_hash is true, a
    __hash__() method function is added. If frozen is true, fields may
    not be assigned to after instance creation.
    """

    def wrap(cls):
        try:
            original_post_init = cls.__post_init__
        except AttributeError:
            original_post_init = BaseValidator.__original_post_init__
        setattr(cls, "__post_init__", BaseValidator.__post_init__)
        setattr(cls, "__original_post_init__", original_post_init)
        setattr(cls, "to_dict", BaseValidator.to_dict)
        return _process_class(cls, init, repr, eq, order, unsafe_hash, frozen)

    # See if we're being called as @dataclass or @dataclass().
    if cls is None:
        # We're called with parens.
        return wrap

    # We're called as @dataclass without parens.
    return wrap(cls)


def _validate_dict(value: Any, target_type: Any) -> bool:
    """
    Validate typing.Dict
    """
    if not isinstance(value, dict):
        return False
    results = []
    # List comprehension is not used because it has more performance in this way
    for key, val in value.items():
        if not isinstance(target_type.__args__[0], type):
            key_is_valid = _is_valid(key, target_type.__args__[0])
        else:
            key_is_valid = isinstance(key, target_type.__args__[0])
        if not isinstance(target_type.__args__[1], type):
            val_is_valid = _is_valid(val, target_type.__args__[1])
        else:
            val_is_valid = isinstance(val, target_type.__args__[1])
        results.append(key_is_valid and val_is_valid)
    return all(results)


def _validate_list(value: Any, target_type: Any) -> bool:
    """
    Validate typing.List
    """
    if not isinstance(value, list):
        return False
    results = []
    # List comprehension is not used because it has more performance in this way
    for val in value:
        if not isinstance(target_type.__args__[0], type):
            is_valid = _is_valid(val, target_type.__args__[0])
        else:
            is_valid = isinstance(val, target_type.__args__[0])
        results.append(is_valid)
    return all(results)


def _validate_tuple(value: Any, target_type: Any) -> bool:
    """
    Validate typing.Tuple
    """
    if not isinstance(value, tuple):
        return False
    results = []
    # List comprehension is not used because it has more performance in this way
    for index, val in enumerate(value):
        if not isinstance(target_type.__args__[index], type):
            is_valid = _is_valid(val, target_type.__args__[index])
        else:
            is_valid = type(val) is target_type.__args__[index]
        results.append(is_valid)
    return all(results)


def _validate_any_str(value: Any, target_type: Any) -> bool:
    return isinstance(value, str) or isinstance(value, bytes)


def _validate_any(value: Any, target_type: Any) -> bool:
    return True


def get_validate_func(type):
    try:
        target_type = type._name
    except AttributeError:
        target_type = str(type)
    return typing_mapping[target_type]


mapping = {
    "List": _validate_list,
    "Dict": _validate_dict,
    "Tuple": _validate_tuple,
    "~AnyStr": _validate_any_str,
    "Any": _validate_any
}

typing_mapping = defaultdict(lambda: None, mapping)


def _is_valid(value: Any, target_type: Any) -> bool:
    """
    Validate value
    """
    if isinstance(target_type, type):
        result = isinstance(value, target_type)
    else:
        validate_func = get_validate_func(target_type)
        result = validate_func(value, target_type)

    if result:
        return True
    else:
        raise TypeError(f"{value} is not {target_type}")


class BaseValidator:

    def __post_init__(self, *args, **kwargs):
        for field in fields(self):
            if field.default != MISSING:
                default_value = field.default
            elif field.default_factory != MISSING:
                default_value = None
            else:
                default_value = None

            if default_value is not None or getattr(self, field.name) is not None:
                _is_valid(getattr(self, field.name), field.type)
        self.__original_post_init__(*args, **kwargs)

    def __original_post_init__(self, *args, **kwargs):
        pass

    def to_dict(self) -> dict:
        return asdict(self)
