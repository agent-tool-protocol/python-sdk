from atp_sdk.clients import ToolKitClient
import requests
import os

client = ToolKitClient(
    api_key="", 
    app_name=""
)
base_url = "https://pro-api.coinmarketcap.com/v1"

@client.register_tool(
    function_name="get_latest_listings",
    params=["start", "limit", "convert"],
    required_params=[],
    description="Get latest cryptocurrency listings.",
    auth_provider="coinmarketcap",
    auth_type="api_key",
    auth_with="api_key"
)
def get_latest_listings(**kwargs):
    params = {
        "start": kwargs.get("start", "1"),
        "limit": kwargs.get("limit", "10"),
        "convert": kwargs.get("convert", "USD"),
    }
    cmc_api_key = kwargs.get("auth_token")
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": cmc_api_key,
    }
    response = requests.get(f"{base_url}/cryptocurrency/listings/latest", headers=headers, params=params)
    return response.json()

@client.register_tool(
    function_name="get_global_metrics",
    params=[],
    required_params=[],
    description="Get global cryptocurrency market metrics.",
    auth_provider="coinmarketcap",
    auth_type="api_key",
    auth_with="api_key"
)
def get_global_metrics(**kwargs):
    cmc_api_key = kwargs.get("auth_token")
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": cmc_api_key,
    }
    response = requests.get(f"{base_url}/global-metrics/quotes/latest", headers=headers)
    return response.json()

client.start()
