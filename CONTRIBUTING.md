# Contributing to Command Line Todo App

## Development Environment

Command Line Todo App uses [poetry](https://python-poetry.org/docs/) for packaging and
dependency management. To start developing with Command Line Todo App, install Poetry
using the [recommended method](https://python-poetry.org/docs/#installation) or run:

```
pip install poetry
```

Once Poetry is installed, install the dependencies with the following command:

```
poetry install
```

Poetry uses virtual environments and handles those for you efficiently.

If you want to have a shell in the virtual environment you can activate it with (for Linux/MacOS):

```
. $(poetry env info --path)/bin/activate
```

The package is linked in editable mode so you will not need to reinstall the package when changing something.

Alternatively you can run things in the virtual environment by using a `poetry run` prefix for commands, e.g.:

```
poetry run pytest
```

**The following section commands assume you are in the poetry installed environment by either activating or prefixing commands with `poetry run`!**

### Pre-Commit-Hooks

Pre commit hooks can be setup with:

```
pre-commit install
```

### Tests

Run tests with the following command:

```
pytest --cov-report term-missing --cov=todo tests/ -vv
```

New code should ideally have tests and not break existing tests.

### Type Checking

Command Line Todo App uses type annotations throughout, and `mypy` to do the checking. Run the following to type check Command Line Todo App:

```
mypy --ignore-missing-imports --no-implicit-optional --warn-unreachable
```

### Code Formatting

Command Line Todo App uses [`black`](https://github.com/psf/black) for code formatting.
I recommend setting up black in your editor to format on save.

To run black from the command line, use `black --check .` to check your formatting,
and use `black .` to also apply all diffs.
