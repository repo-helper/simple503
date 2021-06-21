==========
simple503
==========

.. start short_desc

**PEP 503 index generator.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/simple503/latest?logo=read-the-docs
	:target: https://simple503.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/repo-helper/simple503/workflows/Docs%20Check/badge.svg
	:target: https://github.com/repo-helper/simple503/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/repo-helper/simple503/workflows/Linux/badge.svg
	:target: https://github.com/repo-helper/simple503/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/repo-helper/simple503/workflows/Windows/badge.svg
	:target: https://github.com/repo-helper/simple503/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/repo-helper/simple503/workflows/macOS/badge.svg
	:target: https://github.com/repo-helper/simple503/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/repo-helper/simple503/workflows/Flake8/badge.svg
	:target: https://github.com/repo-helper/simple503/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/repo-helper/simple503/workflows/mypy/badge.svg
	:target: https://github.com/repo-helper/simple503/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://requires.io/github/repo-helper/simple503/requirements.svg?branch=master
	:target: https://requires.io/github/repo-helper/simple503/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/repo-helper/simple503/master?logo=coveralls
	:target: https://coveralls.io/github/repo-helper/simple503?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/repo-helper/simple503?logo=codefactor
	:target: https://www.codefactor.io/repository/github/repo-helper/simple503
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/simple503
	:target: https://pypi.org/project/simple503/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/simple503?logo=python&logoColor=white
	:target: https://pypi.org/project/simple503/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/simple503
	:target: https://pypi.org/project/simple503/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/simple503
	:target: https://pypi.org/project/simple503/
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/simple503?logo=anaconda
	:target: https://anaconda.org/domdfcoding/simple503
	:alt: Conda - Package Version

.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/simple503?label=conda%7Cplatform
	:target: https://anaconda.org/domdfcoding/simple503
	:alt: Conda - Platform

.. |license| image:: https://img.shields.io/github/license/repo-helper/simple503
	:target: https://github.com/repo-helper/simple503/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/repo-helper/simple503
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/repo-helper/simple503/v0.0.0
	:target: https://github.com/repo-helper/simple503/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/repo-helper/simple503
	:target: https://github.com/repo-helper/simple503/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2021
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/simple503
	:target: https://pypi.org/project/simple503/
	:alt: PyPI - Downloads

.. end shields

Installation
--------------

.. start installation

``simple503`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install simple503

To install with ``conda``:

	* First add the required channels

	.. code-block:: bash

		$ conda config --add channels https://conda.anaconda.org/domdfcoding

	* Then install

	.. code-block:: bash

		$ conda install simple503

.. end installation
