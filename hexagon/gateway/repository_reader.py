# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from hexagon.models import Commit


class IRepositoryReader(ABC):
    @abstractmethod
    def branches(self) -> List[str]:
        pass

    @abstractmethod
    def commits(self, branch_name: str) -> List[Commit]:
        pass
