from pydantic import BaseModel
from abc import ABCMeta, abstractmethod


class TgResponse(BaseModel, metaclass=ABCMeta):

    @abstractmethod
    def as_text(self) -> str:
        raise NotImplementedError
