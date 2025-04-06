# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("sum-two-numbers")

@mcp.tool()
def add_two_numbers(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    mcp.run()