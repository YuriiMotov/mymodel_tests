import typing
from typing import Any, TypeVar, cast

from src.validate import Undefined, field_validate


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
            msg = (
                "Invalid value. "
                f"Expected type {self._field_annotation.__name__}, "
                f"got {type(value)}. Input: {value}"
            )
            raise ValueError(msg)  # noqa: TRY004
        instance.__dict__[attr_name] = value


@typing.dataclass_transform(kw_only_default=True)
class Meta(type):
    def __new__(cls, name, bases, dct: dict[str, Any]):
        fields_annotations = cast(dict[str, Any], dct.get("__annotations__"))

        obj = super().__new__(cls, name, bases, dct)

        defaults: dict[str, Any] = {}
        if fields_annotations:
            for field_name, field_type in fields_annotations.items():
                setattr(obj, field_name, MyModelField(field_name, field_type))
                if field_name in dct:
                    defaults[field_name] = dct[field_name]

        def __init__(self: "ModelBase", *args, **kwargs):
            if len(args):
                msg = "Can only accept keyword arguments"
                raise RuntimeError(msg)
            if fields_annotations:
                for field_name, field_type in fields_annotations.items():
                    default = defaults.get(field_name, Undefined)
                    val = field_validate(
                        field_name=field_name,
                        field_type=field_type,
                        default=default,
                        value=kwargs.get(field_name, Undefined),
                    )
                    self.__setattr__(field_name, val)

        obj.__init__ = __init__

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
