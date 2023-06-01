#!/usr/bin/env python3
#
#  __init__.py
"""
:pep:`503` Python package repository generator.
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
import posixpath
import re
import shutil
from collections import defaultdict
from html import escape
from operator import attrgetter
from typing import TYPE_CHECKING, Callable, Dict, Iterable, List, NamedTuple, Optional, Union

# 3rd party
from airium import Airium  # type: ignore
from apeye.url import URL
from dist_meta import distributions, metadata
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike
from natsort import natsorted
from shippinglabel import normalize
from shippinglabel.checksum import get_sha256_hash
from typing_extensions import Literal

if TYPE_CHECKING:
	# stdlib
	from hashlib import _Hash
else:
	try:
		# 3rd party
		from _hashlib import HASH as _Hash
	except ImportError:  # pragma: no cover
		try:
			# 3rd party
			from _hashlib import Hash as _Hash
		except ImportError:
			pass

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2021 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.4.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = [
		"WheelFile",
		"generate_index",
		"generate_project_page",
		"make_simple",
		]


def make_simple(
		origin: PathLike,
		target: Optional[PathLike] = None,
		base_url: Union[str, URL] = '/',
		*,
		sort: bool = False,
		copy: bool = False,
		extract_metadata: bool = True,
		) -> Dict[str, List["WheelFile"]]:
	"""
	Generate a simple repository of Python wheels.

	:param origin: A directory containing wheels. The wheels may be arranged in subdirectories.
	:param target: The directory to create the repository in.
		The directory structure of ``origin`` will be recreated there.
		Defaults to ``origin``.
	:no-default target:
	:param base_url: The base URL of the simple repository.
	:param sort: Sort the wheel files into per-project base directories.
	:param copy: Copy files from the source to the destination, rather than moving them.
	:param extract_metadata: Extract and serve METADATA files per :pep:`658`.

	:returns: A mapping of (unnormalized) project names to a list of wheels for that project.

	.. versionchanged:: 0.2.0

		Now ignores wheels in the following directories: ``.git``, ``.hg``, ``.tox``, ``.tox4``,
		``.nox``, ``venv``, ``.venv``.

	.. versionchanged:: 0.3.0

		* Renamed the ``move`` option to ``sort`` to better reflect its behaviour.
		* Files are moved to the destination by default, unless the ``copy`` option is :py:obj:`True`.

	.. versionchanged:: 0.4.0  Added the ``extract_metadata`` option.
	"""

	if target is None:
		target = origin

	origin = PathPlus(origin).abspath()
	target = PathPlus(target).abspath()

	target.maybe_make(parents=True)

	projects: Dict[str, List[WheelFile]] = defaultdict(list)

	move_operation: Callable = shutil.copyfile if copy else shutil.move  # type: ignore[assignment]

	unwanted_dirs = (".git", ".hg", "venv", ".venv", ".tox", ".tox4", ".nox")
	for wheel_file in origin.iterchildren(exclude_dirs=unwanted_dirs, match="**/*.whl"):
		target_file = target / wheel_file.relative_to(origin)

		with distributions.WheelDistribution.from_path(wheel_file) as wd:
			if not wd.has_file("METADATA"):  # pragma: no cover
				raise FileNotFoundError(f"METADATA file not found in {wheel_file}")

			metadata_string = wd.read_file("METADATA")
			wheel_metadata = metadata.loads(metadata_string)

		if sort:
			# Move to the appropriate directory
			project_dir = target / normalize(wheel_metadata["Name"])
			project_dir.maybe_make()
			if wheel_file.relative_to(origin).parts[0] != project_dir.parts[-1]:
				destination = project_dir / wheel_file.name
				destination.parent.maybe_make(parents=True)
				move_operation(wheel_file, destination)
				target_file = destination

		else:
			if not target_file.is_file() or not wheel_file.samefile(target_file):
				# note: will not overwrite files with the same name, even if the source file changed
				target_file.parent.maybe_make(parents=True)
				move_operation(wheel_file, target_file)

		if extract_metadata:
			metadata_filename = target_file.with_suffix(f"{target_file.suffix}.metadata")
			metadata_filename.write_text(metadata_string)
			metadata_hash = get_sha256_hash(metadata_filename)

		else:
			metadata_hash = None

		projects[wheel_metadata["Name"]].append(
				WheelFile(
						filename=target_file.relative_to(target).as_posix(),
						wheel_hash=get_sha256_hash(target_file),
						requires_python=wheel_metadata.get("Requires-Python"),
						metadata_hash=metadata_hash,
						)
				)

	index_content = str(generate_index(projects.keys(), base_url=base_url))
	_update_file(target / "index.html", index_content)

	for project_name, project_files in projects.items():
		project_dir = target / normalize(project_name)
		project_dir.maybe_make()

		project_index = generate_project_page(
				project_name,
				natsorted(project_files, key=attrgetter("filename"), reverse=True),
				base_url,
				)

		_update_file(project_dir / "index.html", str(project_index))

	return projects


def generate_index(projects: Iterable[str], base_url: Union[str, URL] = '/') -> Airium:
	"""
	Generate the simple repository index page, containing a list of all projects.

	:param projects: The list of projects to generate links for.
	:param base_url: The base URL of the Python package repository.
		For example, with PyPI's URL, a URL of /foo/ would be https://pypi.org/simple/foo/.
	"""

	base_url = URL(base_url)
	index = Airium()

	index("<!DOCTYPE html>")
	with index.html(lang="en"):
		with index.head():
			get_meta_tags(index)

			with index.title():
				index(f"Simple Package Repository")

		with index.body():
			for project_name in natsorted(projects, key=str.lower):
				normalized_name = normalize(project_name)

				with index.a(href=f"{base_url / normalized_name}/"):
					index(project_name)
				index.br()

	return index


class WheelFile(NamedTuple):
	"""
	Represents a wheel file in the repository.
	"""

	#: The name of the wheel file.
	filename: str

	wheel_hash: "_Hash"
	"""
	The hash of the wheel file.

	Repositories SHOULD choose a hash function from one of the ones guaranteed
	to be available via the hashlib module in the Python standard library
	(currently ``md5``, ``sha1``, ``sha224``, ``sha256``, ``sha384``, ``sha512``).
	The current recommendation is to use ``sha256``.
	"""

	requires_python: Optional[str] = None
	"""
	The ``Requires-Python`` attribute from the wheel's ``METADATA`` file.

	:py:obj:`None` if undefined.
	"""

	metadata_hash: Union["_Hash", Literal[True], None] = None
	"""
	The hash of the wheel's METADATA file.

	:py:obj:`None` if the metadata file is not exposed.
	May be :py:obj:`True` if no hash is available.
	"""

	def as_anchor(self, page: Airium, base_url: Union[str, URL] = '/') -> None:
		"""
		Generate an anchor tag in a :class:`airium.Airium` document for this file.

		:param page:
		:param base_url: The base URL of the Python package repository.
		"""

		base_url = URL(base_url)

		href = f"{base_url / self.filename}#{self.wheel_hash.name.lower()}={self.wheel_hash.hexdigest()}"
		kwargs = {"href": href}

		if self.requires_python is not None:
			kwargs["data-requires-python"] = escape(self.requires_python)

		if self.metadata_hash is True:
			kwargs["data-dist-info-metadata"] = "true"
		elif self.metadata_hash is not None:
			hash_string = f"{self.metadata_hash.name.lower()}={self.metadata_hash.hexdigest()}"
			kwargs["data-dist-info-metadata"] = hash_string

		with page.a(**kwargs):
			page(posixpath.basename(self.filename))


def generate_project_page(name: str, files: Iterable[WheelFile], base_url: Union[str, URL] = '/') -> Airium:
	"""
	Generate the repository page for a project.

	:param name: The project name, e.g. ``domdf-python-tools``.
	:param files: An iterable of files for the project, which will be linked to from the index page.
	:param base_url: The base URL of the Python package repository.
		For example, with PyPI's URL, a URL of /foo/ would be https://pypi.org/simple/foo/.
	"""

	name = normalize(name)
	base_url = URL(base_url)
	page = Airium()

	page("<!DOCTYPE html>")
	with page.html(lang="en"):

		with page.head():
			get_meta_tags(page)
			with page.title():
				page(f"Links for {name}")

		with page.body():

			with page.h1():
				# Not part of the spec, but allowed
				page(f"Links for {name}")

			for wheel_file in files:
				wheel_file.as_anchor(page, base_url)
				page.br()

	return page


def get_meta_tags(page: Airium) -> None:
	# Not part of the spec, but allowed
	page.meta(name="generator", content=f"simple503 version {__version__}")
	page.meta(name="pypi:repository-version", content="1.0")
	page.meta(charset="UTF-8")


def cleanup(directory: PathLike) -> None:
	"""
	Cleanup files generated by ``simple503`` in the directory.

	This entails removing:

	* all ``index.html`` files
	* all ``.whl.metadata`` files
	* all empty directories.

	:param directory:
	"""

	directory = PathPlus(directory).abspath()

	for filename in directory.rglob("**/*"):
		if not filename.is_file():
			continue

		if filename.match("**/index.html"):
			filename.unlink()
		elif filename.match("**/*.whl.metadata"):
			filename.unlink()

	for filename in directory.rglob("**/*"):
		if not filename.is_dir():
			continue

		if next(filename.iterdir(), None) is None:
			filename.rmdir()


_minify_re = re.compile(r"\n\s*")


def _update_file(filename: PathPlus, new_content: str) -> bool:
	"""
	Write ``new_content`` to filename, but only if the content has changed.

	Requires the ``incremental`` extra (``BeautifulSoup`` and ``html5lib``), otherwise always writes.

	.. versionadded:: 0.2.0 (private)

	:param filename:
	:param new_content:

	:returns: Whether the file was updated on disk.
	"""

	try:
		# 3rd party
		from bs4 import BeautifulSoup as soup  # type: ignore
	except ImportError:  # pragma: no cover
		soup = None

	if not filename.exists() or soup is None:
		filename.write_clean(new_content)
		return True

	current_soup = soup(_minify_re.sub('', filename.read_text().strip()), "html.parser").body
	new_soup = soup(_minify_re.sub('', new_content.strip()), "html.parser").body

	if current_soup != new_soup:
		filename.write_clean(new_content)
		return True

	return False
