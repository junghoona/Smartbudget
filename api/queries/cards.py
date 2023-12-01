from psycopg_pool import ConnectionPool
from typing import List, Union
from pydantic import BaseModel
import os


pool = ConnectionPool(conninfo=os.environ["DATABASE_URL"])


class Error(BaseModel):
    message: str


class CardIn(BaseModel):
    name: str
    credit_limit: float
    minimum_payment: float
    card_number: str
    balance: float
    budget_id: int


class CardOut(BaseModel):
    id: int
    name: str
    credit_limit: float
    minimum_payment: float
    card_number: str
    balance: float
    budget_id: int


class CardRepository:
    def create(self, card: CardIn) -> Union[CardOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        INSERT INTO cards (
                            name
                          , credit_limit
                          , minimum_payment
                          , card_number
                          , balance
                          , budget_id
                        )
                        VALUES
                            (%s, %s, %s, %s, %s)
                        RETURNING id;
                        """,
                        [
                            card.name,
                            card.credit_limit,
                            card.minimum_payment,
                            card.card_number,
                            card.balance,
                            card.budget_id
                        ]
                    )
                    id = result.fetchone()[0]
                    data = card.dict()
                    return CardOut(id=id, **data)
        except Exception as e:
            print('ERROR: ', e)
            return {"message": "Could not create card"}

    def get_all(self) -> Union[List[CardOut], Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        SELECT id
                             , name
                             , credit_limit
                             , minimum_payment
                             , card_number
                             , balance
                             , budget_id
                        FROM cards
                        ORDER BY name ASC;
                        """
                    )
                    result = []
                    for record in db:
                        card = CardOut(
                            id=record[0],
                            name=record[1],
                            credit_limit=record[2],
                            minimum_payment=record[3],
                            card_number=record[4],
                            balance=record[5],
                            budget_id=record[6]
                        )
                        result.append(card)
                    return result

        except Exception as e:
            print('ERROR: ', e)
            return {"message": "Could not get all cards"}

    def get_card(self, card_id: int) -> Union[CardOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        SELECT id
                             , name
                             , credit_limit
                             , minimum_payment
                             , card_number
                             , balance
                             , budget_id
                        FROM cards
                        WHERE id = %s
                        """,
                        [card_id]
                    )

        except Exception as e:
            print('ERROR: ', e)
            return {"message": "Could not get the card by ID"}

    def update(self, card_id: int, card: CardIn) -> Union[CardOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        UPDATE cards
                        SET name = %s
                          , credit_limit = %s
                          , minimum_payment = %s
                          , card_number = %s
                          , balance = %s
                          , budget_id = %s
                        WHERE id = %s
                        """,
                        [
                            card.name,
                            card.credit_limit,
                            card.minimum_payment,
                            card.card_number,
                            card.balance,
                            card.budget_id,
                            card_id
                        ]
                    )
                data = card.dict()
                return CardOut(
                    id=card_id, **data
                )
        except Exception as e:
            print('ERROR: ', e)
            return {"message": "Could not update card"}

    def delete(self, card_id: int) -> Union[bool, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        DELETE FROM cards
                        WHERE id = %s
                        """,
                        [card_id]
                    )

        except Exception as e:
            print('ERROR: ', e)
            return {"message": "Could not delete card by ID"}
