import typing

from marshmallow import Schema

from chalicelib.exceptions.validation_error import ChaliceValidationError, ChaliceUnhandledError
from marshmallow import ValidationError



class BaseSchema(Schema):
    validation_error = ChaliceValidationError

    def __init__(self, data: dict | list, **kwargs):
        super().__init__(**kwargs)
        self._data = data
        self._validated_data = None

    def is_valid(self,
                 many: bool = False,
                 partial: bool = False,
                 raise_exception: bool = False):
        try:
            self._validated_data = self.load(self._data, many=many, partial=partial)
        except ValidationError as exc:
            messages = typing.cast(typing.Dict[str, typing.List[str]], exc.messages)
            if raise_exception:
                raise self.validation_error(messages=messages)
            return messages

    @property
    def data(self) -> dict:
        if not self._validated_data:
            raise AttributeError('Data not validated. Try calling the is_valid method')

        return self._validated_data
