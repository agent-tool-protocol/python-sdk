# Changelog

All notable changes to the Agent Tool Protocol Python SDK will be documented in this file.

## [0.2.0] - 2024-12-19

### Added
- **Auto-restart functionality** for ToolKitClient similar to Flask/Django development servers
  - File watching for Python files in project directory
  - Automatic detection of code changes using file hashing
  - Seamless restart and tool re-registration
  - Configurable via `auto_restart` parameter (defaults to True)
- **Enhanced LLMClient** with AI provider integration
  - Support for OpenAI, Anthropic, and Mistral tool call formats
  - Automatic conversion of tool call schemas to ATP format
  - New `ai_provider` parameter for specifying the AI company
  - Batch execution of multiple tool calls
- **FileWatcher class** for monitoring code changes
  - Real-time file monitoring with configurable check intervals
  - Efficient change detection using SHA256 hashing
  - Thread-safe operation with daemon threads

### Changed
- **ToolKitClient constructor** now accepts `auto_restart` parameter
- **LLMClient constructor** now requires `ai_provider` parameter
- **LLMClient.call_tool method** completely redesigned:
  - Now accepts `tool_calls` list instead of `json_response` string
  - Returns list of results with tool_call_id tracking
  - Automatically handles different AI provider formats
  - No more manual JSON parsing required
- **Removed emojis** from logging messages for cleaner output

### Removed
- Manual JSON workflow handling in LLMClient
- `clean_json_string` function (no longer needed)
- Old `call_tool` method signature

### Breaking Changes
- `LLMClient.call_tool()` method signature changed from `(toolkit_id, json_response, ...)` to `(toolkit_id, tool_calls, ...)`
- `LLMClient` constructor now requires `ai_provider` parameter
- Return type of `call_tool()` changed from string to list of result objects

### Migration Guide
To migrate from v0.1.x to v0.2.0:

1. **Update LLMClient initialization:**
   ```python
   # Old
   llm_client = LLMClient(api_key="YOUR_KEY")
   
   # New
   llm_client = LLMClient(api_key="YOUR_KEY", ai_provider="openai")
   ```

2. **Update call_tool usage:**
   ```python
   # Old
   result = llm_client.call_tool(
       toolkit_id="toolkit_id",
       json_response=json.dumps(workflow)
   )
   
   # New
   results = llm_client.call_tool(
       toolkit_id="toolkit_id",
       tool_calls=openai_response.choices[0].message.tool_calls
   )
   ```

3. **Handle new return format:**
   ```python
   # Old
   print(result)  # String response
   
   # New
   for result in results:
       print(f"Tool {result['tool_call_id']}: {result['result']}")
   ```

### Examples
- New `examples/auto_restart_example.py` demonstrating auto-restart functionality
- New `examples/llm_client_example.py` showing AI provider integration
- Updated README with comprehensive examples for all supported AI providers

## [0.1.4] - 2024-12-18

### Added
- Initial release of Agent Tool Protocol Python SDK
- ToolKitClient for registering and serving Python functions as tools
- LLMClient for toolkit context retrieval and tool execution
- WebSocket-based communication with ATP backend
- Support for OAuth2 authentication flows
- Tool registration and execution via decorators

### Features
- Secure tool registration with API key authentication
- Real-time tool invocation via WebSocket
- Support for multiple authentication providers
- Automatic reconnection handling
- Comprehensive error handling and logging
