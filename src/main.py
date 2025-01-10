from typing import Any, TypeVar, cast


class MyModelField:

    def __init__(self, field_name, field_annotation):
        self._name = field_name
        self._field_annotation = field_annotation

    def __get__(self, instance, owner):
        attr_name = f"_{self._name}"
        if attr_name not in instance.__dict__:
            msg = "Attempt to access attribute before setting\\loading"
            raise AttributeError(msg)
        return instance.__dict__[attr_name]

    def __set__(self, instance, value):
        attr_name = f"_{self._name}"
        if not isinstance(value, self._field_annotation):
            msg = f"Invalid value. Expected type: {self._field_annotation.__name__}"
            raise ValueError(msg)  # noqa: TRY004
        instance.__dict__[attr_name] = value


class Meta(type):
    def __new__(cls, name, bases, dct: dict[str, Any]):

        fields_annotations = cast(dict[str, Any], dct.get("__annotations__"))

        obj = super().__new__(cls, name, bases, dct)

        if fields_annotations:
            for field_name, field_type in fields_annotations.items():
                setattr(obj, field_name, MyModelField(field_name, field_type))

        return obj


T = TypeVar("T", bound="ModelBase")

class ModelBase(metaclass=Meta):

    @classmethod
    def validate(cls: type[T], data: dict[str, Any], partial: bool = False) -> T:
        if partial is False:
            raise NotImplementedError()

        obj = cls.__new__(cls)
        for field_name, field_val in data.items():
            setattr(obj, field_name, field_val)
        return obj

