from queries.transactions import (
    Error,
    TransactionIn,
    TransactionOut,
    TransactionRepository
)
from fastapi import (
    APIRouter,
    Depends,
    Response
)
from typing import List, Union


router = APIRouter()


@router.post("/transactions", response_model=Union[TransactionOut, Error])
def create_transaction(
    transaction: TransactionIn,
    response: Response,
    repo: TransactionRepository = Depends(),    # Dependency injection
) -> Union[TransactionOut, Error]:
    transaction = repo.create(transaction)
    if transaction is None:
        response.status_code = 404
    return transaction


@router.get("/transactions", response_model=Union[List[TransactionOut], Error])
def get_transactions(
    repo: TransactionRepository = Depends()
) -> Union[List[TransactionOut], Error]:
    return repo.get_all()


@router.get("/transactions/{transaction_id}", response_model=Union[TransactionOut, Error])
def get_transaction(
    transaction_id: int,
    response: Response,
    repo: TransactionRepository = Depends()
) -> Union[TransactionOut, Error]:
    transaction = repo.get(transaction_id)
    if transaction is None:
        response.status_code = 404
    return transaction


@router.put("/transactions/{transaction_id}", response_model=Union[TransactionOut, Error])
def update_transaction(
    transaction_id: int,
    transaction: TransactionIn,
    repo: TransactionRepository = Depends()
) -> Union[TransactionOut, Error]:
    return repo.update(transaction_id, transaction)


@router.delete("/transactions/{transaction_id}", response_model=Union[bool, Error])
def delete_transaction(
    transaction_id: int,
    repo: TransactionRepository = Depends()
) -> Union[bool, Error]:
    return True
