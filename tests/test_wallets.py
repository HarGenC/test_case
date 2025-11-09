import pytest
from httpx import AsyncClient
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_CONTENT,
)

BASE = "/api/v1/wallets"

@pytest.mark.parametrize("balance, expectation", [
    (0, [200, 0, None]),
    (-100, [HTTP_400_BAD_REQUEST, None, "Invalid balance"])
])
@pytest.mark.asyncio
async def test_create_wallet(balance: int, expectation: list, client: AsyncClient):
    response = await client.post(f"{BASE}/create", json={"balance":balance})
    assert response.status_code == expectation[0]
    data = response.json()
    
    if response.status_code == 200:
        assert data["balance"] == expectation[1]
        assert "uuid" in data
    else:
        assert data["error"] == expectation[2]

@pytest.mark.parametrize("flag_create_wallet, expectation", [
    (True, [200, 0, None]),
    (False, [HTTP_404_NOT_FOUND, None, "Wallet not found"])
])
@pytest.mark.asyncio
async def test_get_balance_wallet(flag_create_wallet: bool, expectation: list, client: AsyncClient):
    if flag_create_wallet:
        response = await client.post(f"{BASE}/create", json={})
        data = response.json()
        uuid = data["uuid"]
        response = await client.get(f"{BASE}/{uuid}")
        data = response.json()

        assert response.status_code == expectation[0]
        if response.status_code == 200:
            assert data["balance"] == expectation[1]
            assert "uuid" in data
    else:
        response = await client.get(f"{BASE}/262b9460-e1b1-45fe-bd89-e01d66133ceb")
        data = response.json()
        assert data["error"] == expectation[2]


@pytest.mark.parametrize("operation_type, start_balance, amount, expectation", [
    ("DEPOSIT", 0, 100, [200, 100, None]), 
    ("DEPOSIT", 0, -100, [HTTP_422_UNPROCESSABLE_CONTENT, None, "Invalid input"]),
    ("DEPoSIT", 0, 100, [HTTP_422_UNPROCESSABLE_CONTENT, None, "Invalid input"]),
    ("WITHDRAW", 100, 100, [200, 0, None]),
    ("WITHDRAW", 0, -100, [HTTP_422_UNPROCESSABLE_CONTENT, None, "Invalid input"]),
    ("WITHDRAW", 0, 100, [HTTP_400_BAD_REQUEST, None, "Insufficient funds"])
])
@pytest.mark.asyncio
async def test_change_balance_for_existing_wallet(operation_type: str, start_balance: int, amount: int, expectation: list, client: AsyncClient):
    create_response = await client.post(f"{BASE}/create", json={"balance":start_balance})
    data = create_response.json()
    uuid = data["uuid"]
    response = await client.post(f"{BASE}/{uuid}/operation", json={"operation_type":operation_type,"amount":amount})

    assert response.status_code == expectation[0]
    data = response.json()
    if response.status_code == 200:
        assert data["balance"] == expectation[1]
    else:
        assert data["error"] == expectation[2]

@pytest.mark.asyncio
async def test_change_balance_not_exist_wallet(client: AsyncClient):
    response = await client.post(f"{BASE}/262b9445-e1b1-45fe-bd89-e01d66133ceb/operation", json={"operation_type":"DEPOSIT","amount":100})
    data = response.json()

    assert response.status_code == HTTP_404_NOT_FOUND
    assert data["error"] == "Wallet not found"