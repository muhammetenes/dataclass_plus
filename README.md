# dataclass_plus
[![Python 3.6](https://img.shields.io/badge/python-3.6-brightgreen.svg)](https://www.python.org/downloads/release/python-360)
[![pypi](https://badge.fury.io/py/dataclass-plus.svg)](https://badge.fury.io/py/dataclass-plus)

The `dataclass_plus` is a fastest type validation library for the `dataclass`


## Install
```
pip install dataclass-plus
```

## Example


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
# => ValueError: {'test': 1} is not typing.Dict[str, str]
```
