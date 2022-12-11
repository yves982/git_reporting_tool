# -*- coding: utf-8 -*-
from typing import List


class NoMatchingCommitsFix:
    def __init__(self, branches: List[str], pattern: str):
        self.branches: [str] = branches
        self.pattern = pattern
