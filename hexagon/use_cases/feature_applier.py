# -*- coding: utf-8 -*-
from .irepository import IRepository


class FeatureApplier:
    def __init__(self, repository: IRepository):
        self.__repository = repository
