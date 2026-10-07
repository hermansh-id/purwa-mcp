from fastmcp import FastMCP

mcp = FastMCP("Purwa Hitung MCP Server")

@mcp.tool
def hitung_pertambahan(a: int, b: int) -> int:
    """Fungsi untuk menghitung pertambahan dua bilangan"""
    return a + b

@mcp.tool
def hitung_pengurangan(a: int, b: int) -> int:
    """Fungsi untuk menghitung pengurangan dua bilangan"""
    return a - b

if __name__ == "__main__":
    print("MCP Server is running on http://localhost:8000")
    mcp.run(transport="http", port=8000)