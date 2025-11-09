import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InsufficientFundsError, InvalidBalanceError, WalletNotFoundError
from app.db.models import WalletsOrm

async def get_balance(uuid: uuid, session: AsyncSession):
    wallet = await session.get(WalletsOrm, uuid)
    if wallet is None:
        raise WalletNotFoundError(str(uuid))
    return wallet

async def create_wallet(balance: int, session: AsyncSession):
    if balance < 0:
        raise InvalidBalanceError(balance)
    new_wallet = WalletsOrm(balance=balance)
    session.add(new_wallet)
    await session.commit()
    await session.refresh(new_wallet)
    
    return new_wallet

async def change_balance(uuid: uuid, amount: int, session: AsyncSession):
    stmt = select(WalletsOrm).where(WalletsOrm.uuid == uuid).with_for_update()
    result = await session.execute(stmt)
    wallet = result.scalars().first()

    if wallet is None:
        raise WalletNotFoundError(str(uuid))

    new_balance = wallet.balance + amount
    if new_balance < 0:
        raise InsufficientFundsError(wallet.balance, amount)

    wallet.balance = new_balance
    session.add(wallet)
    await session.flush()
    await session.commit()
    return wallet