import asyncio

import streamlit as st
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langchain_openrouter import ChatOpenRouter

load_dotenv()

CONFIG = {
    "mcpServers": {
        "hitung": {
            "url": "http://localhost:8000/mcp",
            "transport": "http",
        },
        "langchain": {
            "url": "https://docs.langchain.com/mcp",
            "transport": "http",
        },
    }
}

model = ChatOpenRouter(model="deepseek/deepseek-v4.1-flash")


async def ask_agent(messages: list[dict]) -> str:
    async with MCPAdapter(CONFIG) as adapter:
        tools = await adapter.list_tools()
        agent = create_agent(model, tools)
        result = await agent.ainvoke({"messages": messages})
    return result["messages"][-1].content


st.title("Purwa Hitung 🤖")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Mulai ngobrol yuk! 👇"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Mau tanya apa?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Berpikir..."):
            try:
                response = asyncio.run(ask_agent(st.session_state.messages))
            except Exception as e:
                response = f"Error: {e}"
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
