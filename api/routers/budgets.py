from typing import List, Union
from fastapi import (
    APIRouter,
    Depends,
    Response
)
from queries.budgets import (
    BudgetIn,
    BudgetRepository,
    BudgetOut,
    Error
)


router = APIRouter()


# POST: Create a Budget
# Add response model to change the output data type
@router.post("/budgets", response_model=Union[BudgetOut, Error])
def create_budget(
    budget: BudgetIn,
    response: Response,
    repo: BudgetRepository = Depends()
):
    return repo.create(budget)


# GET: Get all budgets
@router.get("/budgets", response_model=Union[List[BudgetOut], Error])
def get_all(
    repo: BudgetRepository = Depends()
):
    return repo.get_all()


# GET: Get a budget by id
@router.get("/budgets/{budget_id}", response_model=Union[BudgetOut, Error])
def get_budget(
    budget_id: int,
    response: Response,
    repo: BudgetRepository = Depends()
) -> Union[BudgetOut, Error]:
    budget = repo.get_budget(budget_id)
    if budget is None:
        response.status_code = 404
    return budget


# PUT: Update a budget
@router.put("/budgets/{budget_id}", response_model=Union[BudgetOut, Error])
def update_budget(
    budget_id: int,
    budget: BudgetIn,
    repo: BudgetRepository = Depends()
) -> Union[BudgetOut, Error]:
    return repo.update(budget_id, budget)


@router.delete("/budgets/{budget_id}", response_model=Union[bool, Error])
def delete_budget(
    budget_id: int,
    repo: BudgetRepository = Depends()
) -> Union[bool, Error]:
    return repo.delete(budget_id)
