from atp_sdk.clients import ToolKitClient
from polygon import RESTClient
import os

client = ToolKitClient(
    api_key="", 
    app_name=""
)


@client.register_tool(
    function_name="get_stock_aggregates",
    params=["ticker", "multiplier", "timespan", "from_date", "to_date"],
    required_params=["ticker", "from_date", "to_date"],
    description="Get aggregate bars for a stock ticker over a date range.",
    auth_provider="polygon",
    auth_type="api_key",
    auth_with="api_key"
)
def get_stock_aggregates(**kwargs):
    ticker = kwargs.get("ticker")
    multiplier = int(kwargs.get("multiplier", 1))
    timespan = kwargs.get("timespan", "day")
    from_date = kwargs.get("from_date")
    to_date = kwargs.get("to_date")
    polygon_api_key = kwargs.get("auth_token")
    polygon_client = RESTClient(api_key=polygon_api_key)
    bars = polygon_client.list_aggs(ticker=ticker, multiplier=multiplier, timespan=timespan, from_=from_date, to=to_date)
    return {"bars": [bar._raw for bar in bars]}

@client.register_tool(
    function_name="get_last_trade",
    params=["ticker"],
    required_params=["ticker"],
    description="Get the last trade for a stock ticker.",
    auth_provider="polygon",
    auth_type="api_key",
    auth_with="api_key"
)
def get_last_trade(**kwargs):
    ticker = kwargs.get("ticker")
    polygon_api_key = kwargs.get("auth_token")
    polygon_client = RESTClient(api_key=polygon_api_key)
    trade = polygon_client.get_last_trade(ticker=ticker)
    return trade._raw

@client.register_tool(
    function_name="get_last_quote",
    params=["ticker"],
    required_params=["ticker"],
    description="Get the last quote for a stock ticker.",
    auth_provider="polygon",
    auth_type="api_key",
    auth_with="api_key"
)
def get_last_quote(**kwargs):
    ticker = kwargs.get("ticker")
    polygon_api_key = kwargs.get("auth_token")
    polygon_client = RESTClient(api_key=polygon_api_key)
    quote = polygon_client.get_last_quote(ticker=ticker)
    return quote._raw

client.start()
