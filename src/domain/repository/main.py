from abc import ABCMeta, abstractmethod


class Repository(metaclass=ABCMeta):
    @abstractmethod
    def save(self):
        pass
