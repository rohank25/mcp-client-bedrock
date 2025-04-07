# Hello World


## TODO
- add tests
- create proper data models
- implement tool usage
- separate MCP client from MCP Host (Bedrock Agent) code
- multi agent orchestration
    - host -> multi mcp client -> multi mcp server



## refactor
```
    chat = BedrockConversation()
    chat.tools = BedrockToolManager()

    async with mcp_client_ctx:
        init_tools

        while input is not exit:
            response = chat.invoke(input)

            if stop_reason is "end_turn":
                print(response)
            if stop_reason is "tool_use":
                print("Tool use requested")
                tool_use_id = response['output']['message']['content'][0]['toolUse']['toolUseId']
                tool_name = response['output']['message']['content'][0]['toolUse']['name']
                params = response['output']['message']['content'][0]['toolUse']['input']
                tool_response = await session.call_tool(tool_name, params)
                response = chat.invoke(tool_response)
                print(f"Tool response: {tool_response}")
```