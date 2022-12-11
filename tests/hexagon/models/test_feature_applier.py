import json

import pytest

from hexagon.use_cases import FeatureApplier
from hexagon.gateway import IRepository
from hexagon.models import ApplierStatus, Commit

from tests.fixtures import NoMatchingCommitsFix, MatchingCommitsFix
from tests.helpers import assert_collection_equivalent

_feature_applier: FeatureApplier | None = None
_rep: IRepository | None = None


@pytest.fixture
def no_matching_commits():
    with open("tests/fixtures/no_matching_commits.json", "r", encoding="utf-8") as f:
        return NoMatchingCommitsFix(**json.load(f))


FILES = [
    "tests/fixtures/single_matching_commit.json",
    "tests/fixtures/multiple_matching_commits.json"
]


@pytest.fixture(params=FILES)
def matching_commits(request):
    with open(request.param, "r", encoding="utf-8") as f:
        return MatchingCommitsFix(json.load(f))


@pytest.fixture()
def repository_error_matching_commit():
    with open("tests/fixtures/repository_error_matching_commit.json", "r", encoding="utf-8") as f:
        return MatchingCommitsFix(json.load(f))


@pytest.fixture(autouse=True)
def setup(mocker):
    global _feature_applier, _rep
    _rep = mocker.patch("hexagon.gateway.irepository.IRepository")
    _feature_applier = FeatureApplier(_rep)


def compare_commits_by_identifier(first_commit: Commit, second_commit: Commit):
    return 0 if first_commit.id == second_commit.id else 1


def extract_filtered_commits(matching_commits: MatchingCommitsFix):
    filtered_commits = [commit for commit in matching_commits.commits if commit.id in matching_commits.applied_commits]
    return filtered_commits


@pytest.mark.feature_applier
def test_feature_applier_no_matching_commits(mocker, no_matching_commits):
    _rep.branches.return_value = no_matching_commits.branches
    _rep.filter_commits.return_value = []

    res = _feature_applier.apply(no_matching_commits.src_branch, no_matching_commits.target_branch,
                                 no_matching_commits.pattern)
    assert res.status == ApplierStatus.No_match
    assert res.applied_commits == []


@pytest.mark.feature_applier
def test_feature_applier_single_matching_commit(mocker, matching_commits):
    _rep.branches.return_value = matching_commits.branches
    _rep.commits.return_value = matching_commits.commits
    filtered_commits = extract_filtered_commits(matching_commits)
    _rep.filter_commits.return_value = filtered_commits

    cherry_pick = mocker.spy(_rep, "cherry_pick")

    res = _feature_applier.apply(matching_commits.src_branch, matching_commits.target_branch,
                                 matching_commits.pattern)
    assert res.status == ApplierStatus.Match
    assert_collection_equivalent(res.applied_commits, matching_commits.commits,
                                 "applied_commits", compare_commits_by_identifier)
    assert cherry_pick.call_count == len(matching_commits.commits), "All advertised commits were not commited !"
    for (i, commit_id) in enumerate(matching_commits.applied_commits):
        assert cherry_pick.mock_calls[i].args == (str(commit_id), matching_commits.target_branch, True), \
            f"Missing commit {str(commit_id)} call !"


@pytest.mark.feature_applier
def test_feature_applier_repository_error(mocker, repository_error_matching_commit):
    _rep.branches.return_value = repository_error_matching_commit.branches
    _rep.commits.return_value = repository_error_matching_commit.commits
    _rep.filter_commits.return_value = extract_filtered_commits(repository_error_matching_commit)
    err_message = "fail to connect to repository!"
    _rep.cherry_pick.side_effect = IOError(err_message)

    with pytest.raises(IOError) as io_err:
        _feature_applier.apply(repository_error_matching_commit.src_branch,
                               repository_error_matching_commit.target_branch,
                               repository_error_matching_commit.pattern)
        assert io_err.value.args[0] == err_message
