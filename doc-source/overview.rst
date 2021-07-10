============
Overview
============

``simple503`` generates a static, :pep:`503` simple repository of Python distributions.
It takes a directory of Python :pep:`wheels <427>` and generates the necessary directories and ``index.html`` files and.
The source directory can optionally be pre-sorted by project name, or ``simple503`` can do this for you.


Example
------------

.. seealso:: An online example repository can be seen at https://repo-helper.uk/simple503/

Consider the following directory::

	simple
	├── alabaster-0.7.12-py2.py3-none-any.whl
	├── apeye-1.0.1-py3-none-any.whl
	├── appdirs-1.4.4-py2.py3-none-any.whl
	├── Babel-2.9.1-py2.py3-none-any.whl
	├── cawdrey-0.4.2-py3-none-any.whl
	├── certifi-2021.5.30-py2.py3-none-any.whl
	├── chardet-4.0.0-py2.py3-none-any.whl
	├── default_values-0.5.0-py3-none-any.whl
	├── docutils-0.16-py2.py3-none-any.whl
	├── domdf_python_tools-0.10.0-py3-none-any.whl
	├── domdf_python_tools-0.9.2-py3-none-any.whl
	└── zipp-3.4.1-py3-none-any.whl

after running ``simple503 ./simple`` the directory looks like::

	simple
	├── alabaster
	│   └── index.html
	├── alabaster-0.7.12-py2.py3-none-any.whl
	├── alabaster-0.7.12-py2.py3-none-any.whl.metadata
	├── apeye
	│   └── index.html
	├── apeye-1.0.1-py3-none-any.whl
	├── apeye-1.0.1-py3-none-any.whl.metadata
	├── appdirs
	│   └── index.html
	├── appdirs-1.4.4-py2.py3-none-any.whl
	├── appdirs-1.4.4-py2.py3-none-any.whl.metadata
	├── babel
	│   └── index.html
	├── Babel-2.9.1-py2.py3-none-any.whl
	├── Babel-2.9.1-py2.py3-none-any.whl.metadata
	├── cawdrey
	│   └── index.html
	├── cawdrey-0.4.2-py3-none-any.whl
	├── cawdrey-0.4.2-py3-none-any.whl.metadata
	├── certifi
	│   └── index.html
	├── certifi-2021.5.30-py2.py3-none-any.whl
	├── certifi-2021.5.30-py2.py3-none-any.whl.metadata
	├── chardet
	│   └── index.html
	├── chardet-4.0.0-py2.py3-none-any.whl
	├── chardet-4.0.0-py2.py3-none-any.whl.metadata
	├── default-values
	│   └── index.html
	├── default_values-0.5.0-py3-none-any.whl
	├── default_values-0.5.0-py3-none-any.whl.metadata
	├── docutils
	│   └── index.html
	├── docutils-0.16-py2.py3-none-any.whl
	├── docutils-0.16-py2.py3-none-any.whl.metadata
	├── domdf-python-tools
	│   └── index.html
	├── domdf_python_tools-0.10.0-py3-none-any.whl
	├── domdf_python_tools-0.9.2-py3-none-any.whl
	├── domdf_python_tools-0.9.2-py3-none-any.whl.metadata
	├── index.html
	├── zipp
	│   └── index.html
	├── zipp-3.4.1-py3-none-any.whl
	└── zipp-3.4.1-py3-none-any.whl.metadata

``simple503`` has created a directory for each project, and within that directory has created an ``index.html`` containing a list of wheels for that project.
A top-level ``index.html`` file has also been created, which lists all available projects.

``simple503`` can also be run with the :option:`--move <simple503 --move>` option, which will move thw wheels into the appropriate project directory::

	simple
	├── alabaster
	│   ├── alabaster-0.7.12-py2.py3-none-any.whl
	│   ├── alabaster-0.7.12-py2.py3-none-any.whl.metadata
	│   └── index.html
	├── apeye
	│   ├── apeye-1.0.1-py3-none-any.whl
	│   ├── apeye-1.0.1-py3-none-any.whl.metadata
	│   └── index.html
	├── appdirs
	│   ├── appdirs-1.4.4-py2.py3-none-any.whl
	│   ├── appdirs-1.4.4-py2.py3-none-any.whl.metadata
	│   └── index.html
	├── babel
	│   ├── Babel-2.9.1-py2.py3-none-any.whl
	│   ├── Babel-2.9.1-py2.py3-none-any.whl.metadata
	│   └── index.html
	├── cawdrey
	│   ├── cawdrey-0.4.2-py3-none-any.whl
	│   ├── cawdrey-0.4.2-py3-none-any.whl.metadata
	│   └── index.html
	├── certifi
	│   ├── certifi-2021.5.30-py2.py3-none-any.whl
	│   ├── certifi-2021.5.30-py2.py3-none-any.whl.metadata
	│   └── index.html
	├── chardet
	│   ├── chardet-4.0.0-py2.py3-none-any.whl
	│   ├── chardet-4.0.0-py2.py3-none-any.whl.metadata
	│   └── index.html
	├── default-values
	│   ├── default_values-0.5.0-py3-none-any.whl
	│   ├── default_values-0.5.0-py3-none-any.whl.metadata
	│   └── index.html
	├── docutils
	│   ├── docutils-0.16-py2.py3-none-any.whl
	│   ├── docutils-0.16-py2.py3-none-any.whl.metadata
	│   └── index.html
	├── domdf-python-tools
	│   ├── domdf_python_tools-0.10.0-py3-none-any.whl
	│   ├── domdf_python_tools-0.10.0-py3-none-any.whl.metadata
	│   ├── domdf_python_tools-0.9.2-py3-none-any.whl
	│   ├── domdf_python_tools-0.9.2-py3-none-any.whl.metadata
	│   └── index.html
	├── dom-toml
	│   ├── dom_toml-0.5.0-py3-none-any.whl
	│   ├── dom_toml-0.5.0-py3-none-any.whl.metadata
	│   └── index.html
	├── index.html
	└── zipp
	    ├── index.html
	    ├── zipp-3.4.1-py3-none-any.whl
	    └── zipp-3.4.1-py3-none-any.whl.metadata


``simple503`` also extracts ``METADATA`` files from the wheels, and exposes them per :pep:`658`.

To use the repository with pip, use the `--extra-index-url`_ option:

.. prompt:: bash

	pip install <pkg_name> --extra-index-url file:///path/to/repository/simple

Alternatively, the directory can be uploaded to a static-file hosting service, and the public https URL used instead.

.. _--extra-index-url: https://pip.pypa.io/en/stable/cli/pip_install/#install-extra-index-url
