import pytest
from pytest_mock import mocker

from hexagon.use_cases import Repository, FeatureApplier

_feature_applier : FeatureApplier | None = None
_rep : Repository | None = None

@pytest.fixture(autouse=True)
def setup(repository):
    global _feature_applier, _rep
    _feature_applier = FeatureApplier(repository)
    _rep = mocker(Repository)

def test_feature_applier_no_matching_commits():
    pass

def test_feature_applier_single_matching_commit():
    pass

def test_feature_applier_multiple_matching_commits():
    pass

def test_feature_applier_repository_error():
    pass