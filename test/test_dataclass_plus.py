from dataclasses import FrozenInstanceError

import pytest
import typing

from dataclass_plus import dataclass_plus


def test_int_validation():
    @dataclass_plus
    class IntegerDataclass:
        integer: int

    integer_dataclass = IntegerDataclass(integer=1)
    assert isinstance(integer_dataclass.integer, int)
    with pytest.raises(TypeError):
        assert IntegerDataclass(integer="test")


def test_str_validation():
    @dataclass_plus
    class StringDataclass:
        string: str

    string_dataclass = StringDataclass(string="test")
    assert isinstance(string_dataclass.string, str)
    with pytest.raises(TypeError):
        assert StringDataclass(string=1)


def test_list_validation():
    @dataclass_plus
    class ListDataclass:
        list_type: list

    list_dataclass = ListDataclass(list_type=[1, "test"])
    assert isinstance(list_dataclass.list_type, list)
    with pytest.raises(TypeError):
        assert ListDataclass(list_type=1)


def test_dict_validation():
    @dataclass_plus
    class DictDataclass:
        dict_type: dict

    dict_dataclass = DictDataclass(dict_type={"test": "test"})
    assert isinstance(dict_dataclass.dict_type, dict)
    with pytest.raises(TypeError):
        assert DictDataclass(dict_type=1)


def test_typing_list_string_validator():
    @dataclass_plus
    class TypingListStringDataclass:
        typing_list: typing.List[str]

    typing_list_string_dataclass = TypingListStringDataclass(typing_list=["test"])
    assert isinstance(typing_list_string_dataclass.typing_list[0], str)
    with pytest.raises(TypeError):
        assert TypingListStringDataclass(typing_list=[1])


def test_typing_list_int_wrong_type_validator():
    @dataclass_plus
    class TypingListStringDataclass:
        typing_list: typing.List[str]

    with pytest.raises(TypeError):
        assert TypingListStringDataclass(typing_list=1)


def test_nested_typing_list_int_wrong_type_validator():
    @dataclass_plus
    class TypingListStringDataclass:
        typing_list: typing.List[typing.List[str]]

    with pytest.raises(TypeError):
        assert TypingListStringDataclass(typing_list=1)


def test_nested_typing_list_in_list_int_wrong_type_validator():
    @dataclass_plus
    class TypingListStringDataclass:
        typing_list: typing.List[typing.List[str]]

    with pytest.raises(TypeError):
        assert TypingListStringDataclass(typing_list=[[1]])


def test_nested_typing_list_in_list_str_validator():
    @dataclass_plus
    class TypingListStringDataclass:
        typing_list: typing.List[typing.List[str]]

    assert TypingListStringDataclass(typing_list=[["test"]])


def test_nested_typing_list_in_any_validator():
    @dataclass_plus
    class TypingListAnyDataclass:
        typing_list: typing.List[typing.Any]

    assert TypingListAnyDataclass(typing_list=[""])


def test_nested_typing_list_in_any_str_validator():
    @dataclass_plus
    class TypingListAnyStrDataclass:
        typing_list: typing.List[typing.AnyStr]

    assert TypingListAnyStrDataclass(typing_list=[b""])


def test_nested_typing_list_in_any_wrong_validator():
    @dataclass_plus
    class TypingListAnyStrDataclass:
        typing_list: typing.List[typing.AnyStr]

    with pytest.raises(TypeError):
        assert TypingListAnyStrDataclass(typing_list=[1])


def test_typing_dict_string_validator():
    @dataclass_plus
    class TypingDictStringDataclass:
        typing_dict: typing.Dict[str, str]

    typing_dict_string_dataclass = TypingDictStringDataclass(
        typing_dict={"test": "test"}
    )
    assert isinstance(typing_dict_string_dataclass.typing_dict["test"], str)
    with pytest.raises(TypeError):
        assert TypingDictStringDataclass(typing_dict={1: 1})


