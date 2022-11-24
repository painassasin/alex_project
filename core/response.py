from abc import ABCMeta, abstractmethod

from pydantic import BaseModel


class TgResponse(BaseModel, metaclass=ABCMeta):

    @abstractmethod
    def as_text(self) -> str:
        raise NotImplementedError
