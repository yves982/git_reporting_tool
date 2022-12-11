import re
import uuid
from datetime import datetime, timedelta
from itertools import product
from typing import List

import pytest

from hexagon.gateway import IRepositoryReader
from hexagon.models import Commit
from hexagon.use_cases import Repository
from tests.helpers import assert_collection_equivalent

_rep: Repository | None = None
_repository_reader: IRepositoryReader | None = None


@pytest.fixture()
def repo_reader(mocker):
    reader = mocker.patch('hexagon.gateway.IRepositoryReader')
    global _repository_reader
    _repository_reader = reader.return_value
    return _repository_reader


@pytest.fixture(autouse=True)
def setup(repo_reader):
    global _rep
    _rep = Repository(repo_reader, None)


@pytest.fixture()
def expected_branches():
    return ["toto", "tintin", "tata"]


@pytest.mark.repository
def test_repository_list_branches(expected_branches):
    # Arrange
    _repository_reader.branches.return_value = expected_branches

    # Act
    branches = _rep.branches()

    # Assert
    assert_collection_equivalent(branches, expected_branches, "branches", _str_comparer)
    _repository_reader.branches.assert_called_with()


@pytest.mark.repository
def test_repository_list_branches_reader_throws_propagated():
    # Arrange
    _repository_reader.branches.side_effect = ConnectionError("server not found")

    # Act
    with pytest.raises(ConnectionError) as exec_info:
        _rep.branches()

    # Assert
    assert exec_info.value.args[0] == "server not found"


def _str_comparer(first: str, second: str):
    if first > second:
        return 1
    elif first < second:
        return -1
    else:
        return 0


def _compare_commits_by_message(first: Commit, second: Commit):
    return _str_comparer(first.message, second.message)


def _compare_commits_by_id(first: Commit, second: Commit):
    return _str_comparer(str(first.id), str(second.id))


@pytest.fixture()
def expected_commits():
    base_date = datetime(2020, 1, 1)
    return [Commit(uuid.uuid4(), f"commit num {index + 1}", base_date + timedelta(days=2))
            for index, _ in enumerate(range(4))]


@pytest.fixture()
def branch_name():
    return "toto"


@pytest.mark.repository
def test_repository_commits_by_branch(expected_commits, branch_name):
    # Arrange
    _repository_reader.commits.return_value = expected_commits

    # Act
    commits = _rep.commits(branch_name)

    # Assert
    assert_collection_equivalent(commits, expected_commits, "commits", _compare_commits_by_id)
    _repository_reader.commits.assert_called_with(branch_name)


@pytest.mark.repository
def test_repository_commits_for_empty_branch_throws():
    # Act
    with pytest.raises(ValueError) as exec_info:
        _rep.commits("")

    # Assert
    assert exec_info.value.args[0] == "branch name cannot be empty or none", "empty branch name was not handled!"

    # Act
    with pytest.raises(ValueError) as exec_info:
        _rep.commits(None)

    # Assert : we can have multiple assertions per test if they're closely related and we provide proper descriptions
    assert exec_info.value.args[0] == "branch name cannot be empty or none", "None branch name was not handled!"


@pytest.mark.repository
def test_repository_commits_reader_throws_propagated():
    # Arrange
    _repository_reader.commits.side_effect = ConnectionError("server not found")

    # Act
    with pytest.raises(ConnectionError) as exec_info:
        _rep.commits("toto")

    # Assert
    assert exec_info.value.args[0] == "server not found"


@pytest.fixture
def filtered_branch_name():
    return "master"


@pytest.fixture
def filtered_all_commits():
    base_date = datetime.utcnow()
    messages = [f"{name} {position} commit" for name, position in
                product(["JACK", "JOE", "ALINE"], ["first", "second"])]
    filtered_commits = [Commit(uuid.uuid4(), messages[index], base_date + timedelta(days=2)) for index in range(6)]
    return filtered_commits


def expected_filtered_commits(filtered_returned_commits: List[Commit], pattern: str):
    return [commit for commit in filtered_returned_commits if
            re.match(pattern, commit.message) is not None]


@pytest.mark.repository
def test_repository_filter_commits_by_pattern(filtered_branch_name, filtered_all_commits):
    # Arrange
    _repository_reader.commits.return_value = filtered_all_commits
    expected_commits = expected_filtered_commits(filtered_all_commits, ".*JOE.+")

    # Act
    filtered_commits = _rep.filter_commits(filtered_branch_name, ".*JOE.+")

    # Assert
    assert_collection_equivalent(filtered_commits, expected_commits, "commit", _compare_commits_by_message)


@pytest.mark.repository
def test_repository_filter_non_matching_pattern_empty_result(filtered_branch_name, filtered_all_commits):
    # Arrange
    _repository_reader.commits.return_value = filtered_all_commits
    expected_commits = []

    # Act
    filtered_commits = _rep.filter_commits(filtered_branch_name, "zz.+")

    # Assert
    assert_collection_equivalent(filtered_commits, expected_commits, "commit", _compare_commits_by_id)


@pytest.mark.repository
def test_repository_filter_invalid_regex_throws(filtered_branch_name, filtered_all_commits):
    # Act
    with pytest.raises(re.error) as exec_info:
        _rep.filter_commits(filtered_branch_name, "**")
    # Assert
    assert str(exec_info.value.args[0]).__contains__("nothing to repeat")


@pytest.mark.repository
@pytest.mark.optional
def test_repository_repr():
    utcnow = datetime.utcnow()
    commit = Commit(uuid.uuid4(), "toto", utcnow)
    assert commit.__repr__() == f"{commit.id}(toto) on {utcnow.strftime('%Y-%m-%d')}"
