import pytest

from src.main import ModelBase


class MyClass(ModelBase):
    int_field: int
    str_field: str


def test__not_set__attribute_error():
    """
    Attempt to access atribute that hasn't been set yet causes AttributeError
    """

    inst = MyClass()

    with pytest.raises(AttributeError):
        _ = inst.int_field

    with pytest.raises(AttributeError):
        _ = inst.str_field


def test__set__value_stored_in_right_attribute():
    """
    When set attribute value, it's stored in attribute with leading underscore
    """

    inst = MyClass()

    TEST_INT_VALUE = 123
    inst.int_field = TEST_INT_VALUE
    assert inst.int_field == TEST_INT_VALUE
    assert inst.__getattribute__("_int_field") == TEST_INT_VALUE

    TEST_STR_VALUE = "asd"
    inst.str_field = TEST_STR_VALUE
    assert inst.str_field == TEST_STR_VALUE
    assert inst.__getattribute__("_str_field") == TEST_STR_VALUE



def test__set_invalid_value__value_error():
    """
    Attempt to set invalid value causes ValueError
    """

    inst = MyClass()

    with pytest.raises(ValueError):  # noqa: PT011
        inst.int_field = "asd"

    with pytest.raises(ValueError):  # noqa: PT011
        inst.str_field = 123

