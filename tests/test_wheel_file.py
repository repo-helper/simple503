# stdlib
import shutil

# 3rd party
import pytest
from airium import Airium  # type: ignore
from coincidence import AdvancedFileRegressionFixture
from coincidence.params import param
from domdf_python_tools.paths import PathPlus
from shippinglabel.checksum import get_sha256_hash

# this package
from simple503 import WheelFile

_wheels_glob = (PathPlus(__file__).parent / "wheels").glob("*.whl")


@pytest.fixture(params=(param(w, key=lambda t: t[0].name) for w in _wheels_glob))
def example_wheel(tmp_pathplus: PathPlus, request) -> PathPlus:
	return PathPlus(shutil.copy2(request.param, tmp_pathplus))


def test_wheel_file(
		example_wheel: PathPlus,
		tmp_pathplus: PathPlus,
		advanced_file_regression: AdvancedFileRegressionFixture,
		):

	page = Airium()

	metadata_file = tmp_pathplus / "METADATA"
	metadata_file.write_clean("Metadata-Version: 2.1")

	wf = WheelFile(filename=example_wheel.name, wheel_hash=get_sha256_hash(example_wheel))
	wf.as_anchor(page)

	wf = WheelFile(filename=example_wheel.name, wheel_hash=get_sha256_hash(example_wheel), requires_python=">=3.6")
	wf.as_anchor(page)

	wf = WheelFile(
			filename=example_wheel.name,
			wheel_hash=get_sha256_hash(example_wheel),
			requires_python="!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,>=2.7",
			)
	wf.as_anchor(page)

	wf = WheelFile(
			filename=example_wheel.name,
			wheel_hash=get_sha256_hash(example_wheel),
			requires_python=">=3.6",
			metadata_hash=get_sha256_hash(metadata_file)
			)
	wf.as_anchor(page)

	wf = WheelFile(
			filename=example_wheel.name,
			wheel_hash=get_sha256_hash(example_wheel),
			metadata_hash=get_sha256_hash(metadata_file)
			)
	wf.as_anchor(page)

	wf = WheelFile(
			filename=example_wheel.name,
			wheel_hash=get_sha256_hash(example_wheel),
			requires_python=">=3.6",
			metadata_hash=True
			)
	wf.as_anchor(page)

	advanced_file_regression.check(str(page), extension=".html")
