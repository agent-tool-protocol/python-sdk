#!/usr/bin/env python3
"""
Example demonstrating the auto-restart functionality of ToolKitClient.
This example shows how the toolkit client automatically restarts when code changes are detected.
"""

from atp_sdk.clients import ToolKitClient
import time
import logging

# Configure logging to see restart messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Initialize the toolkit client with auto-restart enabled
    client = ToolKitClient(
        api_key="YOUR_ATP_API_KEY",
        app_name="auto_restart_demo",
        auto_restart=True  # This is the default behavior
    )
    
    # Register a simple tool
    @client.register_tool(
        function_name="hello_world",
        params=['name'],
        required_params=['name'],
        description="Returns a greeting message.",
        auth_provider=None, 
        auth_type=None, 
        auth_with=None
    )
    def hello_world(**kwargs):
        name = kwargs.get('name', 'World')
        return {"message": f"Hello, {name}!", "timestamp": time.time()}
    
    # Register another tool
    @client.register_tool(
        function_name="get_info",
        params=[],
        required_params=[],
        description="Returns basic information about the system.",
        auth_provider=None,
        auth_type=None,
        auth_with=None
    )
    def get_info(**kwargs):
        return {
            "status": "running",
            "auto_restart": "enabled",
            "timestamp": time.time()
        }
    
    print("Starting toolkit client with auto-restart enabled...")
    print("The client will automatically restart when you modify this file or any Python file in the directory.")
    print("Try editing this file while it's running to see the auto-restart in action!")
    print("Press Ctrl+C to stop the client.")
    
    try:
        # Start the client
        client.start()
    except KeyboardInterrupt:
        print("\nStopping toolkit client...")
        client.stop()
        print("Client stopped.")

if __name__ == "__main__":
    main()
