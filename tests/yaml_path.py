# stdlib
import pathlib

# 3rd party
from coincidence.regressions import _representer_for
from domdf_python_tools.paths import PathPlus
from pytest_regressions.data_regression import RegressionYamlDumper


@_representer_for(pathlib.PurePath, pathlib.Path, PathPlus)
def _represent_sequences(dumper: RegressionYamlDumper, data: pathlib.PurePath):
	return dumper.represent_data(data.as_posix())
