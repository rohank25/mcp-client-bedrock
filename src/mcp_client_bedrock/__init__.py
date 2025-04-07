from .client import ChatClient
import asyncio
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from mcp_client_bedrock.tools import BedrockToolManager

def main():
    server_params = StdioServerParameters(
        command = "uv",
        args=["run", "mcp-test-server"]
    )

    asyncio.run(
        connect(server_params)
    )

async def connect(params):
    async with stdio_client(params) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            await session.initialize()

            tools = await session.list_tools()
            # print(tools.tools)

            tool_manager = BedrockToolManager()
            [tool_manager.add_tool(
                name=tool.name,
                desc=tool.description,
                schema= {
                    'json': tool.inputSchema
                }
            ) for tool in tools.tools]
            # print(tool_manager)

            chat = ChatClient(
                aws_profile = "dio",
                aws_region = "us-east-1",
                model = "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
                tools = tool_manager
            )

            chat.start()


if __name__ == "__main__":
    main()