# 3rd party
from coincidence import AdvancedDataRegressionFixture
from domdf_python_tools.paths import PathPlus, sort_paths

# this package
from simple503 import make_simple
from simple503.utils import cleanup


def test_cleanup(
		wheel_directory: PathPlus,
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):

	original_content = [p.relative_to(tmp_pathplus) for p in wheel_directory.iterchildren()]

	make_simple(wheel_directory)
	generated_content = [p.relative_to(tmp_pathplus) for p in wheel_directory.iterchildren()]

	cleanup(wheel_directory)
	cleaned_content = [p.relative_to(tmp_pathplus) for p in wheel_directory.iterchildren()]

	advanced_data_regression.check({
			"original_content": sort_paths(*original_content),
			"generated_content": sort_paths(*generated_content),
			"cleaned_content": sort_paths(*cleaned_content),
			})

	assert original_content == cleaned_content
