# dataclass_plus
[![Python 3.6](https://img.shields.io/badge/python-3.7-brightgreen.svg)](https://www.python.org/downloads/release/python-370)
[![pypi](https://badge.fury.io/py/dataclass-plus.svg)](https://badge.fury.io/py/dataclass-plus)
[![travis-badge](https://travis-ci.org/mgurdal/aegis.svg?branch=master)](https://travis-ci.org/muhammetenes/dataclass_plus)
[![Coverage Status](https://coveralls.io/repos/github/muhammetenes/dataclass_plus/badge.svg?branch=master)](https://coveralls.io/github/muhammetenes/dataclass_plus?branch=master)

The `dataclass_plus` is a fastest type validation library for the `dataclass`


## Install
```
pip install dataclass-plus
```

## Example

Basic Example
```python
from dataclass_plus import dataclass_plus
from typing import List, Dict, Tuple


@dataclass_plus
class Model:
    id: int
    name: str
    dict_example: Dict[str, str]
    list_example: List[int] # this field is required
    tuple_example: Tuple[str, float] = None # this field is not required because set default None


Model(
    id=1, 
    name='Test Test', 
    dict_example={"test": "test"}, 
    list_example=[1,2],
    tuple_example=("test", 1.2)
)
# => Model(id=1, name='Test Test', dict_example={"test": "test"}, list_example=[1,2], tuple_example=("test", 1.2))

# Invalid Model
Model(
    id=1, 
    name='Test Test', 
    dict_example={"test": 1}, 
    list_example=[1,2],
    tuple_example=("test", 1.2)
)
# => TypeError: {'test': 1} is not typing.Dict[str, str]

```

Nested Example

```python
from dataclass_plus import dataclass_plus
from typing import List, Dict, Tuple


@dataclass_plus
class Model:
    nested_example: List[List[str]]
    multi_nested_example: Dict[str, List[Tuple[str, List[int]]]]


Model(
    nested_example=[["test"], ["test_2"]],
    multi_nested_example={"test": [("test",[1, 2])]}
)
# => Model(nested_example=[['test'], ['test_2']], multi_nested_example={'test': [('test', [1, 2])]})

# Invalid Model
Model(
    nested_example=[["test"], ["test_2"]],
    multi_nested_example={"test": [("test",[1, "test"])]}
)
# => TypeError: [1, 'test'] is not typing.List[int]

```

Note: Can use every feature of dataclass (Example: frozen=True, init=True ...)