import json

import pytest

from hexagon.use_cases import IRepository, FeatureApplier
from hexagon.models import ApplierStatus, Commit

from tests.fixtures import NoMatchingCommitsFix, SingleMatchingCommitFix
from tests.helpers import assert_collection_equivalent

_feature_applier: FeatureApplier | None = None
_rep: IRepository | None = None


@pytest.fixture
def no_matching_commits():
    with open("tests/fixtures/no_matching_commits.json", "r", encoding="utf-8") as f:
        return NoMatchingCommitsFix(**json.load(f))


@pytest.fixture
def single_matching_commit():
    with open("tests/fixtures/single_matching_commit.json", "r", encoding="utf-8") as f:
        return SingleMatchingCommitFix(json.load(f))


@pytest.fixture(autouse=True)
def setup(mocker):
    global _feature_applier, _rep
    _rep = mocker.patch("hexagon.use_cases.irepository.IRepository")
    _feature_applier = FeatureApplier(_rep)


def compare_commits_by_identifier(first_commit: Commit, second_commit: Commit):
    return 0 if first_commit.id == second_commit.id else 1

@pytest.mark.feature_applier
def test_feature_applier_no_matching_commits(mocker, no_matching_commits):
    _rep.branches.return_value = no_matching_commits.branches

    res = _feature_applier.apply(no_matching_commits.src_branch, no_matching_commits.target_branch,
                                 no_matching_commits.pattern)
    assert res.status == ApplierStatus.No_match
    assert res.applied_commits == []

@pytest.mark.feature_applier
def test_feature_applier_single_matching_commit(mocker, single_matching_commit):
    _rep.branches.return_value = single_matching_commit.branches
    _rep.commits.return_value = single_matching_commit.commits

    cherry_pick = mocker.spy(_rep, "cherry_pick")

    res = _feature_applier.apply(single_matching_commit.src_branch, single_matching_commit.target_branch,
                                 single_matching_commit.pattern)
    assert res.status == ApplierStatus.Match
    assert_collection_equivalent(res.applied_commits, single_matching_commit.commits,
                                 "applied_commits", compare_commits_by_identifier)
    assert cherry_pick.call_count == len(single_matching_commit.commits), "All advertised commits were not commited !"



@pytest.mark.skip
def test_feature_applier_multiple_matching_commits():
    pass


@pytest.mark.skip
def test_feature_applier_repository_error():
    pass
