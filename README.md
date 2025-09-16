# Agent Tool Protocol(ATP)

<p align="center">
  <img src="assets/atp.png" alt="ATP Logo" />
</p>

<p align="center">
  <strong>
  A Python SDK for registering, exposing, and serving your own Python functions as tools via the ATP platform.
  Supports secure OAuth2 flows, dynamic tool registration, and real-time tool invocation via WebSocket.
  </strong>
</p>


---

## Table of Contents

- Installation
- Quick Start
- Class: ToolKitClient
  - Constructor
  - register_tool
  - start
  - stop
- Tool Function Requirements
- WebSocket Events
- Error Handling
- Examples
- Advanced Usage
- License

---

## Installation

```sh
pip install AgentToolProtocol
```

---

## Quick Start

```python
from atp_sdk.clients import ToolKitClient
import requests

client = ToolKitClient(
    api_key="YOUR_ATP_API_KEY",
    app_name="my_app",
    auto_restart=True  # Enable auto-restart on code changes
)

@client.register_tool(
    function_name="hello_world",
    params=['name'],
    required_params=['name'],
    description="Returns a greeting.",
    auth_provider=None, auth_type=None, auth_with=None
)
def hello_world(**kwargs):
    return {"message": f"Hello, {kwargs.get('name', 'World')}!"}

client.start()
```

---

## Class: ToolKitClient

### Constructor

```python
ToolKitClient(
    api_key: str,
    app_name: str,
    base_url: str = "https://chatatp-backend.onrender.com",
    auto_restart: bool = True
)
```

**Parameters:**
- `api_key` (str): Your ATP API key.
- `app_name` (str): Name of your application.
- `base_url` (str, optional): ATP Server backend URL. Defaults to chatatp-backend.onrender.com.
- `auto_restart` (bool, optional): Enable auto-restart on code changes. Defaults to True.

---

### register_tool

Registers a Python function as a tool with the ATP platform.

```python
@client.register_tool(
    function_name: str,
    params: list[str],
    required_params: list[str],
    description: str,
    auth_provider: Optional[str],
    auth_type: Optional[str],
    auth_with: Optional[str]
)
def my_tool(**kwargs):
    ...
```

**Arguments:**
- `function_name`: Unique name for the tool.
- `params`: List of all parameter names.
- `required_params`: List of required parameter names.
- `description`: Human-readable description.
- `auth_provider`: Name of OAuth2 provider (e.g., "hubspot", "google"), or `None`.
- `auth_type`: Auth type (e.g., "OAuth2", "apiKey"), or `None`.
- `auth_with`: Name of the token parameter (e.g., "access_token", "api_key"), or `None`.

**Returns:**  
A decorator to wrap your function.

**Example:**

```python
@client.register_tool(
    function_name="create_company",
    params=['name', 'domain', 'industry'],
    required_params=['name', 'domain', 'industry'],
    description="Creates a company in HubSpot.",
    auth_provider="hubspot", auth_type="OAuth2", auth_with="access_token"
)
def create_company(**kwargs):
    access_token = kwargs.get('auth_token')
    url = "https://api.hubapi.com/crm/v3/objects/companies"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    data = {"properties": {
        "name": kwargs.get('name'),
        "domain": kwargs.get('domain'),
        "industry": kwargs.get('industry')
    }}
    response = requests.post(url, json=data, headers=headers)
    return response.json()
```

---

### start

Starts the WebSocket client and begins listening for tool requests.

```python
client.start()
```

- Keeps the main thread alive.
- Handles reconnections automatically.
- Starts file watching for auto-restart (if enabled).

---

### Auto-Restart on Code Changes

The ToolKitClient automatically monitors your Python files for changes and restarts when code is modified, similar to Flask and Django development servers.

**Features:**
- **File Watching**: Monitors all Python files in your project directory
- **Smart Detection**: Detects code changes using file hashing
- **Automatic Restart**: Restarts the toolkit client and re-registers all tools
- **Seamless Recovery**: Maintains tool registration after restart

**Example:**
```python
# Enable auto-restart (default behavior)
client = ToolKitClient(
    api_key="YOUR_API_KEY",
    app_name="my_app",
    auto_restart=True
)

# Disable auto-restart
client = ToolKitClient(
    api_key="YOUR_API_KEY", 
    app_name="my_app",
    auto_restart=False
)
```

When code changes are detected, you'll see:
```
INFO: Code change detected in /path/to/your/file.py. Restarting toolkit client...
INFO: Re-registering tools after code change...
INFO: Re-registered 3 tools
INFO: Toolkit client restarted successfully after code change
```

---

### stop

Stops the WebSocket client and closes the connection.

```python
client.stop()
```

---

## Tool Function Requirements

- Must accept all parameters as `**kwargs`.
- If your tool requires authentication, expect `auth_token` in `kwargs`.
- Return a serializable object (dict, str, etc).

