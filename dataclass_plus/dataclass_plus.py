import typing

from dataclasses import asdict, fields, MISSING, _process_class
from typing import Any


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
        setattr(cls, "__post_init__", BaseValidator.__post_init__)
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
        if isinstance(target_type.__args__[0], typing._GenericAlias):
            _is_valid(val, target_type.__args__[0])
        elif isinstance(target_type.__args__[1], typing._GenericAlias):
            _is_valid(val, target_type.__args__[1])
        results.append(
            isinstance(key, target_type.__args__[0]) and
            isinstance(val, target_type.__args__[1]))
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
        if isinstance(target_type.__args__[0], typing._GenericAlias):
            _is_valid(val, target_type.__args__[0])
        else:
            results.append(isinstance(val, target_type.__args__[0]))
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
        if isinstance(target_type.__args__[index], typing._GenericAlias):
            _is_valid(val, target_type.__args__[index])
        else:
            results.append(type(val) is target_type.__args__[index])
    return all(results)


def get_validate_func(type):
    return typing_mapping.get(type)


typing_mapping = {
    "List": _validate_list,
    "Dict": _validate_dict,
    "Tuple": _validate_tuple
}


def _is_valid(value: Any, target_type: Any) -> bool:
    """
    Validate value
    """
    if isinstance(target_type, type):
        result = isinstance(value, target_type)
    else:
        validate_func = get_validate_func(target_type._name)
        result = validate_func(value, target_type)

    if result:
        return True
    else:
        raise ValueError(f"{value} is not {target_type}")


class BaseValidator:

    def __post_init__(self):
        for field in fields(self):
            if field.default != MISSING:
                default_value = field.default
            elif field.default_factory != MISSING:
                default_value = None
            else:
                default_value = None

            if default_value is not None or getattr(self, field.name) is not None:
                _is_valid(getattr(self, field.name), field.type)

    def to_dict(self) -> dict:
        return asdict(self)


