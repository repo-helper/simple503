# stdlib
from typing import Optional

# 3rd party
from docutils import nodes
from domdf_python_tools.stringlist import StringList
from sphinx.application import Sphinx  # nodep
from sphinx.config import Config
from sphinx.environment import BuildEnvironment  # nodep
from sphinx.ext.intersphinx import missing_reference

__all__ = ["handle_missing_xref", "setup"]


def handle_missing_xref(
		app: Sphinx,
		env: BuildEnvironment,
		node: nodes.Element,
		contnode: nodes.TextElement,
		) -> Optional[nodes.Node]:

	if not isinstance(node, nodes.Element):
		return

	if node.get("reftarget", '') == "_hashlib.HASH":
		node["reftype"] = "mod"
		node["reftarget"] = "hashlib"

		return missing_reference(app, env, node, contnode)


def configure(app: Sphinx, config: Config):
	"""
	Configure :mod:`sphinx_toolbox_experimental.autosummary_widths`.
	:param app: The Sphinx application.
	:param config:
	"""

	latex_elements = getattr(config, "latex_elements", {})

	latex_preamble = StringList(latex_elements.get("preamble", ''))
	latex_preamble.blankline()
	latex_preamble.append(r"\makeatletter")
	latex_preamble.append(r"\newcolumntype{\Xx}[2]{>{\raggedright\arraybackslash}p{\dimexpr")
	latex_preamble.append(r"    (\linewidth-\arrayrulewidth)*#1/#2-\tw@\tabcolsep-\arrayrulewidth\relax}}")
	latex_preamble.append(r"\makeatother")
	latex_preamble.blankline()

	latex_elements["preamble"] = str(latex_preamble)
	config.latex_elements = latex_elements


def setup(app: Sphinx):
	app.connect("config-inited", configure)
	app.connect("missing-reference", handle_missing_xref, priority=450)
