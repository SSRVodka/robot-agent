from langchain_openai import ChatOpenAI
from mcp import StdioServerParameters

# ────────────────────────────────────────────────────────────────────────────
# Configurations
# ────────────────────────────────────────────────────────────────────────────

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.3,
    base_url="http://localhost:17100",
    api_key="sk-dwjeifjiewrpijepwjiw")
server_params = StdioServerParameters(
    command="python",
    args=["servers/robot_mcp_server.py", "--stdio", "--grpc-host", "192.168.12.210"],
    env={"PYTHONPATH": "."},
    # args=["robot_mcp_server.py", "--stdio"]
)