def test_typing_dict_wrong_type_validator():
    @dataclass_plus
    class TypingDictDataclass:
        typing_dict: typing.Dict[str, str]
    with pytest.raises(TypeError):
        assert TypingDictDataclass(typing_dict=1)


def test_nested_typing_dict_list_type_validator():
    @dataclass_plus
    class TypingDictDataclass:
        typing_dict: typing.Dict[str, typing.List[int]]

    assert TypingDictDataclass(typing_dict={"test": [1]})


def test_nested_typing_dict_wrong_int_type_validator():
    @dataclass_plus
    class TypingDictDataclass:
        typing_dict: typing.Dict[str, typing.List[int]]

    with pytest.raises(TypeError):
        assert TypingDictDataclass(typing_dict={"a": 1})


def test_nested_typing_dict_any_list_type_validator():
    @dataclass_plus
    class TypingDictDataclass:
        typing_dict: typing.Dict[typing.Any, typing.List[int]]

    assert TypingDictDataclass(typing_dict={"test": [1]})


def test_nested_typing_dict_anystr_list_type_validator():
    @dataclass_plus
    class TypingDictDataclass:
        typing_dict: typing.Dict[typing.AnyStr, typing.List[int]]

    assert TypingDictDataclass(typing_dict={b"test": [1]})


def test_nested_typing_dict_anystr_wrong_type_validator():
    @dataclass_plus
    class TypingDictDataclass:
        typing_dict: typing.Dict[typing.AnyStr, typing.List[int]]

    with pytest.raises(TypeError):
        assert TypingDictDataclass(typing_dict={1: [1]})


def test_nested_typing_dict_wrong_str_type_validator():
    @dataclass_plus
    class TypingDictDataclass:
        typing_dict: typing.Dict[str, typing.List[int]]

    with pytest.raises(TypeError):
        assert TypingDictDataclass(typing_dict={"a": "asd"})


def test_nested_typing_dict_wrong_dict_type_validator():
    @dataclass_plus
    class TypingDictDataclass:
        typing_dict: typing.Dict[str, typing.List[int]]

    with pytest.raises(TypeError):
        assert TypingDictDataclass(typing_dict={1: [1, 2]})


def test_typing_tuple_str_validator():
    @dataclass_plus
    class TypingTupleStringDataclass:
        typing_tuple: typing.Tuple[str]

    assert TypingTupleStringDataclass(typing_tuple=("",))


def test_typing_tuple_str_wrong_type_validator():
    @dataclass_plus
    class TypingTupleStringDataclass:
        typing_tuple: typing.Tuple[str]

    with pytest.raises(TypeError):
        assert TypingTupleStringDataclass(typing_tuple=(1,))


def test_typing_tuple_int_validator():
    @dataclass_plus
    class TypingTupleIntDataclass:
        typing_tuple: typing.Tuple[int]

    assert TypingTupleIntDataclass(typing_tuple=(1,))


def test_typing_tuple_int_wrong_type_validator():
    @dataclass_plus
    class TypingTupleIntDataclass:
        typing_tuple: typing.Tuple[int]

    with pytest.raises(TypeError):
        assert TypingTupleIntDataclass(typing_tuple=("test",))


def test_typing_tuple_wrong_type_validator():
    @dataclass_plus
    class TypingTupleIntDataclass:
        typing_tuple: typing.Tuple[int]

    with pytest.raises(TypeError):
        assert TypingTupleIntDataclass(typing_tuple=1)


def test_typing_tuple_int_str_validator():
    @dataclass_plus
    class TypingTupleIntDataclass:
        typing_tuple: typing.Tuple[int, str]

    assert TypingTupleIntDataclass(typing_tuple=(1, "test"))


def test_typing_tuple_int_str_wrong_type_validator():
    @dataclass_plus
    class TypingTupleIntDataclass:
        typing_tuple: typing.Tuple[int, str]

    with pytest.raises(TypeError):
        assert TypingTupleIntDataclass(typing_tuple=("test", 1))


