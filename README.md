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

### Install from registry

Prerequisites: `docker, python3, make`

Just run after installing prerequisites:

```bash
make prod
```

## Stack

-   python3.11
-   pytest
-   redis
-   grpcio
-   grpcio-tools
-   black, flake8, isort (idea: switch to [ruff](), as black [could clash](https://black.readthedocs.io/en/stable/guides/using_black_with_other_tools.html#flake8) with flake8)

## Implementation

The service is listening for incoming requests.

If SetField is received, it means that robot has begun a new sequence of moves.
inside `services.field_state.set_field` we initialize `models.Entry` with new Field information and store it inside `state.state.State`, which is, in fact, a simple abstraction above Redis.

If Moving is received, it means that robot is ready to move.
If we have received no targets, we return `FINISH`.
And we call `services.field_state.moving` which retrieves current state from `state.state.State` and passes information to `pathfinder.finder.determine_direction`. After receiving direction we can inrement the steps counter.

If direction equals `FINISH` we can stop the process. So we store current step count to `models.Entry`.

The number of robots could be easily extended. To achieve that we need to add `robot_id` to `MovingRequest` and `SetField`. After that we can pass `robot_id` to `key` parameter of `set/get` methods of `state.state.State`.

Another improvement could be implementing the `redis` memoization of calculated distances.

Also more effecient algorithm could be implemented, for example, [Hub Labeling](https://www.microsoft.com/en-us/research/wp-content/uploads/2010/12/HL-TR.pdf)

## LICENSE

[GNU General Public License](./LICENSE)

## Authors

[Stanislav Bogatskiy](https://github.com/sbkubric)
