# -*- coding: utf-8 -*-
from typing import List
from hexagon.models import Commit
from uuid import UUID
from dateutil.parser import parse


class SingleMatchingCommitFix:
    def __init__(self, kwargs):
        self.branches: List[str] = kwargs['branches']
        self.src_branch: str = kwargs['src_branch']
        self.target_branch: str = kwargs['target_branch']
        self.pattern: str = kwargs['pattern']
        self.commits: List[Commit] = [Commit(UUID(commit['identifier']), commit['message'], parse(commit['date']))
                                      for commit in kwargs['commits']]
