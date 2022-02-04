#!/usr/bin/env python3
#
#  config.py
"""
Configuration parser for ``simple503.toml``.
"""
#
#  Copyright © 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from typing import Any, ClassVar, Dict, List, Optional, cast

# 3rd party
from dom_toml.parser import TOML_TYPES, AbstractConfigParser
from typing_extensions import TypedDict

__all__ = ["ConfigDict", "Simple503ConfigParser"]


class ConfigDict(TypedDict):
	"""
	:class:`typing.TypedDict` representing the parsed configuration.

	.. versionadded:: 0.3.0
	"""

	base_url: str
	sort: bool
	copy: bool
	target: Optional[str]


class Simple503ConfigParser(AbstractConfigParser):
	"""
	Parser for ``simple503.toml``.

	.. versionadded:: 0.3.0
	"""

	#: The list of keys parsed from ``pyproject.toml``
	keys: List[str] = [
			"base-url",
			"sort",
			"copy",
			"target",
			]

	defaults: ClassVar[Dict[str, Any]] = {
			"sort": False,
			"copy": False,
			"base-url": '/',
			"target": None,
			}

	def parse_base_url(self, config: Dict[str, TOML_TYPES]) -> str:
		"""
		Parse the ``base-url`` key.

		**Format**: :toml:`String`

		:bold-title:`Example:`

		.. code-block:: TOML

			[simple503]
			base-url = "/simple"

		:param config: The unparsed TOML config for the ``simple503`` table.
		"""

		url = config["base-url"]
		self.assert_type(url, str, ["simple503", "base-url"])
		return url

	def parse_target(self, config: Dict[str, TOML_TYPES]) -> str:
		"""
		Parse the ``target`` key.

		**Format**: :toml:`String`

		:bold-title:`Example:`

		.. code-block:: TOML

			[simple503]
			target = "."

		:param config: The unparsed TOML config for the ``simple503`` table.
		"""

		target = config["target"]
		self.assert_type(target, str, ["simple503", "target"])
		return target

	def parse_sort(self, config: Dict[str, TOML_TYPES]) -> str:
		"""
		Parse the ``sort`` key.

		**Format**: :toml:`Boolean`

		:bold-title:`Example:`

		.. code-block:: TOML

			[simple503]
			sort = true

		:param config: The unparsed TOML config for the ``simple503`` table.
		"""

		sort = config["sort"]
		self.assert_type(sort, bool, ["simple503", "sort"])
		return sort

	def parse_copy(self, config: Dict[str, TOML_TYPES]) -> str:
		"""
		Parse the ``copy`` key.

		**Format**: :toml:`Boolean`

		:bold-title:`Example:`

		.. code-block:: TOML

			[simple503]
			copy = true

		:param config: The unparsed TOML config for the ``simple503`` table.
		"""

		copy = config["copy"]
		self.assert_type(copy, bool, ["simple503", "copy"])
		return copy

	def parse(  # type: ignore[override]
		self,
		config: Dict[str, TOML_TYPES],
		set_defaults: bool = False,
		) -> ConfigDict:
		"""
		Parse the TOML configuration.

		:param config:
		:param set_defaults: If :py:obj:`True`, the values in
			:attr:`self.defaults <dom_toml.parser.AbstractConfigParser.defaults>`
			will be set as defaults for the returned mapping.
		"""

		parsed_config = super().parse(config, set_defaults=set_defaults)
		if "base-url" in parsed_config:
			parsed_config["base_url"] = parsed_config.pop("base-url")

		return cast(ConfigDict, parsed_config)
