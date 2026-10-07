from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    "mcpServers": {
        "hitung": {
            "url": "http://localhost:8000/mcp",
            "transport": "http",
            "name": "Purwa Hitung MCP Server"
        },
        "langchain": {
            "url": "https://docs.langchain.com/mcp",
            "transport": "http",
            "name": "LangChain MCP Server"
        }
    }
}


async def main():
    print("Connecting to MCP Server...")
    model = ChatOpenRouter(model="deepseek/deepseek-v4.1-flash")
    async with MCPAdapter(CONFIG) as adapter:
        tools = await adapter.list_tools()
        agent = create_agent(model, tools)
        result = await agent.ainvoke({"messages": [{"role": "user", "content": "Gimana cara implementasi react agent di langchain?"}]})
        print("Agent Response:", result["messages"][-1].content)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())