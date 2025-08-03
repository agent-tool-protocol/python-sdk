from atp_sdk.clients import LLMClient
import logging

logging.basicConfig(level=logging.INFO)

llm_client = LLMClient(api_key="123")

try:
    toolkit_context = llm_client.get_toolkit_context(
        toolkit_id="BQYtqbMqbzu9XGuiXmpC8U",
        user_prompt="How can I use this toolkit?"
    )
    print(toolkit_context)
except Exception as e:
    print(f"Error: {e}")