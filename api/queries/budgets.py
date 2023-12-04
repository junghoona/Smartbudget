from psycopg_pool import ConnectionPool
from pydantic import BaseModel
from typing import List, Union
import os


pool = ConnectionPool(conninfo=os.environ["DATABASE_URL"])


class Error(BaseModel):
    message: str


class BudgetIn(BaseModel):
    category: str
    amount: float


class BudgetOut(BaseModel):
    id: int
    category: str
    amount: float


class BudgetRepository:
    def create(self, budget: BudgetIn) -> Union[BudgetOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        INSERT INTO budgets (
                            category, amount
                        )
                        VALUES
                            (%s, %s)
                        RETURNING id;
                        """,
                        [
                            budget.category,
                            budget.amount
                        ]
                    )
                    id = result.fetchone()[0]
                    data = budget.dict()
                    return BudgetOut(id=id, **data)
        except Exception as e:
            print('ERROR: ', e)
            return {"message": "Could not create budget"}

    def get_budget(self, budget_id: int) -> Union[BudgetOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT id
                             , category
                             , amount
                        FROM budgets
                        WHERE id = %s;
                        """,
                        [budget_id]
                    )
                    data = result.fetchone()
                    if data is None:
                        return None
                    return BudgetOut(
                        id=budget_id,
                        category=data[1],
                        amount=data[2]
                    )

        except Exception as e:
            print('ERROR: ', e)
            return {"message": "Invalid budget ID"}

    def get_all(self) -> Union[List[BudgetOut], Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        SELECT id
                             , category
                             , amount
                        FROM budgets
                        ORDER BY category ASC;
                        """
                    )
                    result = []
                    for record in db:
                        budget = BudgetOut(
                            id=record[0],
                            category=record[1],
                            amount=record[2]
                        )
                        result.append(budget)
                    return result
        except Exception as e:
            print('ERROR: ', e)
            return {"message": "Could not get all budgets"}

    def update(
        self,
        budget_id: int,
        budget: BudgetIn
    ) -> Union[BudgetOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        UPDATE budgets
                        SET category = %s
                          , amount = %s
                        WHERE id = %s
                        """,
                        [
                            budget.category,
                            budget.amount,
                            budget_id
                        ]
                    )
                    data = budget.dict()
                    return BudgetOut(
                        id=budget_id, **data
                    )
        except Exception as e:
            print('ERROR: ', e)
            return {"message": "Could not update budget"}

    def delete(
        self,
        budget_id: int
    ) -> Union[bool, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        DELETE FROM budgets
                        WHERE id = %s
                        """,
                        [budget_id]
                    )
                    return True
        except Exception as e:
            print('ERROR: ', e)
            return {"message": "Could not delete budget"}
