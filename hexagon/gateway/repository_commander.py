# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from hexagon.models import CherryPickResult


class IRepositoryCommander(ABC):
    @abstractmethod
    def cherry_pick(self, commit_id: str, target_branch: str, is_merge: bool = True) -> CherryPickResult:
        pass
