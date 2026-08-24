from dataclasses import dataclass


@dataclass(frozen=True)
class ExampleValueObject:

    value: float
    unit: str


class ExampleEntity:

    def __init__(self, id: int, name: str, value_object: ExampleValueObject):
        self.id = id
        self.name = name
        self.value_object = value_object

    def __eq__(self, other) -> bool:
        if not isinstance(other, ExampleEntity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
