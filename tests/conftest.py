# stdlib
import shutil

# 3rd party
import pytest
from domdf_python_tools.paths import PathPlus

pytest_plugins = ("coincidence", "consolekit.testing", "tests.yaml_path")

_original_wheel_directory = PathPlus(__file__).parent / "wheels"


@pytest.fixture()
def wheel_directory(tmp_pathplus) -> PathPlus:
	wheel_dir = tmp_pathplus / "origin"
	shutil.copytree(_original_wheel_directory, wheel_dir)
	return wheel_dir


@pytest.fixture()
def fixed_version(monkeypatch):
	# 3rd party
	from airium import Airium  # type: ignore

	def get_meta_tags(page: Airium):
		# Not part of the spec, but allowed
		page.meta(name="generator", content=f"simple503 version 0.0.0")
		page.meta(charset="UTF-8")

	monkeypatch.setattr("simple503.get_meta_tags", get_meta_tags)
