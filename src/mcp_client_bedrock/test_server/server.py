from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("sum-two-numbers")

@mcp.tool()
def add_two_numbers(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

def main():
    mcp.run()

if __name__ == "__main__":
    main()