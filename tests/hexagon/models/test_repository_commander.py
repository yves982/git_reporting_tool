import uuid

import pytest

from hexagon.gateway import IRepositoryCommander
from hexagon.models import Commit, CherryPickResult
from hexagon.use_cases import Repository

_rep: Repository | None = None
_repository_commander: IRepositoryCommander | None = None


@pytest.fixture()
def repo_commander(mocker):
    commander = mocker.patch('hexagon.gateway.repository_commander.IRepositoryCommander')
    global _repository_commander
    _repository_commander = commander.return_value
    return _repository_commander


@pytest.fixture(autouse=True)
def setup(repo_commander):
    global _rep
    _rep = Repository(None, repo_commander)


@pytest.fixture
def cherry_pick_commit_id():
    return uuid.uuid4()


@pytest.fixture
def cherry_pick_target_branch():
    return "master"


@pytest.mark.repository
@pytest.mark.repository_commander
def test_repository_commander_cherry_pick(cherry_pick_commit_id, cherry_pick_target_branch):
    # Arrange
    _repository_commander.cherry_pick.return_value = \
        CherryPickResult(True,
                         Commit(uuid.uuid4(), f"cherry picked from commit {cherry_pick_commit_id}"))

    # Act
    result = _rep.cherry_pick(cherry_pick_commit_id, cherry_pick_target_branch, True)

    # Assert
    assert result.success
    assert result.new_commit.message == f"cherry picked from commit {cherry_pick_commit_id}"
