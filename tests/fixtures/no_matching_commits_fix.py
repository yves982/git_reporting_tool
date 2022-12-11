# -*- coding: utf-8 -*-
from typing import List


class NoMatchingCommitsFix:
    def __init__(self, branches: List[str], src_branch: str, target_branch: str, pattern: str):
        self.branches: [str] = branches
        self.src_branch = src_branch
        self.pattern = pattern
        self.target_branch = target_branch
