# stdlib
import shutil

# 3rd party
import pytest
from domdf_python_tools.paths import PathPlus

pytest_plugins = ("coincidence", "tests.yaml_path")

_original_wheel_directory = PathPlus(__file__).parent / "wheels"


@pytest.fixture()
def wheel_directory(tmp_pathplus) -> PathPlus:
	shutil.copytree(_original_wheel_directory, tmp_pathplus / "origin")
	return tmp_pathplus / "origin"
