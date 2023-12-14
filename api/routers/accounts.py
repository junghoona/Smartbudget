from fastapi import (
    Depends,
    HTTPException,
    status,
    Response,
    APIRouter,
    Request,
)
from authenticator import authenticator
from psycopg.errors import UniqueViolation
from auth.authentication import Token
from pydantic import BaseModel
from queries.accounts import (
    AccountIn,
    AccountOut,
    AccountQueries
)


class AccountForm(BaseModel):
    username: str
    password: str


class AccountToken(Token):
    account: AccountOut


class HttpError(BaseModel):
    detail: str


router = APIRouter()


@router.get("/token", response_model=AccountToken | None)
async def get_token(
    request: Request,
    account: AccountOut = Depends(authenticator.try_get_current_account_data)
) -> AccountToken | None:
    if account and authenticator.cookie_name in request.cookies:
        return {
            "access_token": request.cookies[authenticator.cookie_name],
            "type": "Bearer",
            "account": account,
        }


@router.post("/api/accounts", response_model=AccountToken | HttpError)
async def create_account(
    account_info: AccountIn,
    request: Request,
    response: Response,
    accounts: AccountQueries = Depends(),
):
    hashed_password = authenticator.hash_password(account_info.password)
    try:
        account = accounts.create(account_info, hashed_password)
    except UniqueViolation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ERROR: Cannot create an account with duplicate credentials",
        )
    except Exception as e:
        print('ERROR: ', e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ERROR: Cannot create this account"
        )
    form = AccountForm(username=account_info.email, password=account_info.password)
    token = await authenticator.login(response, request, form, accounts)

    return AccountToken(account=account, **token.dict())
