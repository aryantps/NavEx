from abc import ABC, abstractmethod


class DatabaseDriver(ABC):
    """
    base driver class to be inherited for connecting to database
    """
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass
