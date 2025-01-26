import pytest

from src.main import ModelBase
from src.validate import ValidationError


class MyClass(ModelBase):
    int_field: int
    str_field: str
    field_with_default: str = "default value"


def test__init__success():
    """
    Create instance using init method, provide all values.
    """
    TEST_INT_VALUE = 123
    TEST_STR_VALUE = "asd"
    TEST_STR_VALUE_2 = "new value"

    inst = MyClass(
        int_field=TEST_INT_VALUE,
        str_field=TEST_STR_VALUE,
        field_with_default=TEST_STR_VALUE_2,
    )

    assert inst.int_field == TEST_INT_VALUE
    assert inst.str_field == TEST_STR_VALUE
    assert inst.field_with_default == TEST_STR_VALUE_2


def test__init_only_required__success():
    """
    Create instance using init method, provide only required values.
    """
    TEST_INT_VALUE = 123
    TEST_STR_VALUE = "asd"

    inst = MyClass(
        int_field=TEST_INT_VALUE,
        str_field=TEST_STR_VALUE,
    )

    assert inst.field_with_default == "default value"


def test__init__required_field_not_provided():
    """
    Create instance not providing required field throws ValidationError.
    """

    with pytest.raises(ValidationError):
        MyClass()
