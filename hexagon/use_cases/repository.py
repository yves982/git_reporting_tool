# -*- coding: utf-8 -*-
import re

from hexagon.gateway import IRepositoryReader, IRepositoryCommander
from .irepository import IRepository


class Repository(IRepository):
    """
    Active class to handle a cvs repository
    """

    def __init__(self, reader: IRepositoryReader, commander: IRepositoryCommander):
        self.__reader = reader
        self.__commander = commander

    def commits(self, branch_name: str):
        if branch_name is None or len(branch_name) == 0:
            raise ValueError("branch name cannot be empty or none")
        return self.__reader.commits(branch_name)

    def branches(self):
        return self.__reader.branches()

    def filter_commits(self, branch_name: str, pattern: str):
        commits = self.commits(branch_name)
        regex = re.compile(pattern, re.RegexFlag.MULTILINE | re.RegexFlag.IGNORECASE)
        return [commit for commit in commits if regex.match(commit.message) is not None]

    def cherry_pick(self, commit_id: str, target_branch: str, is_merge: bool = True):
        return self.__commander.cherry_pick(commit_id, target_branch, is_merge)
