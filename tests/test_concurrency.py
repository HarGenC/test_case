import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

BASE = "/api/v1/wallets"
TRANSPORT = ASGITransport(app=app)
BASE_URL = "http://test"

async def post_operation(wallet_id, operation):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        await client.post(f"{BASE}/{wallet_id}/operation", json=operation)

@pytest.mark.asyncio
async def test_concurrent_withdrawals():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        response = await client.post(f"{BASE}/create", json={})
        wallet_id = response.json()["uuid"]

        await client.post(
            f"{BASE}/{wallet_id}/operation",
            json={"operation_type": "DEPOSIT", "amount": 10000},
        )

    tasks = [
        asyncio.create_task(
            post_operation(wallet_id, {"operation_type": "WITHDRAW", "amount": 100})
        )
        for _ in range(1000)
    ]
    await asyncio.gather(*tasks)


    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        response = await client.get(f"{BASE}/{wallet_id}")
        
        assert response.status_code == 200
        assert response.json()["balance"] == 0