import pytest
import typing

from dataclass_plus import dataclass_plus


def test_int_validation():
    @dataclass_plus
    class IntegerDataclass:
        integer: int

    integer_dataclass = IntegerDataclass(integer=1)
    assert isinstance(integer_dataclass.integer, int)
    with pytest.raises(ValueError):
        assert IntegerDataclass(integer="test")


def test_str_validation():
    @dataclass_plus
    class StringDataclass:
        string: str

    string_dataclass = StringDataclass(string="test")
    assert isinstance(string_dataclass.string, str)
    with pytest.raises(ValueError):
        assert StringDataclass(string=1)


def test_list_validation():
    @dataclass_plus
    class ListDataclass:
        list_type: list

    list_dataclass = ListDataclass(list_type=[1, "test"])
    assert isinstance(list_dataclass.list_type, list)
    with pytest.raises(ValueError):
        assert ListDataclass(list_type=1)


def test_dict_validation():
    @dataclass_plus
    class DictDataclass:
        dict_type: dict

    dict_dataclass = DictDataclass(dict_type={"test": "test"})
    assert isinstance(dict_dataclass.dict_type, dict)
    with pytest.raises(ValueError):
        assert DictDataclass(dict_type=1)


def test_typing_list_string_validator():
    @dataclass_plus
    class TypingListStringDataclass:
        typing_list: typing.List[str]

    typing_list_string_dataclass = TypingListStringDataclass(typing_list=["test"])
    assert isinstance(typing_list_string_dataclass.typing_list[0], str)
    with pytest.raises(ValueError):
        assert TypingListStringDataclass(typing_list=[1])


def test_typing_dict_string_validator():
    @dataclass_plus
    class TypingDictStringDataclass:
        typing_dict: typing.Dict[str, str]

    typing_dict_string_dataclass = TypingDictStringDataclass(
        typing_dict={"test": "test"}
    )
    assert isinstance(typing_dict_string_dataclass.typing_dict["test"], str)
    with pytest.raises(ValueError):
        assert TypingDictStringDataclass(typing_dict={1: 1})
