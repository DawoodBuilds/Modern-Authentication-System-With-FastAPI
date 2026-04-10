import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_auth(client: AsyncClient):
    data = {
        "First Name": "David",
        "Last Name": "Hussain",
        "username": "wownow",
        "password": "Mango#27h",
        "email": "technogoydks@gmail.com"
    }
    response = await client.post("/auth/register", data=data)
    assert response.status_code == 201, response.json()
    assert "id" in response.json()