import pytest
from pytest_mock import mocker

from hexagon.use_cases import Repository, IRepository, FeatureApplier
from hexagon.models import ApplierStatus

_feature_applier: FeatureApplier | None = None
_rep: IRepository | None = None


@pytest.fixture(autouse=True)
def setup(mocker):
    global _feature_applier, _rep
    _rep = mocker.patch("hexagon.use_cases.irepository.IRepository")
    _feature_applier = FeatureApplier(_rep)


@pytest.mark.feature_applier
def test_feature_applier_no_matching_commits(mocker):
    _rep.branches.return_value = ["PAIE-4322-test"]
    commit_spy = mocker.spy(_rep, "commits")

    res = _feature_applier.apply(r"PAIE-4429")
    assert commit_spy.call_count == 0, "commits should not be called"
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
