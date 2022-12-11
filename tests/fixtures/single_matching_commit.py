# -*- coding: utf-8 -*-
from typing import List, Mapping
from hexagon.models import Commit
from uuid import UUID
from dateutil.parser import parse


class SingleMatchingCommitFix:
    def __init__(self, raw_json: Mapping[str, object]):
        self.branches: List[str] = raw_json['branches']
        self.src_branch: str = raw_json['src_branch']
        self.target_branch: str = raw_json['target_branch']
        self.pattern: str = raw_json['pattern']
        self.commits: List[Commit] = [Commit(UUID(commit['identifier']), commit['message'], parse(commit['date']))
                                      for commit in raw_json['commits']]
        self.applied_commits: List[UUID] = [UUID(commit_id) for commit_id in raw_json['applied_commits']]
