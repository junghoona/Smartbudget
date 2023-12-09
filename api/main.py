from routers import (
    accounts,
    budgets,
    cards,
    transactions
)
from fastapi import FastAPI
from authenticator import authenticator


app = FastAPI()


app.include_router(accounts.router)
app.include_router(cards.router)
app.include_router(transactions.router)
app.include_router(budgets.router)
app.include_router(authenticator.router)
