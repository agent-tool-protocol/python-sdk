import os
import requests
from dotenv import load_dotenv
from atp_sdk.clients import ToolKitClient

load_dotenv()

client = ToolKitClient(
    api_key="",
    app_name=""
)

@client.register_tool(
    function_name="get_github_repos",
    params=['username'],
    required_params=['username'],
    description="Fetches public repositories for a specified GitHub username.",
    auth_provider="github", auth_type="OAuth2", auth_with="access_token"
)
def get_github_repos(**kwargs):
    try:
        access_token = kwargs.get('auth_token')
        username = kwargs.get('username')
        url = f"https://api.github.com/users/{username}/repos"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@client.register_tool(
    function_name="get_private_github_repos",
    params=[],
    required_params=[],
    description="Fetches private repositories for the authenticated user.",
    auth_provider="github", auth_type="OAuth2", auth_with="access_token"
)
def get_private_github_repos(**kwargs):
    try:
        access_token = kwargs.get('auth_token')
        url = "https://api.github.com/user/repos"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@client.register_tool(
    function_name="create_github_repo",
    params=['name', 'description'],
    required_params=['name', 'description'],
    description="Creates a new public GitHub repository.",
    auth_provider="github", auth_type="OAuth2", auth_with="access_token"
)
def create_github_repo(**kwargs):
    try:
        access_token = kwargs.get('auth_token')
        url = "https://api.github.com/user/repos"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "name": kwargs.get('name'),
            "description": kwargs.get('description')
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@client.register_tool(
    function_name="delete_github_repo",
    params=['repo_id'],
    required_params=['repo_id'],
    description="Deletes a GitHub repository.",
    auth_provider="github", auth_type="OAuth2", auth_with="access_token"
)
def delete_github_repo(**kwargs):
    try:
        access_token = kwargs.get('auth_token')
        url = f"https://api.github.com/repos/{kwargs.get('repo_id')}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.delete(url, headers=headers)
        return {"status_code": response.status_code, "message": "Deleted" if response.status_code == 204 else response.text}
    except Exception as e:
        return {"error": str(e)}


@client.register_tool(
    function_name="update_github_repo",
    params=['repo_id', 'name', 'description'],
    required_params=['repo_id', 'name', 'description'],
    description="Updates a GitHub repository.",
    auth_provider="github", auth_type="OAuth2", auth_with="access_token"
)
def update_github_repo(**kwargs):
    try:
        access_token = kwargs.get('auth_token')
        url = f"https://api.github.com/repos/{kwargs.get('repo_id')}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "name": kwargs.get('name'),
            "description": kwargs.get('description')
        }
        response = requests.patch(url, headers=headers, json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@client.register_tool(
    function_name="create_github_issue",
    params=['repo_id', 'title', 'body'],
    required_params=['repo_id', 'title', 'body'],
    description="Creates a new GitHub issue in a repository.",
    auth_provider="github", auth_type="OAuth2", auth_with="access_token"
)
def create_github_issue(**kwargs):
    try:
        access_token = kwargs.get('auth_token')
        url = f"https://api.github.com/repos/{kwargs.get('repo_id')}/issues"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "title": kwargs.get('title'),
            "body": kwargs.get('body')
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@client.register_tool(
    function_name="create_github_pull_request",
    params=['repo_id', 'title', 'body'],
    required_params=['repo_id', 'title', 'body'],
    description="Creates a new GitHub pull request in a repository.",
    auth_provider="github", auth_type="OAuth2", auth_with="access_token"
)
def create_github_pull_request(**kwargs):
    try:
        access_token = kwargs.get('auth_token')
        url = f"https://api.github.com/repos/{kwargs.get('repo_id')}/pulls"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "title": kwargs.get('title'),
            "body": kwargs.get('body'),
            "head": "main",  # You may want to make `head` and `base` dynamic
            "base": "main"
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@client.register_tool(
    function_name="create_github_release",
    params=['repo_id', 'tag_name', 'name', 'body'],
    required_params=['repo_id', 'tag_name', 'name', 'body'],
    description="Creates a new GitHub release in a repository.",
    auth_provider="github", auth_type="OAuth2", auth_with="access_token"
)
def create_github_release(**kwargs):
    try:
        access_token = kwargs.get('auth_token')
        url = f"https://api.github.com/repos/{kwargs.get('repo_id')}/releases"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "tag_name": kwargs.get('tag_name'),
            "name": kwargs.get('name'),
            "body": kwargs.get('body')
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@client.register_tool(
    function_name="create_github_label",
    params=['repo_id', 'name', 'color'],
    required_params=['repo_id', 'name', 'color'],
    description="Creates a new GitHub label in a repository.",
    auth_provider="github", auth_type="OAuth2", auth_with="access_token"
)
def create_github_label(**kwargs):
    try:
        access_token = kwargs.get('auth_token')
        url = f"https://api.github.com/repos/{kwargs.get('repo_id')}/labels"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "name": kwargs.get('name'),
            "color": kwargs.get('color')
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@client.register_tool(
    function_name="create_github_milestone",
    params=['repo_id', 'title', 'description'],
    required_params=['repo_id', 'title', 'description'],
    description="Creates a new GitHub milestone in a repository.",
    auth_provider="github", auth_type="OAuth2", auth_with="access_token"
)
def create_github_milestone(**kwargs):
    try:
        access_token = kwargs.get('auth_token')
        url = f"https://api.github.com/repos/{kwargs.get('repo_id')}/milestones"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "title": kwargs.get('title'),
            "description": kwargs.get('description')
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

client.start()