---

## WebSocket Events

### Tool Registration

Upon registration, your tool is announced to the ATP backend and available for invocation.

### Tool Invocation

When a tool request is received, your function is called with the provided parameters and (if needed) `auth_token`.

**Example incoming message:**
```json
{
  "message_type": "atp_tool_request",
  "payload": {
    "request_id": "uuid",
    "tool_name": "create_company",
    "params": {"name": "Acme", "domain": "acme.com", "industry": "Tech"},
    "auth_token": "ACCESS_TOKEN"
  }
}
```

---

## Error Handling

- If your function raises an exception, the error is caught and returned as:
  ```json
  {"error": "Error message"}
  ```
- If required parameters are missing, an error is returned.
- If `auth_token` is required but missing, an error is returned.

---

## Examples

### Minimal Tool

```python
@client.register_tool(
    function_name="echo",
    params=['text'],
    required_params=['text'],
    description="Echoes the input text.",
    auth_provider=None, auth_type=None, auth_with=None
)
def echo(**kwargs):
    return {"echo": kwargs.get('text')}
```

### Tool with OAuth2

```python
@client.register_tool(
    function_name="get_contacts",
    params=[],
    required_params=[],
    description="Fetches contacts from HubSpot.",
    auth_provider="hubspot", auth_type="OAuth2", auth_with="access_token"
)
def get_contacts(**kwargs):
    access_token = kwargs.get('auth_token')
    url = "https://api.hubapi.com/crm/v3/objects/contacts"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()
```

### Tool with API Key

```python
@client.register_tool(
    function_name="get_contacts",
    params=[],
    required_params=[],
    description="Fetches contacts from HubSpot.",
    auth_provider="hubspot", auth_type="apiKey", auth_with="api_key"
)
def get_contacts(**kwargs):
    access_token = kwargs.get('auth_token')
    url = "https://api.hubapi.com/crm/v3/objects/contacts"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()
```


---

## Class: LLMClient

The `LLMClient` lets you connect to the ATP Agent Server, retrieve toolkit context, and execute tools or workflows using JSON payloads—perfect for LLM-based agents.

### Constructor

```python
from atp_sdk.clients import LLMClient

llm_client = LLMClient(
    api_key="YOUR_ATP_API_KEY",
    ai_provider="openai"  # Options: "openai", "anthropic", "mistral", etc.
)
```

---

### get_toolkit_context

Retrieves the toolkit context and system instructions for a given toolkit and user prompt.

```python
context = llm_client.get_toolkit_context(
    toolkit_id="your_toolkit_id",
    user_prompt="What do you want to achieve?"
)
```

---

### call_tool

Executes tools using tool call schemas from LLM providers (OpenAI, Anthropic, etc.).

```python
# For OpenAI
response = llm_client.call_tool(
    toolkit_id="your_toolkit_id",
    tool_calls=openai_response.choices[0].message.tool_calls
)

# For Anthropic
response = llm_client.call_tool(
    toolkit_id="your_toolkit_id", 
    tool_calls=anthropic_response.content[0].tool_use
)

# For Mistral
response = llm_client.call_tool(
    toolkit_id="your_toolkit_id",
    tool_calls=mistral_response.choices[0].message.tool_calls
)
```

**Parameters:**
- `toolkit_id` (str): ID of the toolkit to execute.
- `tool_calls` (list): List of tool call objects from LLM response.
- `auth_token` (str, optional): Authentication token for the request.
- `user_prompt` (str, optional): User prompt to include in the request.
- `timeout` (int, optional): Timeout for the request in seconds. Default is 120.

**Returns:**
- `list`: List of tool execution results with tool_call_id and result.

**Supported AI Providers:**
- **OpenAI**: Automatically converts `tool_calls` format
- **Anthropic**: Automatically converts `tool_use` format  
- **Mistral**: Automatically converts `tool_calls` format
- **Generic**: Supports other providers with flexible conversion

---

## Example: Using LLMClient with OpenAI, Anthropic, and Mistral AI

You can use any LLM to generate the JSON workflow, then execute each step with `LLMClient`.

### 1. OpenAI (GPT-4o)

```python
import openai
from atp_sdk.clients import LLMClient

client = openai.OpenAI(api_key="YOUR_OPENAI_API_KEY")
llm_client = LLMClient(api_key="YOUR_ATP_API_KEY")

# Get toolkit context and system prompt
context = llm_client.get_toolkit_context(toolkit_id="your_toolkit_id", user_prompt="Create a company and then list contacts.")

# Use OpenAI to generate the workflow JSON
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": context},
        {"role": "user", "content": "Create a company and then list contacts."}
    ],
    tools=[...],  # Your tool definitions
    tool_choice="auto"
)

# Execute tool calls directly
if response.choices[0].message.tool_calls:
    results = llm_client.call_tool(
        toolkit_id="your_toolkit_id",
        tool_calls=response.choices[0].message.tool_calls
    )
    print(results)
```

