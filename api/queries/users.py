from psycopg_pool import ConnectionPool
from pydantic import BaseModel
from typing import List
import os


pool = ConnectionPool(conninfo=os.environ["DATABASE_URL"])


class UserOut(BaseModel):
    id: int
    first: str
    last: str
    avatar: str
    email: str
    username: str


class UserIn(BaseModel):
    first: str
    last: str
    avatar: str
    email: str
    username: str


class UserQueries:
    def create_user(self, data: UserIn) -> UserOut:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    """,
                    []
                )
            return

    def get_user(self, user_id: int) -> UserOut:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    """,
                    [user_id]
                )
            return

    def get_all_users(self) -> List[UserOut]:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    """
                )
            return

    def update_user(self, user_id: int) -> UserOut:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    """,
                    [user_id]
                )
            return

    def delete_user(self, user_id: int) -> None:
        with pool.connection() as conn:
            with conn.curosr() as cur:
                cur.execute(
                    """
                    """,
                    [user_id]
                )
