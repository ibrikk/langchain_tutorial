import asyncio
from urllib.parse import urlencode

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

# Construct server URL with authentication
base_url = "https://server.smithery.ai/@meowhuman/weather/mcp"
params = {"api_key": "eb788121-fd30-4502-8768-3b32d2719f47"}
url = f"{base_url}?{urlencode(params)}"

async def main():
    async with streamablehttp_client(url) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print(f"✅ Available tools: {', '.join([t.name for t in tools_result.tools])}")

            # Call the tool (likely name is "get_weather")
            if "get_weather" in [t.name for t in tools_result.tools]:
                result = await session.call_tool("get_weather", {"location": "Baltimore"})
                print(f"🌤️ Weather: {result}")
            else:
                print("❌ Tool 'get_weather' not found.")

if __name__ == "__main__":
    asyncio.run(main())
