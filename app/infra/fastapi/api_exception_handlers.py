from fastapi import Request
from starlette import status
from starlette.responses import JSONResponse

from app.core.interactors.auth import ForbiddenException, NotAuthorizedException
from app.core.interactors.transactions import NotEnoughBitcoinsException
from app.core.interactors.users import UserNotFoundException
from app.core.interactors.wallets import (
    WalletNotFoundException,
    UserReachedWalletLimitException,
)


def user_not_found_exception_handler(
    request: Request, exc: UserNotFoundException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message},
    )


def forbidden_access_exception_handler(
    request: Request, exc: ForbiddenException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"message": exc.message},
    )


def not_authorized_exception_handler(
    request: Request, exc: NotAuthorizedException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": exc.message},
    )


def wallet_not_found_exception_handler(
    request: Request, exc: WalletNotFoundException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message},
    )


def not_enough_bitcoins_exception_handler(
    request: Request, exc: NotEnoughBitcoinsException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": exc.message},
    )


def user_reached_wallet_limit_exception_handler(
    request: Request, exc: UserReachedWalletLimitException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": exc.message},
    )


def illegal_amount_exception_handler(
    request: Request, exc: ValueError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message" : exc.args},
    )
