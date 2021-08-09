# stdlib
import hashlib
import shutil
from functools import partial

# 3rd party
import pytest
from airium import Airium  # type: ignore
from apeye import URL
from bs4 import BeautifulSoup  # type: ignore
from coincidence import AdvancedDataRegressionFixture, AdvancedFileRegressionFixture
from domdf_python_tools.paths import PathPlus, TemporaryPathPlus, sort_paths
from shippinglabel.checksum import check_sha256_hash

# this package
from simple503 import WheelFile, generate_project_page, make_simple


def test_inplace(
		wheel_directory: PathPlus,
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):
	make_simple(wheel_directory)

	dir_content = [p.relative_to(tmp_pathplus) for p in wheel_directory.iterchildren()]
	advanced_data_regression.check(sort_paths(*dir_content))


def test_inplace_explicit_same_target(
		wheel_directory: PathPlus,
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):
	make_simple(wheel_directory, wheel_directory)

	dir_content = [p.relative_to(tmp_pathplus) for p in wheel_directory.iterchildren()]
	advanced_data_regression.check(sort_paths(*dir_content))


def test_to_target(
		wheel_directory: PathPlus,
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):
	target = tmp_pathplus / "target"

	make_simple(wheel_directory, target)

	origin_content = [p.relative_to(tmp_pathplus) for p in wheel_directory.iterchildren()]
	target_content = [p.relative_to(tmp_pathplus) for p in target.iterchildren()]
	advanced_data_regression.check({
			"origin": sort_paths(*origin_content),
			"target": sort_paths(*target_content),
			})


@pytest.mark.usefixtures("fixed_version")
def test_to_target_move(
		wheel_directory: PathPlus,
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		advanced_file_regression: AdvancedFileRegressionFixture,
		):
	target = tmp_pathplus / "target"

	make_simple(wheel_directory, target, move=True)

	origin_content = [p.relative_to(tmp_pathplus) for p in wheel_directory.iterchildren()]
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
		):
	make_simple(wheel_directory)
	advanced_file_regression.check_file(wheel_directory / "index.html")

	soup = BeautifulSoup((wheel_directory / "index.html").read_text(), "html5lib")

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
		):
	make_simple(wheel_directory)
	advanced_file_regression.check_file(wheel_directory / "domdf-python-tools" / "index.html")

	soup = BeautifulSoup((wheel_directory / "domdf-python-tools" / "index.html").read_text(), "html5lib")

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
def test_generate_project_page(advanced_file_regression: AdvancedFileRegressionFixture):
	the_hash = hashlib.sha256()
	the_hash.update(b"hello world")

	files = [WheelFile(filename="foo.bar.whl", wheel_hash=the_hash)] * 5

	check = partial(advanced_file_regression.check, extension=".html")
	check(str(generate_project_page("Foo.Bar", files, base_url="/simple")))
	check(str(generate_project_page("Foo.Bar", iter(files), base_url="/simple")))


@pytest.mark.usefixtures("fixed_version")
def test_incremental(
		wheel_directory: PathPlus,
		tmp_pathplus: PathPlus,
		advanced_file_regression: AdvancedFileRegressionFixture,
		monkeypatch,
		):
	target = tmp_pathplus / "target"

	make_simple(wheel_directory, target, move=True)
	advanced_file_regression.check_file(target / "domdf-python-tools" / "index.html")

	# Again, with a different version but nothing else changed
	# The file should stay the same

	def get_meta_tags(page: Airium):
		# Not part of the spec, but allowed
		page.meta(name="generator", content=f"simple503 version 2.0.0")
		page.meta(charset="UTF-8")

	monkeypatch.setattr("simple503.get_meta_tags", get_meta_tags)

	make_simple(wheel_directory, target, move=True)
	advanced_file_regression.check_file(target / "domdf-python-tools" / "index.html")

	# Should have changed this time

	with TemporaryPathPlus() as tmpdir:
		try:
			shutil.move(
					str(wheel_directory / "domdf_python_tools-2.6.1-py3-none-any.whl"),
					tmpdir / "domdf_python_tools-2.6.1-py3-none-any.whl",
					)

			make_simple(wheel_directory, target, move=True)

			with pytest.raises(AssertionError, match="^FILES DIFFER:"):
				advanced_file_regression.check_file(target / "domdf-python-tools" / "index.html")

		finally:
			shutil.move(
					str(tmpdir / "domdf_python_tools-2.6.1-py3-none-any.whl"),
					wheel_directory / "domdf_python_tools-2.6.1-py3-none-any.whl",
					)


def test_unwanted_dirs(
		wheel_directory: PathPlus,
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):
	target = tmp_pathplus / "target"

	unwanted_a = (wheel_directory / ".tox/wheels/embed")
	unwanted_a.maybe_make(parents=True)

	unwanted_b = (wheel_directory / "venv/lib/python3.8/site-packages/virtualenv/wheels/embed")
	unwanted_b.maybe_make(parents=True)

	shutil.move(
			str(wheel_directory / "domdf_python_tools-2.6.1-py3-none-any.whl"),
			unwanted_a / "domdf_python_tools-2.6.1-py3-none-any.whl",
			)
	shutil.move(
			str(wheel_directory / "chardet-4.0.0-py2.py3-none-any.whl"),
			unwanted_b / "chardet-4.0.0-py2.py3-none-any.whl",
			)

	try:
		make_simple(wheel_directory, target)

		origin_content = [p.relative_to(tmp_pathplus) for p in wheel_directory.iterchildren()]
		target_content = [p.relative_to(tmp_pathplus) for p in target.iterchildren()]
		advanced_data_regression.check({
				"origin": sort_paths(*origin_content),
				"target": sort_paths(*target_content),
				})

	finally:
		shutil.move(
				str(unwanted_a / "domdf_python_tools-2.6.1-py3-none-any.whl"),
				wheel_directory / "domdf_python_tools-2.6.1-py3-none-any.whl",
				)
		shutil.move(
				str(unwanted_b / "chardet-4.0.0-py2.py3-none-any.whl"),
				wheel_directory / "chardet-4.0.0-py2.py3-none-any.whl",
				)
		unwanted_a.rmdir()
		unwanted_b.rmdir()
