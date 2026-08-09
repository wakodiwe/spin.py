# spin.py

A dependency‑free loading spinner for Python 3.  Drop it in, wrap a slow
operation in a `Loader` context manager or decorator, and get a responsive,
terminal‑friendly spinner.

## Features

- Pure Python 3 (standard library only).
- Single‑module library (`src/spin/__init__.py`).
- Use as a context manager **or** as a decorator.
- Optional description text shown next to the spinner.
- Configurable frame rate (`timeout` seconds per frame).
- Sensible non‑TTY fallback (no spinner garbage when output is redirected).
- Hides/shows the cursor so the terminal stays tidy.

## Installation

Install from GitHub with [uv](https://docs.astral.sh/uv/):

```sh
uv add git+ssh://git@github.com/wakodiwe/spin.py
```

The `spin` module is now importable in that project:

```python
from spin import Loader
```

No external dependencies (standard library only).

### Local development

Clone the repo, then `make devinstall` to symlink the source into
`~/.local/lib/py/spin.py` for ad‑hoc use, or `uv sync` inside the repo to
get an editable install in a local venv.

## Usage

### Context manager

```python
from spin import Loader
from time import sleep

with Loader("installing dependencies ..."):
    sleep(5)          # replace with real work
```

### Decorator

```python
from spin import Loader

@Loader("processing ...", end="done")
def compute():
    # ... long‑running job ...
```

## API

`Loader(desc="Loading ...", end="", timeout=0.1)`

- **desc** – text shown beside the spinner (default `"Loading ..."`).
- **end** – message printed when the spinner stops (default clears the line).
- **timeout** – seconds per frame (default `0.1`, accepts decimals).

The spinner runs on a background thread and stops automatically when the
context exits or the decorated function returns.  It does nothing when
`stdout` is not a TTY.

## Demo

The following snippet demonstrates every supported usage pattern:

```python
from time import sleep
from spin import Loader


def long_job():
    sleep(1)


def other_long_job():
    sleep(1)


@Loader("Loading via decorator ...", end="decorated done.")
def decorated_job():
    sleep(2)


with Loader("", end=""):
    long_job()

with Loader("Loading 1st long job ..."):
    long_job()

with Loader("Loading 2nd long job ...", end="done."):
    other_long_job()

decorated_job()
decorated_job()
```

## Test

A quick syntax check:

```sh
make test          # runs python -m py_compile src/spin/__init__.py
```

or manually:

```sh
python -m py_compile src/spin/__init__.py
```
