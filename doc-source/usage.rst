========
Usage
========

simple503
-----------

.. click:: simple503.__main__:main
	:prog: simple503
	:nested: none

.. latex:vspace:: 20px

TARGET defaults to ORIGIN, in which case the index files are generated inplace.

.. versionchanged:: 0.3.0

	Added the :option:`--copy <-c>`, :option:`--sort <-s>`, :option:`--config` options, and removed the ``--move`` option.


.. versionchanged:: 0.4.0

	Added the :option:`--no-extract-metadata <-e>` option.


Configuration File
--------------------

.. versionadded:: 0.3.0

``simple503`` can load configuration from a configuration file rather than from the command line.
The default filename is ``simple503.toml``, but this can be changed using the :option:`--config` option.
The file uses TOML_ syntax (version 0.5.0).
the The configuration should be placed in the ``simple503`` table, and the following options are available:


.. tconf:: simple503.base-url
	:type: :toml:`String`

	The base URL for the Python package repository.

	:bold-title:`Example:`

	.. code-block:: TOML

		[simple503]
		base-url = "/simple"


.. tconf:: simple503.target
	:type: :toml:`String`

	The directory to create the PEP 503 repository in.

	:bold-title:`Example:`

	.. code-block:: TOML

		[simple503]
		target = "."


.. tconf:: simple503.sort
	:type: :toml:`Boolean`

	Sort the wheel files into per-project base directories.

	:bold-title:`Example:`

	.. code-block:: TOML

		[simple503]
		sort = true


.. tconf:: simple503.copy
	:type: :toml:`Boolean`

	Copy files from the source to the destination, rather than moving them.

	:bold-title:`Example:`

	.. code-block:: TOML

		[simple503]
		copy = true


.. _TOML: https://toml.io/en/v0.5.0


All keys are optional.
Options passed on the command line take precedence over those defined in the config file.
