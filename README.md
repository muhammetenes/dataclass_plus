# dataclass_plus

The `dataclass_plus` is a fastest type validation library for the `dataclass`


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