import os
from routers import (
    accounts,
    budgets,
    cards,
    transactions
)
from fastapi import FastAPI
from authenticator import authenticator
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.include_router(accounts.router)
app.include_router(cards.router)
app.include_router(transactions.router)
app.include_router(budgets.router)
app.include_router(authenticator.router)

origins = [
    "http://localhost:3000",
    os.environ.get("CORS_HOST", None)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
