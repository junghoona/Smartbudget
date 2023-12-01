from typing import List, Union
from fastapi import (
    APIRouter,
    Depends,
    Response
)
from queries.cards import (
    Error,
    CardIn,
    CardOut,
    CardRepository
)


router = APIRouter()


@router.post("/cards", response_model=Union[CardOut, Error])
def create_card(
    card: CardIn,
    response: Response,
    repo: CardRepository = Depends()
):
    card = repo.create(card)
    if card is None:
        response.status_code = 404
    return card


# GET a list of cards
@router.get("/cards", response_model=Union[List[CardOut], Error])
def get_cards(
    repo: CardRepository = Depends()
):
    return repo.get_all()


# GET a card by ID
@router.get("/cards/{card_id}", response_model=Union[CardOut, Error])
def get_card(
    card_id: int,
    response: Response,
    repo: CardRepository = Depends()
):
    card = repo.get_card(card_id)
    if card is None:
        response.status_code = 404
    return card


# PUT
@router.put("/cards/{card_id}", response_model=Union[CardOut, Error])
def update_card(
    card_id: int,
    card: CardIn,
    repo: CardRepository = Depends()
):
    return repo.update(card_id, card)


# DELETE
@router.delete("/cards/{card_id}", response_model=Union[bool, Error])
def delete_card(
    card_id: int,
    repo: CardRepository = Depends()
) -> Union[bool, Error]:
    return repo.delete(card_id)
