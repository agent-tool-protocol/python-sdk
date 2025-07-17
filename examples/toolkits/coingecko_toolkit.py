from atp_sdk.clients import ToolKitClient
from pycoingecko import CoinGeckoAPI

client = ToolKitClient(
    api_key="", 
    app_name=""
)

@client.register_tool(
    function_name="get_price",
    params=["ids", "vs_currencies"],
    required_params=["ids", "vs_currencies"],
    description="Get current price of cryptocurrencies.",
    auth_provider="coingecko",
    auth_type="api_key",
    auth_with="api_key"
)
def get_price(**kwargs):
    ids = kwargs.get("ids")  # comma-separated string of coin ids, e.g. "bitcoin,ethereum"
    vs_currencies = kwargs.get("vs_currencies")  # comma-separated string e.g. "usd,eur"
    cg_api_key = kwargs.get("auth_token")
    cg = CoinGeckoAPI(api_key=cg_api_key)
    price = cg.get_price(ids=ids.split(","), vs_currencies=vs_currencies.split(","))
    return price

@client.register_tool(
    function_name="get_coin_market_chart",
    params=["id", "vs_currency", "days"],
    required_params=["id", "vs_currency", "days"],
    description="Get historical market data for a coin.",
    auth_provider="coingecko",
    auth_type="api_key",
    auth_with="api_key"
)
def get_coin_market_chart(**kwargs):
    coin_id = kwargs.get("id")
    vs_currency = kwargs.get("vs_currency")
    days = kwargs.get("days")
    cg_api_key = kwargs.get("auth_token")
    cg = CoinGeckoAPI(api_key=cg_api_key)
    chart = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency=vs_currency, days=days)
    return chart


# now time for demo usage
@client.register_tool(
    function_name="get_demo_price",
    params=["ids", "vs_currencies"],
    required_params=["ids", "vs_currencies"],
    description="Get current price of cryptocurrencies.",
    auth_provider="coingecko",
    auth_type="api_key",
    auth_with="api_key"
)
def get_demo_price(**kwargs):
    ids = kwargs.get("ids")  # comma-separated string of coin ids, e.g. "bitcoin,ethereum"
    vs_currencies = kwargs.get("vs_currencies")  # comma-separated string e.g. "usd,eur"
    cg_api_key = kwargs.get("auth_token")
    cg = CoinGeckoAPI(demo_api_key=cg_api_key)
    price = cg.get_price(ids=ids.split(","), vs_currencies=vs_currencies.split(","))
    return price

@client.register_tool(
    function_name="get_demo_coin_market_chart",
    params=["id", "vs_currency", "days"],
    required_params=["id", "vs_currency", "days"],
    description="Get historical market data for a coin.",
    auth_provider="coingecko",
    auth_type="api_key",
    auth_with="api_key"
)
def get_demo_coin_market_chart(**kwargs):
    coin_id = kwargs.get("id")
    vs_currency = kwargs.get("vs_currency")
    days = kwargs.get("days")
    cg_api_key = kwargs.get("auth_token")
    cg = CoinGeckoAPI(demo_api_key=cg_api_key)
    chart = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency=vs_currency, days=days)
    return chart

client.start()
