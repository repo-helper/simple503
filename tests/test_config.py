# stdlib
from typing import Tuple, Type

# 3rd party
import dom_toml
import pytest
from coincidence.regressions import AdvancedDataRegressionFixture

# this package
from simple503.config import Simple503ConfigParser


@pytest.mark.parametrize(
		"config",
		[
				pytest.param("[simple503]\nbase-url = '/simple'", id="base-url"),
				pytest.param("[simple503]\nbase-url = '/simple'\nsort = true", id="base-url_sort"),
				pytest.param("[simple503]\nbase-url = '/simple'\ncopy = true", id="base-url_copy"),
				pytest.param("[simple503]\nbase-url = '/simple'\nsort = false", id="base-url_sort_false"),
				pytest.param("[simple503]\nbase-url = '/simple'\ncopy = false", id="base-url_copy_false"),
				pytest.param(
						"[simple503]\nbase-url = '/simple'\ncopy = false\nextract_metadata = false",
						id="base-url_copy_false_no_extract",
						),
				pytest.param(
						"[simple503]\nbase-url = '/simple'\nsort = true\ncopy = true", id="base-url_sort_copy"
						),
				pytest.param("[simple503]\nbase-url = '/simple'\ntarget = '.'", id="target"),
				]
		)
def test_correct(config: str, advanced_data_regression: AdvancedDataRegressionFixture):

	config_file_contents = dom_toml.loads(config)

	assert "simple503" in config_file_contents

	parsed_config = Simple503ConfigParser().parse(
			config_file_contents["simple503"],
			set_defaults=True,
			)

	advanced_data_regression.check(parsed_config)


@pytest.mark.parametrize(
		"config, error",
		[
				pytest.param(
						"[simple503]\nbase-url = 123",
						(
								TypeError,
								"Invalid type for 'simple503.base-url': expected <class 'str'>, got <class 'int'>$"
								),
						id="base-url_int"
						),
				pytest.param(
						"[simple503]\nbase-url = '/simple'\nsort = 'true'",
						(
								TypeError,
								"Invalid type for 'simple503.sort': expected <class 'bool'>, got <class 'str'>$"
								),
						id="base-url_sort_string"
						),
				pytest.param(
						"[simple503]\nbase-url = '/simple'\ncopy = 'true'",
						(
								TypeError,
								"Invalid type for 'simple503.copy': expected <class 'bool'>, got <class 'str'>$"
								),
						id="base-url_copy_string"
						),
				pytest.param(
						"[simple503]\nbase-url = '/simple'\nextract_metadata = 'false'",
						(
								TypeError,
								"Invalid type for 'simple503.extract_metadata': expected <class 'bool'>, got <class 'str'>$"
								),
						id="base-url_extract_metadata_string"
						),
				]
		)
def test_errors(
		config: str,
		error: Tuple[Type[Exception], str],
		advanced_data_regression: AdvancedDataRegressionFixture,
		):

	config_file_contents = dom_toml.loads(config)

	assert "simple503" in config_file_contents

	with pytest.raises(error[0], match=error[1]):
		Simple503ConfigParser().parse(
				config_file_contents["simple503"],
				set_defaults=True,
				)
