import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_auth(client: AsyncClient):
    data = {
        "First Name": "David",
        "Last Name": "Hussain",
        "username": "wownowsdnon",
        "password": "Mango#27h",
        "email": "technogoydkjsdss@gmail.com"
    }
    response = await client.post("/auth/register", data=data)
    assert response.status_code == 201
    returned_data = response.json()
    assert returned_data["username"] == data["username"].lower()
    assert "id" in returned_data

@pytest.mark.asyncio
async def test_register_duplicate_username(client: AsyncClient):
    data = {
        "First Name": "David",
        "Last Name": "Hussain",
        "username": "wownowj76",
        "password": "Mangodf#27h",
        "email": "technogdfoydsd@gmail.com"
    }
    await client.post("/auth/register", data=data)
    response = await client.post("/auth/register", data=data)
    assert response.status_code in [400, 404, 409] 

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    register_data = {
        "First Name": "David",
        "Last Name": "Hussain",
        "username": "DavidLogin",
        "password": "Password123!",
        "email": "davidlogin@example.com"
    }
    await client.post("/auth/register", data=register_data)
    login_data = {
        "username": "DavidLogin",
        "password": "Password123!",
    }
    response = await client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_protected_route_requires_auth(client: AsyncClient):
    response = await client.get("/auth/me")    
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_current_user_with_valid_token(client: AsyncClient):
    register_data = {
        "First Name": "David",
        "Last Name": "Hussain",
        "username": "David786_2",
        "password": "_Db@#12345",
        "email": "david786_2@example.com"
    }
    await client.post("/auth/register", data=register_data)
    login_data = {
        "username": "David786_2",
        "password": "_Db@#12345",
    }
    login_resp = await client.post("/auth/login", data=login_data)
    assert "access_token" in login_resp.json()
    token = login_resp.json()["access_token"]
    response = await client.get(
        "/auth/me", 
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == register_data["username"]