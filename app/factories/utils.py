from dataclasses import fields


def get_dataclass_field_names(cls: type):
    return [i.name for i in fields(cls)]
