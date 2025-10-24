from openai import OpenAI
from atp_sdk.clients import LLMClient
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def print_turn(turn_type, content, prefix=""):
    separator = "=" * 50
    print(f"\n{separator}\n{turn_type} TURN:\n{prefix}{content}\n{separator}")

# --- Role Instructions ---
TOOL_PLANNER_PROMPT = {
    "role": "system",
    "content": (
        "You are the Tool Planner.\n"
        "Your ONLY job is to decide which tools to call to satisfy the user's request.\n"
        "If a tool is needed, output a function call with correct parameters.\n"
        "Do NOT answer the question directly.\n"
        "If no tool is needed, simply respond with a short explanation and no tool call."
    )
}

FINAL_RESPONDER_PROMPT = {
    "role": "system",
    "content": (
        "You are the Final Responder.\n"
        "The tools have already been executed and their results are provided.\n"
        "Your job is to craft a clear, concise natural-language answer to the user.\n"
        "Do NOT call any tools.\n"
        "Summarize the tool results and address the original question."
    )
}

# --- Clients ---
openai_client = OpenAI(api_key="YOUR_OPENAI_API_KEY_HERE")
llm_client = LLMClient(api_key="YOUR_ATP_LLM_CLIENT_API_KEY", protocol="https")

conversation_history = []  # Shared across turns


def main():
    toolkit_id = "YOUR_TOOLKIT_ID_OR_SLUG_OR_UNIQUE_NAME" # e.g., "serper_toolkit", "github_toolkit", "firecrawl_toolkit", "tavily_toolkit"
    auth_token = "YOUR_API_OR_ACCESS_TOKEN_FOR_TOOL_ACCESS" # e.g., Serper API key, GitHub token, Firecrawl API key, Tavily API key
    provider = "openai"

    print("Welcome to the Interactive ATP Terminal (OpenAI). Type your prompt or 'exit' to quit.")
    print("Example: 'Search for the Richest Man in the world.'")

    while True:
        try:
            user_prompt = input("\nYour prompt: ").strip()
            if user_prompt.lower() == "exit":
                print_turn("SYSTEM", "Exiting interactive terminal.")
                break

            if not user_prompt:
                print_turn("SYSTEM", "Please enter a non-empty prompt.")
                continue

            print_turn("USER", user_prompt)

            # --- Fetch Toolkit Context ---
            print_turn("AGENT", "Fetching toolkit context...", prefix="> ")
            context = llm_client.get_toolkit_context(
                toolkit_id=toolkit_id,
                provider=provider,
                user_prompt=user_prompt
            )

            conversation_history.append({"role": "user", "content": user_prompt})

            # --------- TOOL PLANNER STEP ---------
            print_turn("AGENT", "Generating tool plan...", prefix="> ")

            plan_response = openai_client.responses.create(
                model="gpt-3.5-turbo",
                tools=context["tools"],
                input=[TOOL_PLANNER_PROMPT] + conversation_history
            )

            # Check for tool calls
            tool_calls = [
                item for item in plan_response.output if item.type == "function_call"
            ]

            if tool_calls:
                # Append assistant's tool calls to history
                for tc in tool_calls:
                    conversation_history.append({
                        "type": "function_call",
                        "id": tc.id,
                        "call_id": tc.call_id,
                        "name": tc.name,
                        "arguments": tc.arguments
                    })

                # Log tool calls
                tool_call_summary = "\n".join(
                    f"Calling function  '{tc.name}' with parameters: {tc.arguments}"
                    for tc in tool_calls
                )
                print_turn("AGENT", f"Executing tool calls:\n{tool_call_summary}", prefix="> ")

                # --- Execute tools through ATP SDK ---
                results = llm_client.call_tool(
                    toolkit_id=toolkit_id,
                    tool_calls=tool_calls,
                    provider=provider,
                    user_prompt=user_prompt,
                    auth_token=auth_token
                )

                # Log results
                results_summary = "\n".join(
                    f"Tool '' (ID: {r['call_id']}): {r['output'][:200]}..."
                    for r in results
                )
                print_turn("AGENT", f"Tool execution results:\n{results_summary}", prefix="> ")

                # Append tool results to conversation
                for result in results:
                    conversation_history.append({
                        "type": result["type"],
                        "call_id": result["call_id"],
                        "output": result["output"]
                    })


                # --------- FINAL RESPONDER STEP ---------
                print_turn("AGENT", "Generating final response...", prefix="> ")

                final_response = openai_client.responses.create(
                    model="gpt-3.5-turbo",
                    instructions=FINAL_RESPONDER_PROMPT["content"],
                    input=conversation_history
                )

                final_content = final_response.output_text
                print_turn("AGENT", f"Final response:\n{final_content}", prefix="> ")

                conversation_history.append({"role": "assistant", "content": final_content})

            else:
                # No tool call
                direct_content = plan_response.output_text
                print_turn("AGENT", f"Direct response:\n{direct_content}", prefix="> ")
                conversation_history.append({"role": "assistant", "content": direct_content})

        except KeyboardInterrupt:
            print_turn("SYSTEM", "Exiting interactive terminal.")
            break
        except Exception as e:
            logger.error(f"Error in interactive loop: {e}")
            print_turn("SYSTEM", f"Error occurred: {str(e)}")


if __name__ == "__main__":
    main()