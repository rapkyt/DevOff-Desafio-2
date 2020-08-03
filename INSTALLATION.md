
## Table of Contents

-   [Install](#install)
-   [Usage](#usage)
-   [Maintainers](#maintainers)
-   [Contributing](#contributing)
-   [License](#license)


## Install

### System Requirements

<!-- NOTE: Keep this list alphabetized. -->

-   [Black]
-   [Docker]
-   [Git]
-   [Poetry]
-   [Prettier]
-   [Pyenv]
-   [Python]
-   [Virtualenv]

## Setup

```bash
# STEP 1: Various chores...
# NOTE: `pyenv local` Should output -> 3.6.8
$ pyenv local

# STEP 2: Create and activate local virtualenv.
$ virtualenv .venv  --python=python3.6
$ source .venv/bin/activate

# STEP 3: Install local Python packages.
$ poetry install

# STEP 4: Build local container(s).
$ klak build

# STEP 5: Spin-up local container(s).
$ klak up

# STEP 6: Initialize local container state.
$ klak init

# STEP 7: Create default user
$ klak django admin create_superuser
```

## Usage

### Local Automation

This project leverages a small library called [Klak] to consume a Python file called a [Clickfile](./Clickfile). See the [Klak] for more info.

Run `--help` options to see all available commands and usage:

```bash
# NOTE: See top-level help
klak --help

# NOTE: See command group help
klak <command> --help

# NOTE: See command group, sub-command help
klak <command> <command> --help
```

### Local Development

Running this project requires **two** terminal sessions.

Development server:

```bash
$ source .venv/bin/activate

# NOTE: Spin-up local containers.
$ klak up

# NOTE: Start local dev server.
$ klak serve
```


Site is available at:

| Page        | Link                                |
| :---------- | :---------------------------------- |
| Index       | <http://localhost:8000>             |


## OS Support

This boilerplate and local tooling has been tested on:

-   ✓ MacOS (last tested on 10.14.5)
-   ✘ Windows (Need help on this, want to volunteer?)
-   ✘ Linux (Need help on this, want to volunteer?)

## Maintainers

-   [Cristian Mora](https://github.com/rapkyt/)

## Contributing

See [the contributing file](CONTRIBUTING.md)! it's really important

PRs accepted.

Small note: If editing the README, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

<!-- Links -->
<!-- Please keep this list alphabetized. -->

[black]: "https://github.com/python/black" "Black"
[docker]: "https://docs.docker.com/docker-for-mac/install/" "Docker"
[git]: "https://git-scm.com/" "Git"
[klak]: https://pypi.org/project/klak/ "Klak"
[poetry]: "https://poetry.eustace.io/docs/" "Poetry"
[prettier]: "https://prettier.io/"
[pyenv]: "https://github.com/pyenv/pyenv" "Pyenv"
[python]: "https://www.python.org/" "Python"
[virtualenv]: "https://virtualenv.pypa.io/en/stable/" "Virtualenv"

<!-- End Links -->
