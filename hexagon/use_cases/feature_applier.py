# -*- coding: utf-8 -*-
import re

from .irepository import IRepository
from hexagon.models import ApplierStatus, ApplierResult


class FeatureApplier:
    def __init__(self, repository: IRepository):
        self.__repository = repository

    def apply(self, src_branch: str, target_branch: str, pattern: str) -> ApplierResult:
        regex = re.compile(pattern, re.IGNORECASE)
        matching_commits = [commit for commit in self.__repository.commits(src_branch)
                            if regex.search(commit.message) is not None]
        has_matching_commits = len(matching_commits) > 0
        if has_matching_commits:
            for commit in matching_commits:
                is_merge_commit = commit.message.find("merge") >= 0
                self.__repository.cherry_pick(str(commit.id), target_branch, is_merge_commit)
            return ApplierResult(ApplierStatus.Match, matching_commits)
        return ApplierResult(ApplierStatus.No_match, matching_commits)