def test_typing_tuple_any_str_type_validator():
    @dataclass_plus
    class TypingTupleIntDataclass:
        typing_tuple: typing.Tuple[typing.Any, int]

    assert TypingTupleIntDataclass(typing_tuple=("test", 1))


def test_typing_tuple_anystr_str_type_validator():
    @dataclass_plus
    class TypingTupleIntDataclass:
        typing_tuple: typing.Tuple[typing.AnyStr, int]

    assert TypingTupleIntDataclass(typing_tuple=(b"test", 1))


def test_typing_tuple_anystr_str_wrong_type_validator():
    @dataclass_plus
    class TypingTupleIntDataclass:
        typing_tuple: typing.Tuple[typing.AnyStr, int]

    with pytest.raises(TypeError):
        assert TypingTupleIntDataclass(typing_tuple=(1, 1))


def test_typing_tuple_int_typing_list_validator():
    @dataclass_plus
    class TypingTupleIntDataclass:
        typing_tuple: typing.Tuple[int, typing.List[str]]

    assert TypingTupleIntDataclass(typing_tuple=(1, ["test"]))


def test_typing_tuple_int_typing_list_wrong_type_validator():
    @dataclass_plus
    class TypingTupleIntDataclass:
        typing_tuple: typing.Tuple[int, typing.List[str]]

    with pytest.raises(TypeError):
        assert TypingTupleIntDataclass(typing_tuple=(1, 1))


def test_typing_any_type_validator():
    @dataclass_plus
    class TypingAnyDataclass:
        typing_any: typing.Any

    assert TypingAnyDataclass(typing_any="test")


def test_typing_any_str_byte_type_validator():
    @dataclass_plus
    class TypingAnyDataclass:
        typing_any: typing.AnyStr

    assert TypingAnyDataclass(typing_any=b"test")


def test_typing_any_str_str_type_validator():
    @dataclass_plus
    class TypingAnyDataclass:
        typing_any: typing.AnyStr

    assert TypingAnyDataclass(typing_any="test")


def test_typing_any_str_int_type_validator():
    @dataclass_plus
    class TypingAnyDataclass:
        typing_any: typing.AnyStr

    with pytest.raises(TypeError):
        assert TypingAnyDataclass(typing_any=1)


def test_to_dict():
    @dataclass_plus
    class ToDictDataclass:
        integer: int
        string: str
        list_type: list
        dict_type: dict
        tuple_type: tuple
        typing_list: typing.List[str]
        typing_dict: typing.Dict[str, str]
        typing_tuple: typing.Tuple[str]
        typing_any: typing.Any
        typing_anystr: typing.AnyStr

    dc = ToDictDataclass(
        integer=1,
        string="",
        list_type=[],
        dict_type={},
        tuple_type=(),
        typing_list=[""],
        typing_dict={"": ""},
        typing_tuple=("",),
        typing_any="",
        typing_anystr=b""
    )
    result = {
        "integer": 1,
        "string": "",
        "list_type": [],
        "dict_type": {},
        "tuple_type": (),
        "typing_list": [""],
        "typing_dict": {"": ""},
        "typing_tuple": ("",),
        "typing_any": "",
        "typing_anystr": b""
    }
    assert dc.to_dict() == result


def test_default_post_init_control():
    @dataclass_plus
    class PostInitDataclass:
        a: int
        b: str

        def __post_init__(self, *args, **kwargs):
            self.a = 2
            self.b = "test_2"

    dc = PostInitDataclass(a=1, b="test")

    assert dc.a == 2 and dc.b == "test_2"


def test_frozen_true_control():
    @dataclass_plus(frozen=True)
    class FrozenDataclass:
        a: int
        b: str

    dc = FrozenDataclass(a=1, b="test")
    with pytest.raises(FrozenInstanceError):
        dc.a = 2


def test_frozen_true_validation_control():
    @dataclass_plus(frozen=True)
    class FrozenDataclass:
        a: int
        b: str

    with pytest.raises(TypeError):
        FrozenDataclass(a="test", b=1)
