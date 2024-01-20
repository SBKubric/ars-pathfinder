# ARS PathFinder Microservice Specification

## General Description

This project includes a microservice gRPC server (with asyncio) that communicates via an API
specified in a [proto file](./pathfinder.proto) with a gRPC client (robot). The microservice is wrapped in Docker container and has been uploaded to Github Container Registry.
Tests have been implemented using pytest (unit tests) and manually by Postman.

## Logic of implementation

**CURRENTLY ONLY ONE ROBOT CLIENT IS SUPPORTED.**

The `SetField` RPC method is used to initialize the initial location of the robot.

The `Moving` RPC method is used to process the movement of the robot.

The `Point` message represents a point in the grid with vertical and horizontal coordinates.

The `Field` message represents the field with its height, width, grid, and the starting position of the robot.

The `MoveRequest` message contains the target points of the robot for the current iteration.

The `Motion` enum defines the possible directions of movement for the robot.

The `MoveResponse` message contains the command for the robot.

The robot understands commands to move left, right, up, down, and finish.
The robot knows which cells it needs to visit and passes them in the `MoveRequest.targets`.
When the robot arrives at a cell in `MoveRequest.targets`, it disappears.
On every `MoveResponse` from the server, the robot returns its current targets in `MoveRequest`.
The array `MoveRequest.targets` can increase, but only decreases when one of the target points is reached.
When `MoveRequest.targets` comes empty, a `FINISH` command should be sent.

The robot has a battery, and the fewer actions performed, the less battery it has left. Therefore, we can have a number of steps as a quantative metric to visualize robot perfomance and analyze battery drain.

When server receives a `MoveRequest`, it parses it and calculates the shortest path to the nearest goal.
Calculation algorithm is configured with environment variable `ALGO`. By default, `ALGO=astar[manhattan]`

### Supported algorithms

Possible alues of `ALGO` are:

-   `astar[manhattan]` (default): A\* search with Manhattan distance metric.
-   `astar[euclidean]`: A\* search with Euclidean distance metric.
-   `astar[diagonal]`: A\* search with diagonal distance metric.

Other implementations could be added by implementing `AlgorithmProtocol` and adding new class to `AlgoManager`.

The [proto file](./pathfinder.proto) specifies the structure of the messages and services that are used in the communication between the client and server.
It includes definitions for `Empty`, `PathFinder`, `Point`, `Field`, `MoveRequest`, `Motion`, and `MoveResponse`.

## Example

The provided example describes a scenario where a server is set up and ready to receive requests.

The first message received is `SetField (Field(N=5, M=4, source=Point(i=0, j=0),
grid=’01010010100001000000’))` with parameters defining the size of the field (5x4), the starting position of the robot (at the top left corner), and the layout of the field represented as a binary string.

In this case, `1` represents walls and `0` represents open spaces.

The robot itself does not occupy any space, so underneath it is marked as `0`.

Coordinates start from the top left corner, moving downwards corresponds to increasing `i`, and moving right corresponds to increasing `j`.

So, the staring position looks like this:

| 🤖  | 🪨  |     | 🪨  |
| :-: | :-: | :-: | :-: |
|     |     | 🪨  |     |
| 🪨  |     |     |     |
|     | 🪨  |     |     |
| 🪨  |     |     |     |

Next, the client opens a stream to Moving and sends a MoveRequest with three target points.
The server responds with `MoveResponse(direction=Motion.DOWN)`, indicating that the robot should move downwards.
This is considered one iteration.

State after first iteration:

|     | 🪨  |     | 🪨  |
| :-: | :-: | :-: | :-: |
| 🤖  |     | 🪨  |     |
| 🪨  |     |     | ⛳  |
|     | 🪨  |     |     |
| 🪨  | ⛳  |     | ⛳  |

After this, the client sends the same request again because the robot hasn't reached any of the targets yet.
The server then responds with `MoveResponse(direction=Motion.RIGHT)`, indicating that the robot should move to the right.

Assuming the server decided to reach the point `(2, 3)` first, when the robot is at `(2, 2)`, the server responds with RIGHT and the layout changes accordingly:

|     | 🪨  |     | 🪨  |
| :-: | :-: | :-: | :-: |
|     |     | 🪨  |     |
| 🪨  |     |     | 🤖  |
|     | 🪨  |     |     |
| 🪨  | ⛳  |     | ⛳  |

Then, during the next request to the server, the message will be without the point `(2, 3)`: `MoveRequest(targets=[Point(i=4, j=1), Point(i=4, j=3)])`. Suppose the server responded with `DOWN`. At this moment, a new target appears for the robot at `(1, 1)`. The new request to the server will be: `MoveRequest(targets=[Point(i=4, j=1), Point(i=4, j=3), Point(i=1, j=1)])`.

The view at this iteration would look like this:

|     | 🪨  |     | 🪨  |
| :-: | :-: | :-: | :-: |
|     | ⛳  | 🪨  |     |
| 🪨  |     |     |     |
|     | 🪨  |     | 🤖  |
| 🪨  | ⛳  |     | ⛳  |
