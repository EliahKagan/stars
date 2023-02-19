<!-- SPDX-License-Identifier: 0BSD -->

# Stars

*Querying a GitHub user’s starred repositories and their topics*

## Setup

Install with [`conda`](https://en.wikipedia.org/wiki/Conda_(package_manager))
or [`pipenv`](https://pipenv.pypa.io/en/latest/).

### conda

```sh
conda env create
conda activate stars  # To get a shell in the conda environment.
```

### pipenv

```sh
pipenv install
pipenv shell  # To get a shell in the Python virtual environment.
```

If you want to install development dependencies to support static analysis
(style checking and static type checking), run `pipenv install -d` instead of
(or in addition to) `pipenv install`.

## Usage

Open the notebook [`stars.ipynb`](stars.ipynb). I suggest VS Code, which I
used, but you can also use Jupyter Lab or any other application that supports
Jupyter notebooks.

Most of the program logic is in [`stars.py`](stars.py).

Data are cached and reused in files named
<code>starred-repos-*username*.json</code> in the current directory. These
caches never expire, but you can delete them. One such cache,
[`starred-repos-EliahKagan.json`](starred-repos-EliahKagan.json), is included
in this repository.

## License

[0BSD](https://spdx.org/licenses/0BSD.html). See [**`LICENSE`**](LICENSE).
