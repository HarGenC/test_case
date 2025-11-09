from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.wallet import change_balance, get_balance, create_wallet
from app.schemas import OperationIn, WalletOut, OperationType, WalletCreate
from app.db.session import get_async_session

wallet_router = APIRouter()

@wallet_router.post("/{wallet_uuid}/operation", response_model=WalletOut)
async def wallet_operation(wallet_uuid: str, post_data: OperationIn, session: AsyncSession=Depends(get_async_session)):
    amount = post_data.amount if post_data.operation_type == OperationType.DEPOSIT else -post_data.amount
    return await change_balance(wallet_uuid, amount, session)

@wallet_router.get("/{wallet_uuid}", response_model=WalletOut)
async def get_wallet_balance(wallet_uuid: str, session: AsyncSession=Depends(get_async_session)):
    return await get_balance(wallet_uuid, session)

@wallet_router.post("/create", response_model=WalletOut)
async def create_wallet_point(post_data:WalletCreate, session: AsyncSession=Depends(get_async_session)):
    return await create_wallet(post_data.balance, session)