import os
import sys

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.api.v1.wallets import wallet_router
from app.core import handlers
from app.core.exceptions import (
    WalletNotFoundError, 
    InsufficientFundsError, 
    InvalidBalanceError
)

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


app = FastAPI(title="Wallet API")

app.include_router(wallet_router, prefix="/api/v1/wallets", tags=["wallets"])

app.add_exception_handler(RequestValidationError, handlers.validation_exception_handler)
app.add_exception_handler(HTTPException, handlers.http_exception_handler)
app.add_exception_handler(WalletNotFoundError, handlers.wallet_not_found_handler)
app.add_exception_handler(InsufficientFundsError, handlers.insufficient_funds_handler)
app.add_exception_handler(InvalidBalanceError, handlers.invalid_balance_handler)
app.add_exception_handler(Exception, handlers.generic_exception_handler)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)