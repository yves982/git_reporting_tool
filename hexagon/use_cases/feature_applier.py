# -*- coding: utf-8 -*-
from .irepository import IRepository
from hexagon.models import ApplierStatus, ApplierResult


class FeatureApplier:
    def __init__(self, repository: IRepository):
        self.__repository = repository

    def apply(self, pattern: str) -> ApplierResult:
        return ApplierResult(ApplierStatus.No_match, [])
