from atp_sdk.clients import ToolKitClient
import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

client = ToolKitClient(
    api_key="",
    app_name=""
)

@client.register_tool(
        function_name="create_company", params=['name', 'domain', 'industry'],
        required_params=['name', 'domain', 'industry'], description="For creating hubspot contact",
        auth_provider="hubspot", auth_type="OAuth2", auth_with="access_token"
)
def create_company(**kwargs):
    try:
        access_token = kwargs.get('auth_token')
        url = f"https://api.hubapi.com/crm/v3/objects/companies"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        data = {
            "properties": {
                "name": kwargs.get('name'),
                "domain": kwargs.get('domain'),
                "industry": kwargs.get('industry')
            }
        }
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    except Exception as e:
        return f"Error creating company: {str(e)}"
    

@client.register_tool(
        function_name="create_contact", params=['first_name', 'last_name', 'email', 'phone'],
        required_params=['first_name', 'last_name', 'email', 'phone'], description="For creating hubspot contact",
        auth_provider="hubspot", auth_type="OAuth2", auth_with="access_token"
)
def create_contact(**kwargs):
    try:
        access_token = kwargs.get('auth_token')
        url = f"https://api.hubapi.com/crm/v3/objects/contacts"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        data = {
            "properties": {
                "firstname": kwargs.get('first_name'),
                "lastname": kwargs.get('last_name'),
                "email": kwargs.get('email'),
                "phone": kwargs.get('phone')
            }
        }
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    except Exception as e:
        return f"Error creating contact: {str(e)}"
    

client.start()