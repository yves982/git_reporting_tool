# -*- coding: utf-8 -*-
from .commit import Commit


class CherryPickResult:
    """
    Result of a cherry_pick command
    """

    def __init__(self, success: bool, new_commit: Commit):
        self.__success = success
        self.__new_commit = new_commit

    @property
    def success(self):
        return self.__success

    @property
    def new_commit(self):
        return self.__new_commit
