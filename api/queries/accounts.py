from psycopg_pool import ConnectionPool
from pydantic import BaseModel
from typing import Union
import os


pool = ConnectionPool(conninfo=os.environ["DATABASE_URL"])


class Error(BaseModel):
    message: str


class AccountIn(BaseModel):
    first_name: str
    last_name: str
    avatar: str
    email: str
    password: str


class AccountOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    avatar: str
    email: str


class AccountOutWithPassword(AccountOut):
    hashed_password: str


class AccountQueries:
    def get(self, email: str) -> Union[AccountOutWithPassword, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT id
                             , first_name
                             , last_name
                             , avatar
                             , email
                             , hashed_password
                        FROM accounts
                        WHERE email = %s;
                        """,
                        [email]
                    )
                    data = result.fetchone()
                    if data is None:
                        return {"message": "ERROR: Invalid email"}
                    return AccountOutWithPassword(
                        id=data[0],
                        first_name=data[1],
                        last_name=data[2],
                        avatar=data[3],
                        email=data[4],
                        hashed_password=data[5]
                    )
        except Exception as e:
            print('ERROR: ', e)
            return {"message": "Could not get the account. Email does not exist"}

    def create(
        self,
        account: AccountIn,
        hashed_password: str
    ) -> Union[AccountOutWithPassword, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        INSERT INTO accounts (
                            first_name, last_name, avatar, email, hashed_password
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id
                                , first_name
                                , last_name
                                , avatar
                                , email
                                , hashed_password;
                        """,
                        [
                            account.first_name,
                            account.last_name,
                            account.avatar,
                            account.email,
                            hashed_password
                        ]
                    )
                    record = result.fetchone()
                    return AccountOutWithPassword(
                        id=record[0],
                        first_name=record[1],
                        last_name=record[2],
                        avatar=record[3],
                        email=record[4],
                        hashed_password=record[5]
                    )
        except Exception as e:
            print('ERROR: ', e)
            return {"message": "This attempt to create an account was unsuccessful"}
