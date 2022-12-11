# -*- coding: utf-8 -*-
import uuid
from datetime import datetime


class Commit:
    """
    A commit DTO
    """
    def __init__(self, identifier: uuid.UUID, message: str, date: datetime = datetime.utcnow()):
        self.__id: uuid.UUID = identifier
        self.__message: str = message
        self.__date = date

    @property
    def id(self):
        return self.__id

    @property
    def message(self):
        return self.__message

    @property
    def date(self):
        return self.__date

    def __repr__(self):
        return f"{self.__id}({self.__message}) on {self.date.strftime('%Y-%m-%d')}"
