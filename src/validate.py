from typing import Any, Union, get_args, get_origin

from src.types import Undefined, ValidationError


def _validate_value(value: Any, annotation: type):
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Optional, which is equivalent to Union[T, None]
    if origin is Union and type(None) in args:
        # Check if the value is None or matches one of the types in the Union
        return value is None or any(
            isinstance(value, arg) for arg in args if arg is not type(None)
        )

    # For other types (not Optional/Union), check directly
    return isinstance(value, annotation)


def field_validate(
    field_name: str,
    field_type: type,
    default: Any = Undefined,
    value: Any = Undefined,
) -> Any:
    """
    Take value or default value and validate it against field type.
    Return final value of the field.
    """
    if value is not Undefined:
        if not _validate_value(value, field_type):
            msg = f"Wrong value for {field_name}. Expected {field_type}, got {type(value)}"
            raise ValidationError(msg=msg)
        return value

    if default is not Undefined:
        if not _validate_value(default, field_type):
            msg = f"Wrong default value for {field_name}. Expected {field_type}, got {type(default)}"
            raise ValidationError(msg=msg)
        return default

    msg = "No value was provided for required field: "
    raise ValidationError(msg)
