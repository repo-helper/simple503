#!/usr/bin/env python3
#
#  __main__.py
"""
CLI entry point.
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
import sys
from typing import Optional

# 3rd party
import click
from consolekit import click_command
from consolekit.options import auto_default_argument, auto_default_option, flag_option
from domdf_python_tools.typing import PathLike

# this package
from simple503 import make_simple

__all__ = ["main"]


@flag_option("--cleanup", help="Cleanup files generated by simple503 in the target directory, and exit.")
@flag_option(
		"-m",
		"--move",
		type=click.STRING,
		help="Move the wheel files into the per-project base directories.",
		)
@auto_default_option(
		"-B",
		"--base-url",
		type=click.STRING,
		help="The base URL for the Python package repository.",
		)
@auto_default_argument("target", type=click.STRING)
@click.argument("origin", type=click.STRING)
@click_command()
def main(
		origin: PathLike,
		target: Optional[PathLike] = None,
		base_url: str = '/',
		move: bool = False,
		cleanup: bool = False,
		):
	"""
	Generate a PEP 503 Python package repository in TARGET for the wheels in ORIGIN.
	"""

	if cleanup:
		# this package
		from simple503.utils import cleanup as do_cleanup
		do_cleanup(target or origin)
	else:
		make_simple(origin, target, base_url=base_url, move=move)


if __name__ == "__main__":
	sys.exit(main())
