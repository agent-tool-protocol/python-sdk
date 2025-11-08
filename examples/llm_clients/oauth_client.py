from atp_sdk.clients import LLMClient

llm_client = LLMClient(api_key="YOUR_ATP_LLM_CLIENT_API_KEY", protocol="https")

def main():
    # OAuth flow example

    authorization_url = llm_client.initiate_oauth_connection(
        platform_id="h7yFuHV2SbDB5nZ9YXw4uL",
        external_user_id="your_external_user_id"
    )

    print("Please visit the following URL to authorize the application:")
    print(authorization_url["auth_url"])

    # Poll for connection completion
    connection_info = llm_client.wait_for_connection(
        platform_id="h7yFuHV2SbDB5nZ9YXw4uL",
        external_user_id="your_external_user_id",
        poll_interval=5,
        timeout=300
    )

    print("OAuth connection established:", connection_info)

if __name__ == "__main__":
    main()