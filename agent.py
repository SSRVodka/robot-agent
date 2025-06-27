# agent.py
import os
import time

from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

from prompts import *


from typing import AsyncGenerator, List, Dict, Any

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

history = [{"role": "system", "content": SYSTEM_PROMPT}]


llm = ChatOpenAI(
    # model_name="gpt-4o-mini",
    # temperature=0.3,
    # base_url="http://localhost:17100",
    # api_key="sk-dwjeifjiewrpijepwjiw")
    model_name="doubao-1.5-lite-32k-250115",
    temperature=0.3,
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key="2e43d857-5bdd-41df-99e8-eba890f7e6e9")
    # model_name="o3",
    # temperature=0.3,
    # base_url="http://ipads.chat.gpt:3006/v1",
    # api_key="sk-Tk5qmFP5JRLdsNoNA3Cc6cE967754a8984B352205755Bc20")
server_params = StdioServerParameters(
    command="python",
    args=["robot_mcp_server.py", "--stdio", "--grpc-host", "192.168.12.210"],
    # args=["robot_mcp_server.py", "--stdio"]
)

FILE_NAME = "lock"


def check_file() -> (bool, str):
    if not os.path.exists(FILE_NAME):
        return False, ""
    with open(FILE_NAME, "r") as txt:
        msg = txt.read()
        return len(msg) != 0, msg


async def run_api_agent():
    """Run agent that processes messages from API queue"""
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(llm, tools)

            while True:
                ok, user_message = check_file()
                if not ok:
                    time.sleep(1)
                    continue
                print(f"\n[Agent] Processing message: {user_message}")
                os.system("rm lock")

                # Process message through agent
                async for step in agent.astream(
                        {"messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": user_message},
                        ]},
                        stream_mode="values"):
                    step["messages"][-1].pretty_print()

                print("\n[Agent] Message processing completed")


async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(llm, tools)
            while True:
                user = input("\nUser> ")
                if user.lower() in {"exit", "quit"}:
                    break
                history.append({"role": "user", "content": user})
                async for step in agent.astream({"messages": history}, stream_mode="values"):
                    step["messages"][-1].pretty_print()


if __name__ == "__main__":
    asyncio.run(run_api_agent())
    # asyncio.run(main())
