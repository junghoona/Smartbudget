from routers import (
    budgets,
    cards,
    transactions,
    users
)
from fastapi import FastAPI


app = FastAPI()
app.include_router(users.router)
app.include_router(cards.router)
app.include_router(transactions.router)
app.include_router(budgets.router)
