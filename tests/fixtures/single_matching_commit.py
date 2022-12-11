# -*- coding: utf-8 -*-
from typing import  List
from hexagon.models import Commit


class SingleMatchingCommitFix:
    def __init__(self, branches: List[str], commits: List[Commit], pattern: str):
        self.branches = branches
        self.commits = commits
        self.pattern = pattern
