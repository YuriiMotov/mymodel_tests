import pytest

from src.main import ModelBase
from src.types import ValidationError


def test__requered_field_not_provided():
    """
    Attempt to create instance without providing value for requered field
    causes ValidationError
    """

    class MyClass(ModelBase):
        int_field: int

    with pytest.raises(ValidationError):
        MyClass()


def test__optional_field_not_provided():
    """
    Attempt to create instance without providing value for optional field
    causes ValidationError
    """


    DEFAULT_VAL = 42

    class MyClass(ModelBase):
        int_field: int = DEFAULT_VAL

    inst = MyClass()

    assert inst.int_field == DEFAULT_VAL
