# Robot Agent Documentation

## Introduction

The `robot-agent` repository is designed to provide a comprehensive solution for  controlling robots through a set of tools and services. It uses the  Model Context Protocol (MCP) to communicate with robot control services, enabling efficient and flexible robot operation. This README will guide you through the main components of the repository, how to set up the  environment, and how to use the provided functionality.

## Repository Structure

Here is an overview of the main files and directories in the repository:

- **`agent.py`**: The main agent script that processes user messages and interacts with the robot control services using the MCP.
- **agent_graph.py**: Defines the graph structure for the agent, including the sub - graphs and nodes for handling different tasks.
- **`proto/`**: Contains the Protocol Buffers (gRPC standard) definition files (`robot_control.proto`) and the generated Python code (`robot_control_pb2.py`, robot_control_pb2_grpc.py) for the robot control and camera services.
- **robot_mcp_client.py**: An asynchronous client script for interacting with the MCP server.
- **robot_mcp_server.py**: The MCP server script that bridges the gRPC - based robot control services.
- **simulator.py**: A simulator script for starting a gRPC server to simulate robot control and camera services.
- **prompts.py**: Defines the system prompt for the robot control agent.
- **.gitignore**: Specifies files and directories to be ignored by Git.
- **LICENSE**: Contains the license information for the project.

## Prerequisites

- **Python**: This project is written in Python. It is recommended to use Python 3.10 or higher.
- **Dependencies**: Install the necessary Python packages by running the following command:

```bash
pip install -r requirements.txt
```

Note: The `requirements.txt` file is not provided in the given code snippets. You need to create it based on the imports in the Python files, such as `langchain_openai`, `langgraph`, `fastmcp`, `grpcio`, etc.

## Setup and Configuration

### 1. Environment Variables

You can configure the gRPC host and port for the robot control service using environment variables:

- `ROBOT_GRPC_HOST`: The host address of the gRPC server. Defaults to `localhost`.
- `ROBOT_GRPC_PORT`: The port number of the gRPC server. Defaults to `50051`.

### 2. Configuration in Python Files

- In agent.py, you can configure the language model (LLM) settings, such as the model name, temperature, base URL, and API key.

  ```python
  llm = ChatOpenAI(
      model_name="doubao-1.5-lite-32k-250115",
      temperature=0.3,
      base_url="https://ark.cn-beijing.volces.com/api/v3",
      api_key="2e43d857-5bdd-41df-99e8-eba890f7e6e9"
  )
  ```

- In `robot_mcp_server.py`, you can configure the minimum distance tolerance, orientation tolerance, and speed for the robot movement.

## Running the Application

You need to start an HTTP server first, receive messages from the phone/other agent, execute:

```shell
python external_control.py
```

You can modify the startup configuration (e.g. port, listening host address, etc.) in this file;

In another window, start ``agent.py``, which processes the messages received by the HTTP Server upwards, and calls the gRPC server on the ROS robot side downwards after reasoning, for the purpose of robot control.

```shell
python agent.py
```

If you want to run the tests in the simulator, you can change the listening address in `agent.py` to local and start `simulator.py` to give commands!



## Main Functionality

### 1. Robot Control Tools

The robot_mcp_server.py provides several tools for controlling the robot:

- **`move_to_position`**: Controls the robot to move to the specified position and orientation.
- **`get_current_position`**: Gets the coordinates of the current position of the robot.
- **`emergency_stop`**: Immediately halts all robot motion.
- **`pick_up_object`**: Picks up an object.

### 2. Agent Interaction

The agent.py script uses the LLM and the MCP tools to process user commands. It can  handle complex commands by breaking them down into sub - tasks and  calling the appropriate tools.

## License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.

## Contributing

If you want to contribute to this project, please fork the repository, make your changes, and submit a pull request.

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.

