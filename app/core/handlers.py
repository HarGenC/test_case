from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_CONTENT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from app.core.exceptions import InsufficientFundsError, InvalidBalanceError, WalletNotFoundError


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "path": request.url.path},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_CONTENT,
        content={"error": "Invalid input", "details": exc.errors()},
    )


async def wallet_not_found_handler(request: Request, exc: WalletNotFoundError):
    return JSONResponse(
        status_code=HTTP_404_NOT_FOUND,
        content={"error": "Wallet not found", "wallet_id": exc.wallet_id},
    )


async def insufficient_funds_handler(request: Request, exc: InsufficientFundsError):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={
            "error": "Insufficient funds",
            "balance": exc.balance,
            "requested": exc.amount,
        },
    )

async def invalid_balance_handler(request: Request, exc: InvalidBalanceError):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={
            "error": "Invalid balance",
            "balance": exc.balance,
        },
    )


async def generic_exception_handler(request: Request, exc: Exception):
    # отлавливаем всё, что не было обработано выше
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "details": str(exc),
            "path": request.url.path,
        },
    )