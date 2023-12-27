from psycopg_pool import ConnectionPool
from typing import List, Union
from pydantic import BaseModel
import os


pool = ConnectionPool(conninfo=os.environ["DATABASE_URL"])


class Error(BaseModel):
    message: str


class TransactionIn(BaseModel):
    date: str
    price: float
    description: str


class TransactionOut(BaseModel):
    id: int
    date: str
    price: float
    description: str


class TransactionRepository:
    def create(self, transaction: TransactionIn):
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        INSERT INTO transactions
                            (date, price, description)
                        VALUES
                            (%s, %s, %s)
                        RETURNING id;
                        """,
                        [
                            transaction.date,
                            transaction.price,
                            transaction.description
                        ]
                    )
                    id = result.fetchone()[0]
                    data = transaction.dict()
                    return TransactionOut(id=id, **data)
        except Exception as e:
            print('ERROR: ', e)
            return {"message": "Could not create transaction"}

    def get_all(self) -> Union[List[TransactionOut], Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        SELECT date
                             , price
                             , description
                        FROM transactions
                        ORDER BY date ASC;
                        """
                    )
                    result = []
                    for record in db:
                        transaction = TransactionOut(
                            id=record[0],
                            date=record[2],
                            price=record[3],
                            description=record[4]
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
                             , date
                             , price
                             , description
                        FROM transactions
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
                        SET date = %s
                          , price = %s
                          , description = %s
                        WHERE id = %s
                        """,
                        [
                            transaction.date,
                            transaction.price,
                            transaction.description,
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
