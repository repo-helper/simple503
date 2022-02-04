# stdlib
import shutil
from typing import Any, Dict

# 3rd party
import dom_toml
import pytest
from airium import Airium  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
from coincidence.regressions import AdvancedDataRegressionFixture, AdvancedFileRegressionFixture
from consolekit.testing import CliRunner
from domdf_python_tools.paths import PathPlus, in_directory, sort_paths

# this package
from simple503.__main__ import main


def test_inplace(
		wheel_directory: PathPlus,
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		cli_runner: CliRunner,
		):

	dom_toml.dump({"simple503": {}}, (tmp_pathplus / "simple503.toml"))

	with in_directory(tmp_pathplus):
		result = cli_runner.invoke(main, args=[wheel_directory.as_posix()])

	assert result.exit_code == 0
	assert not result.stdout

	dir_content = [p.relative_to(tmp_pathplus) for p in wheel_directory.iterchildren()]
	advanced_data_regression.check(sort_paths(*dir_content))


def test_inplace_explicit_same_target(
		wheel_directory: PathPlus,
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		cli_runner: CliRunner,
		):

	dom_toml.dump({"simple503": {"target": wheel_directory.as_posix()}}, (tmp_pathplus / "simple503.toml"))

	with in_directory(tmp_pathplus):
		result = cli_runner.invoke(main, args=[wheel_directory.as_posix()])

	assert result.exit_code == 0
	assert not result.stdout

	dir_content = [p.relative_to(tmp_pathplus) for p in wheel_directory.iterchildren()]
	advanced_data_regression.check(sort_paths(*dir_content))


@pytest.mark.parametrize("copy", [True, False])
def test_to_target(
		wheel_directory: PathPlus,
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		copy: bool,
		cli_runner: CliRunner,
		):

	target = tmp_pathplus / "target"
	config: Dict[str, Dict[str, Any]] = {"simple503": {"target": target.as_posix()}}

	args = [wheel_directory.as_posix()]
	if copy:
		config["simple503"]["copy"] = True

	dom_toml.dump(config, (tmp_pathplus / "simple503.toml"))

	with in_directory(tmp_pathplus):
		result = cli_runner.invoke(main, args=args)

	assert result.exit_code == 0
	assert not result.stdout

	origin_content = [p.relative_to(tmp_pathplus) for p in wheel_directory.iterchildren()]
	target_content = [p.relative_to(tmp_pathplus) for p in target.iterchildren()]
	advanced_data_regression.check({
			"origin": sort_paths(*origin_content),
			"target": sort_paths(*target_content),
			})


@pytest.mark.usefixtures("fixed_version")
def test_base_url(
		wheel_directory: PathPlus,
		tmp_pathplus: PathPlus,
		advanced_file_regression: AdvancedFileRegressionFixture,
		cli_runner: CliRunner,
		):

	target = tmp_pathplus / "target"
	config: Dict[str, Dict[str, Any]] = {
			"simple503": {"target": target.as_posix(), "base-url": "/wheelhouse"},
			}

	args = [wheel_directory.as_posix()]

	dom_toml.dump(config, (tmp_pathplus / "simple503.toml"))

	with in_directory(tmp_pathplus):
		result = cli_runner.invoke(main, args=args)

	assert result.exit_code == 0
	assert not result.stdout

	advanced_file_regression.check_file(target / "domdf-python-tools" / "index.html")


@pytest.mark.usefixtures("fixed_version")
def test_to_target_sort(
		wheel_directory: PathPlus,
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		advanced_file_regression: AdvancedFileRegressionFixture,
		cli_runner: CliRunner,
		):

	target = tmp_pathplus / "target"

	dom_toml.dump({"simple503": {
			"target": target.as_posix(),
			"sort": True,
			}}, (tmp_pathplus / "simple503.toml"))

	with in_directory(tmp_pathplus):
		result = cli_runner.invoke(main, args=[wheel_directory.as_posix()])

	assert result.exit_code == 0
	assert not result.stdout

	origin_content = [p.relative_to(tmp_pathplus) for p in wheel_directory.iterchildren()]
	target_content = [p.relative_to(tmp_pathplus) for p in target.iterchildren()]
	advanced_data_regression.check({
			"origin": sort_paths(*origin_content),
			"target": sort_paths(*target_content),
			})

	advanced_file_regression.check_file(target / "domdf-python-tools" / "index.html")


@pytest.mark.usefixtures("fixed_version")
def test_to_target_sort_subdirs(
		wheel_directory: PathPlus,
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		advanced_file_regression: AdvancedFileRegressionFixture,
		cli_runner: CliRunner,
		):
	target = tmp_pathplus / "target"

	dom_toml.dump({"simple503": {
			"target": target.as_posix(),
			"sort": True,
			}}, (tmp_pathplus / "simple503.toml"))

	base_subdir = tmp_pathplus / "subdir1"
	with_subdirs = base_subdir.joinpath("subdir2", "subdir3")
	shutil.copytree(wheel_directory, with_subdirs)

	with in_directory(tmp_pathplus):
		result = cli_runner.invoke(main, args=[base_subdir.as_posix()])

	assert result.exit_code == 0
	assert not result.stdout

	origin_content = [p.relative_to(tmp_pathplus) for p in base_subdir.iterchildren()]
	target_content = [p.relative_to(tmp_pathplus) for p in target.iterchildren()]
	advanced_data_regression.check({
			"origin": sort_paths(*origin_content),
			"target": sort_paths(*target_content),
			})

	advanced_file_regression.check_file(target / "domdf-python-tools" / "index.html")
