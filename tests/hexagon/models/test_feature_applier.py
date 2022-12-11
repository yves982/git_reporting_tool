import json

import pytest
from pytest_mock import mocker

from hexagon.use_cases import Repository, IRepository, FeatureApplier
from hexagon.models import ApplierStatus
import io

from tests.fixtures import NoMatchingCommitsFix

_feature_applier: FeatureApplier | None = None
_rep: IRepository | None = None

@pytest.fixture
def no_matching_commits():
    with open("tests/fixtures/no_matching_commits.json", "r", encoding="utf-8") as f:
        return NoMatchingCommitsFix(**json.load(f))

@pytest.fixture(autouse=True)
def setup(mocker):
    global _feature_applier, _rep
    _rep = mocker.patch("hexagon.use_cases.irepository.IRepository")
    _feature_applier = FeatureApplier(_rep)


@pytest.mark.feature_applier
def test_feature_applier_no_matching_commits(mocker, no_matching_commits):
    _rep.branches.return_value = no_matching_commits.branches

    res = _feature_applier.apply(no_matching_commits.pattern)
    assert res.status == ApplierStatus.No_match


@pytest.mark.skip
def test_feature_applier_single_matching_commit():
    pass

@pytest.mark.skip
def test_feature_applier_multiple_matching_commits():
    pass

@pytest.mark.skip
def test_feature_applier_repository_error():
    pass
