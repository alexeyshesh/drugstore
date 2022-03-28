from app.factories.utils import get_dataclass_field_names


class BaseFactory:

    def __new__(cls, *args, **kwargs):
        attrs = get_dataclass_field_names(cls.model)
        for attr in attrs:
            if attr not in kwargs:
                _attr = getattr(cls, attr)
                if callable(_attr):
                    kwargs[attr] = _attr()
                else:
                    kwargs[attr] = _attr

        return cls.model(**kwargs)