### 2. Anthropic (Claude)

```python
import anthropic
from atp_sdk.clients import LLMClient

llm_client = LLMClient(api_key="YOUR_ATP_API_KEY")
context = llm_client.get_toolkit_context(toolkit_id="your_toolkit_id", user_prompt="...")

client = anthropic.Anthropic(api_key="YOUR_ANTHROPIC_API_KEY")
response = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": context}
    ],
    tools=[...],  # Your tool definitions
    tool_choice="auto"
)

# Execute tool calls directly
if response.content[0].tool_use:
    results = llm_client.call_tool(
        toolkit_id="your_toolkit_id",
        tool_calls=response.content[0].tool_use
    )
    print(results)
```

### 3. Mistral AI

```python
from mistralai.client import MistralClient
from atp_sdk.clients import LLMClient

llm_client = LLMClient(api_key="YOUR_ATP_API_KEY")
context = llm_client.get_toolkit_context(toolkit_id="your_toolkit_id", user_prompt="...")

client = MistralClient(api_key="YOUR_MISTRAL_API_KEY")
response = client.chat(
    model="mistral-large-latest",
    messages=[{"role": "user", "content": context}],
    tools=[...],  # Your tool definitions
    tool_choice="auto"
)

# Execute tool calls directly
if response.choices[0].message.tool_calls:
    results = llm_client.call_tool(
        toolkit_id="your_toolkit_id",
        tool_calls=response.choices[0].message.tool_calls
    )
    print(results)
```

---

## Handling Tool Calls

The `call_tool` method automatically handles multiple tool calls from LLM responses:

```python
# OpenAI example
response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[...],
    tools=[...],
    tool_choice="auto"
)

# Execute all tool calls
if response.choices[0].message.tool_calls:
    results = llm_client.call_tool(
        toolkit_id="your_toolkit_id",
        tool_calls=response.choices[0].message.tool_calls
    )
    
    # Results contain tool_call_id and result for each tool
    for result in results:
        print(f"Tool {result['tool_call_id']}: {result['result']}")
```

**Features:**
- **Batch Execution**: Handles multiple tool calls in a single request
- **Provider Agnostic**: Automatically converts different AI provider formats
- **Result Tracking**: Each result includes the original tool_call_id
- **Error Handling**: Individual tool failures don't stop other executions

---

## Example: Full Workflow

```python
from atp_sdk.clients import LLMClient
import openai

llm_client = LLMClient(api_key="YOUR_ATP_API_KEY", ai_provider="openai")
context = llm_client.get_toolkit_context(toolkit_id="your_toolkit_id", user_prompt="...")

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": context},
        {"role": "user", "content": "Do a multi-step task."}
    ],
    tools=[...],  # Your tool definitions
    tool_choice="auto"
)

# Execute tool calls directly
if response.choices[0].message.tool_calls:
    results = llm_client.call_tool(
        toolkit_id="your_toolkit_id",
        tool_calls=response.choices[0].message.tool_calls
    )
    print(results)
else:
    print("No tool calls generated")
```

---

**Tip:**  
The LLMClient automatically converts tool call formats from different AI providers. Just pass the tool_calls directly from your LLM response.

---

## Advanced Usage

### Auto-Restart Configuration

```python
# Enable auto-restart with custom file watching
client = ToolKitClient(
    api_key="YOUR_API_KEY",
    app_name="my_app",
    auto_restart=True
)

# Disable auto-restart for production
client = ToolKitClient(
    api_key="YOUR_API_KEY",
    app_name="my_app",
    auto_restart=False
)
```

### Custom Backend

```python
client = ToolKitClient(
    api_key="YOUR_API_KEY",
    app_name="my_app",
    base_url="https://your-backend.example.com"
)
```

### Multiple Tools

```python
@client.register_tool(...)
def tool1(**kwargs): ...

@client.register_tool(...)
def tool2(**kwargs): ...
```

### AI Provider Integration

```python
# OpenAI integration
llm_client = LLMClient(api_key="YOUR_ATP_API_KEY", ai_provider="openai")

# Anthropic integration  
llm_client = LLMClient(api_key="YOUR_ATP_API_KEY", ai_provider="anthropic")

# Mistral integration
llm_client = LLMClient(api_key="YOUR_ATP_API_KEY", ai_provider="mistral")

# Custom provider
llm_client = LLMClient(api_key="YOUR_ATP_API_KEY", ai_provider="custom")
```

---

## License

MIT License.  
See LICENSE for details.

---

## Feedback & Issues

For bug reports or feature requests, please open an issue on [GitHub](https://github.com/agent-tool-protocol/python-sdk/).

---

**Happy coding! 🚀**