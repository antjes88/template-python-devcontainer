from abc import ABC, abstractmethod
from typing import List

from src import model


class AbstractSourceRepository(ABC):


    @abstractmethod
    def get_example_value_objects(self) -> List[model.ExampleValueObject]:

        raise NotImplementedError

    @abstractmethod
    def get_example_entities(self) -> List[model.ExampleEntity]:

        raise NotImplementedError
