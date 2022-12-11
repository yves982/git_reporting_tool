# -*- coding: utf-8 -*-
import re

from .irepository import IRepository
from hexagon.models import ApplierStatus, ApplierResult


class FeatureApplier:
    def __init__(self, repository: IRepository):
        self.__repository = repository

    def apply(self, pattern: str) -> ApplierResult:
        regex = re.compile(pattern, re.IGNORECASE)
        matching_branches = [x for x in self.__repository.branches() if regex.search(x) is not None]
        has_matching_branches = len(matching_branches) > 0
        if has_matching_branches:
            return ApplierResult(ApplierStatus.Match, [])
        return ApplierResult(ApplierStatus.No_match, [])
