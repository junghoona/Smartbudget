from psycopg_pool import ConnectionPool
from typing import List, Optional, Union
from pydantic import BaseModel
from datetime import date
import os


pool = ConnectionPool(conninfo=os.environ["DATABASE_URL"])


class Error(BaseModel):
    message: str


class TransactionIn(BaseModel):
    description: str
    date: Optional[date]
    price: float
    card_id: int


class TransactionOut(BaseModel):
    id: int
    description: str
    date: Optional[date]
    price: float
    card_id: int


class TransactionRepository:
    def create(self, transaction: TransactionIn):
        with pool.connection() as conn:
            with conn.cursor() as db:
                result = db.execute(
                    """
                    INSERT INTO transactions
                        (description, date, price, card_id)
                    VALUES
                        (%s, %s, %s, %s)
                    RETURNING id;
                    """,
                    [
                        transaction.description,
                        transaction.date,
                        transaction.price,
                        transaction.card_id
                    ]
                )
                id = result.fetch_one()[0]
                data = transaction.dict()
                return TransactionOut(id=id, **data)

    def get_all(self) -> Union[List[TransactionOut], Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        SELECT description
                             , date
                             , price
                             , cards.name AS card_name
                        FROM transactions
                        LEFT JOIN cards
                        ON (transactions.card_id = cards.id)
                        ORDER BY cards.name ASC;
                        """
                    )
                    result = []
                    for record in db:
                        transaction = TransactionOut(
                            id=record[0],
                            description=record[1],
                            date=record[2],
                            price=record[3],
                            card_name=record[4]
                        )
                        result.append(transaction)
                    return result
        except Exception as e:
            print('ERROR: ', e)
            return {"message": "Could not get all transactions"}

    def get(self, transaction_id: int) -> Union[TransactionOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        SELECT id
                             , description
                             , date
                             , price
                             , cards.name AS card_name
                        FROM transactions
                        LEFT JOIN cards
                        ON (transactions.card_id == cards.id)
                        WHERE id = %s
                        """,
                        [transaction_id]
                    )
        except Exception as e:
            print('ERROR: ', e)
            return {"message": "Could not get transaction by ID"}

    def update(
        self,
        transaction_id: int,
        transaction: TransactionIn
    ) -> Union[TransactionOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        UPDATE transactions
                        SET description = %s
                          , date = %s
                          , price = %s
                          , card_id = %s
                        WHERE id = %s
                        """,
                        [
                            transaction.description,
                            transaction.date,
                            transaction.price,
                            transaction.card_id,
                            transaction_id
                        ]
                    )
        except Exception as e:
            print('ERROR: ', e)
            return {"message": "Could not update this transaction"}

    def delete(
        self,
        transaction_id: int
    ) -> Union[bool, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        DELETE FROM transactions
                        WHERE id = %s
                        """,
                        [transaction_id]
                    )
                return True
        except Exception as e:
            print('ERROR: ', e)
            return {"message": "Could not delete transaction by ID"}
