# ARS Pathfinder

DISCLAIMER: This app was developed as technical assignment.

## Overview

The project is a asyncio gRPC server that controls movement of a robot.
Full specification is located at [SPECIFICATION.md](./SPECIFICATION.md).

## Install on your local machine

You can start the app with docker or just with plain old python. Preferred way is Docker.

### Docker

Prerequisites: `docker, python3, make`

Just run after installing prerequisites:

```bash
make init
make local
```

You have now the gRPC server listening on port 50051.

### Python

Prerequisites: `python3, make`
To start with python you need to populate your bash environment vars located in
`.envs/.local/.app`.

Then you can run:

```bash
make init
poetry run python src/main.py
```

You have now the gRPC server listening on port 50051.

## Stack

-   python3.11
-   pytest
-   redis
-   grpcio
-   grpcio-tools
-   black, flake8, isort (idea: switch to [ruff](), as black [can clash](https://black.readthedocs.io/en/stable/guides/using_black_with_other_tools.html#flake8) with flake8)

## Implementation

To be done

## Features

To be done

## LICENSE

[GNU General Public License](./LICENSE)

## Authors

[Stanislav Bogatskiy](https://github.com/sbkubric)
