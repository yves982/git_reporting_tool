# -*- coding: utf-8 -*-
from hexagon.models import ApplierStatus, Commit
from typing import List


class ApplierResult:
    def __init__(self, status: ApplierStatus, applied_commits: List[Commit]):
        self._status: ApplierStatus = status
        self._applied_commits = applied_commits

    @property
    def status(self):
        return self._status

    @property
    def applied_commits(self):
        return self._applied_commits
