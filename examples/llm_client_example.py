#!/usr/bin/env python3
"""
Example demonstrating the updated LLMClient with tool call schemas and AI provider integration.
This example shows how to use the new call_tool method with different AI providers.
"""

from atp_sdk.clients import LLMClient
import json

def openai_example():
    """Example using OpenAI with the new call_tool method."""
    print("=== OpenAI Example ===")
    
    # Initialize LLMClient for OpenAI
    llm_client = LLMClient(
        api_key="YOUR_ATP_API_KEY",
        ai_provider="openai"
    )
    
    # Simulate OpenAI response with tool calls
    mock_openai_response = {
        "choices": [{
            "message": {
                "tool_calls": [
                    {
                        "id": "call_123",
                        "function": {
                            "name": "hello_world",
                            "arguments": '{"name": "Alice"}'
                        }
                    },
                    {
                        "id": "call_456", 
                        "function": {
                            "name": "get_info",
                            "arguments": '{}'
                        }
                    }
                ]
            }
        }]
    }
    
    # Execute tool calls
    try:
        results = llm_client.call_tool(
            toolkit_id="your_toolkit_id",
            tool_calls=mock_openai_response["choices"][0]["message"]["tool_calls"]
        )
        
        print("OpenAI tool calls executed successfully:")
        for result in results:
            print(f"  Tool {result['tool_call_id']}: {result['result']}")
            
    except Exception as e:
        print(f"Error executing OpenAI tool calls: {e}")

def anthropic_example():
    """Example using Anthropic with the new call_tool method."""
    print("\n=== Anthropic Example ===")
    
    # Initialize LLMClient for Anthropic
    llm_client = LLMClient(
        api_key="YOUR_ATP_API_KEY",
        ai_provider="anthropic"
    )
    
    # Simulate Anthropic response with tool use
    mock_anthropic_response = {
        "content": [{
            "tool_use": [
                {
                    "id": "use_789",
                    "name": "hello_world",
                    "input": {"name": "Bob"}
                },
                {
                    "id": "use_012",
                    "name": "get_info", 
                    "input": {}
                }
            ]
        }]
    }
    
    # Execute tool calls
    try:
        results = llm_client.call_tool(
            toolkit_id="your_toolkit_id",
            tool_calls=mock_anthropic_response["content"][0]["tool_use"]
        )
        
        print("Anthropic tool calls executed successfully:")
        for result in results:
            print(f"  Tool {result['tool_call_id']}: {result['result']}")
            
    except Exception as e:
        print(f"Error executing Anthropic tool calls: {e}")

def mistral_example():
    """Example using Mistral with the new call_tool method."""
    print("\n=== Mistral Example ===")
    
    # Initialize LLMClient for Mistral
    llm_client = LLMClient(
        api_key="YOUR_ATP_API_KEY",
        ai_provider="mistral"
    )
    
    # Simulate Mistral response with tool calls
    mock_mistral_response = {
        "choices": [{
            "message": {
                "tool_calls": [
                    {
                        "id": "call_345",
                        "name": "hello_world",
                        "arguments": {"name": "Charlie"}
                    }
                ]
            }
        }]
    }
    
    # Execute tool calls
    try:
        results = llm_client.call_tool(
            toolkit_id="your_toolkit_id",
            tool_calls=mock_mistral_response["choices"][0]["message"]["tool_calls"]
        )
        
        print("Mistral tool calls executed successfully:")
        for result in results:
            print(f"  Tool {result['tool_call_id']}: {result['result']}")
            
    except Exception as e:
        print(f"Error executing Mistral tool calls: {e}")

def real_openai_integration():
    """Example of real OpenAI integration (requires openai package)."""
    print("\n=== Real OpenAI Integration ===")
    
    try:
        import openai
        
        # Initialize LLMClient
        llm_client = LLMClient(
            api_key="YOUR_ATP_API_KEY",
            ai_provider="openai"
        )
        
        # Get toolkit context
        context = llm_client.get_toolkit_context(
            toolkit_id="your_toolkit_id",
            user_prompt="Say hello to John and get system info"
        )
        
        # Create OpenAI client
        client = openai.OpenAI(api_key="YOUR_OPENAI_API_KEY")
        
        # Define tools
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "hello_world",
                    "description": "Returns a greeting message.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Name to greet"
                            }
                        },
                        "required": ["name"]
                    }
                }
            },
            {
                "type": "function", 
                "function": {
                    "name": "get_info",
                    "description": "Returns basic system information.",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            }
        ]
        
        # Make OpenAI API call
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": "Say hello to John and get system info"}
            ],
            tools=tools,
            tool_choice="auto"
        )
        
        # Execute tool calls if any
        if response.choices[0].message.tool_calls:
            results = llm_client.call_tool(
                toolkit_id="your_toolkit_id",
                tool_calls=response.choices[0].message.tool_calls
            )
            
            print("Real OpenAI tool calls executed:")
            for result in results:
                print(f"  Tool {result['tool_call_id']}: {result['result']}")
        else:
            print("No tool calls generated by OpenAI")
            
    except ImportError:
        print("OpenAI package not installed. Install with: pip install openai")
    except Exception as e:
        print(f"Error in real OpenAI integration: {e}")

def main():
    """Run all examples."""
    print("LLMClient Tool Call Examples")
    print("=" * 50)
    
    # Run mock examples
    openai_example()
    anthropic_example()
    mistral_example()
    
    # Run real integration example
    real_openai_integration()
    
    print("\n" + "=" * 50)
    print("Examples completed!")

if __name__ == "__main__":
    main()
