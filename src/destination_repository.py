from abc import ABC, abstractmethod
from src import model
from typing import List
from src import model


class AbstractDestinationRepository(ABC):

    @abstractmethod
    def load_example_value_objects(self, example_value_objects: List[model.ExampleValueObject]):

        raise NotImplementedError

    @abstractmethod
    def load_example_entities(self, example_entities: List[model.ExampleEntity]):

        raise NotImplementedError

