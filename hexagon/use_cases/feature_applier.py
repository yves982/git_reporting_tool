# -*- coding: utf-8 -*-
import re

from ..gateway.irepository import IRepository
from hexagon.models import ApplierStatus, ApplierResult


class FeatureApplier:
    def __init__(self, repository: IRepository):
        self.__repository = repository

    def apply(self, src_branch: str, target_branch: str, pattern: str) -> ApplierResult:
        regex = re.compile(pattern, re.IGNORECASE)
        matching_commits = self.__repository.filter_commits(src_branch, pattern)
        has_matching_commits = len(matching_commits) > 0
        if has_matching_commits:
            for commit in matching_commits:
                is_merge_commit = commit.message.find("merge") >= 0
                self.__repository.cherry_pick(str(commit.id), target_branch, is_merge_commit)
            return ApplierResult(ApplierStatus.Match, matching_commits)
        return ApplierResult(ApplierStatus.No_match, matching_commits)
