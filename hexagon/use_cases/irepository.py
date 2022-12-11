# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List

from hexagon.models import Commit, CherryPickResult


class IRepository(ABC):

    @abstractmethod
    def commits(self, branch_name: str) -> List[Commit]:
        pass

    @abstractmethod
    def branches(self) -> List[str]:
        pass

    @abstractmethod
    def filter_commits(self, branch_name: str, pattern: str) -> List[Commit]:
        pass

    @abstractmethod
    def cherry_pick(self, commit_id: str, target_branch: str, is_merge: bool = True) -> CherryPickResult:
        pass
