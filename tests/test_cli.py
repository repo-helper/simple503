# stdlib
import shutil

# 3rd party
import pytest
from apeye import URL
from bs4 import BeautifulSoup  # type: ignore
from coincidence.regressions import AdvancedDataRegressionFixture, AdvancedFileRegressionFixture
from consolekit.testing import CliRunner
from domdf_python_tools.paths import PathPlus, sort_paths
from shippinglabel.checksum import check_sha256_hash

# this package
from simple503.__main__ import main


def test_inplace(
		wheel_directory: PathPlus,
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		cli_runner: CliRunner,
		):

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
	result = cli_runner.invoke(main, args=[wheel_directory.as_posix(), wheel_directory.as_posix()])
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
	args = [wheel_directory.as_posix(), target.as_posix()]

	if copy:
		args.append("--copy")

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
def test_to_target_sort(
		wheel_directory: PathPlus,
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		advanced_file_regression: AdvancedFileRegressionFixture,
		cli_runner: CliRunner,
		):
	target = tmp_pathplus / "target"
	result = cli_runner.invoke(main, args=[wheel_directory.as_posix(), target.as_posix(), "--sort"])
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

	base_subdir = tmp_pathplus / "subdir1"
	with_subdirs = base_subdir.joinpath("subdir2", "subdir3")
	shutil.copytree(wheel_directory, with_subdirs)

	result = cli_runner.invoke(main, args=[base_subdir.as_posix(), target.as_posix(), "--sort"])
	assert result.exit_code == 0
	assert not result.stdout

	origin_content = [p.relative_to(tmp_pathplus) for p in base_subdir.iterchildren()]
	target_content = [p.relative_to(tmp_pathplus) for p in target.iterchildren()]
	advanced_data_regression.check({
			"origin": sort_paths(*origin_content),
			"target": sort_paths(*target_content),
			})

	advanced_file_regression.check_file(target / "domdf-python-tools" / "index.html")


@pytest.mark.usefixtures("fixed_version")
def test_index_page(
		wheel_directory: PathPlus,
		advanced_file_regression: AdvancedFileRegressionFixture,
		cli_runner: CliRunner,
		):
	result = cli_runner.invoke(main, args=[wheel_directory.as_posix()])
	assert result.exit_code == 0
	assert not result.stdout

	advanced_file_regression.check_file(wheel_directory / "index.html")

	soup = BeautifulSoup((wheel_directory / "index.html").read_text(), "html.parser")

	all_anchors = soup.findAll('a')
	assert len(all_anchors) == 39

	for anchor in all_anchors:
		href = URL(anchor["href"])

		file = wheel_directory / href.path.name
		assert file.is_dir()
		assert (file / "index.html").is_file()


@pytest.mark.usefixtures("fixed_version")
def test_project_page(
		wheel_directory: PathPlus,
		advanced_file_regression: AdvancedFileRegressionFixture,
		cli_runner: CliRunner,
		):
	result = cli_runner.invoke(main, args=[wheel_directory.as_posix()])
	assert result.exit_code == 0
	assert not result.stdout

	advanced_file_regression.check_file(wheel_directory / "domdf-python-tools" / "index.html")

	soup = BeautifulSoup((wheel_directory / "domdf-python-tools" / "index.html").read_text(), "html.parser")

	all_anchors = soup.findAll('a')
	assert len(all_anchors) == 14

	for anchor in all_anchors:
		href = URL(anchor["href"])
		file = wheel_directory / href.path.name
		assert file.name.startswith("domdf_python_tools")
		assert file.suffix == ".whl"

		assert href.fragment is not None
		hash_name, hash_value = href.fragment.split('=', 1)
		assert hash_name == "sha256"
		check_sha256_hash(file, hash_value)

		metadata_file = file.with_suffix(f"{file.suffix}.metadata")
		assert metadata_file.suffix == ".metadata"
		assert metadata_file.is_file()
		metadata_hash_name, hash_value = anchor["data-dist-info-metadata"].split('=', 1)
		assert metadata_hash_name == "sha256"
		check_sha256_hash(metadata_file, hash_value)

		assert anchor["data-requires-python"] in {">=3.6.1", ">=3.6"}


@pytest.mark.usefixtures("fixed_version")
def test_project_page_no_metadata(
		wheel_directory: PathPlus,
		advanced_file_regression: AdvancedFileRegressionFixture,
		cli_runner: CliRunner,
		):
	result = cli_runner.invoke(main, args=[wheel_directory.as_posix(), "--no-extract-metadata"])
	assert result.exit_code == 0
	assert not result.stdout

	advanced_file_regression.check_file(wheel_directory / "domdf-python-tools" / "index.html")

	soup = BeautifulSoup((wheel_directory / "domdf-python-tools" / "index.html").read_text(), "html.parser")

	all_anchors = soup.findAll('a')
	assert len(all_anchors) == 14

	for anchor in all_anchors:
		href = URL(anchor["href"])
		file = wheel_directory / href.path.name
		assert file.name.startswith("domdf_python_tools")
		assert file.suffix == ".whl"

		assert href.fragment is not None
		hash_name, hash_value = href.fragment.split('=', 1)
		assert hash_name == "sha256"
		check_sha256_hash(file, hash_value)

		metadata_file = file.with_suffix(f"{file.suffix}.metadata")
		assert metadata_file.suffix == ".metadata"
		assert not metadata_file.exists()
		assert "data-dist-info-metadata" not in anchor

		assert anchor["data-requires-python"] in {">=3.6.1", ">=3.6"}
