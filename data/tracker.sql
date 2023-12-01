DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS cards;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS budgets;

CREATE TABLE users (
    id SERIAL NOT NULL UNIQUE,
    first TEXT NOT NULL,
    last TEXT NOT NULL,
    avatar TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    referrer_id INTEGER REFERENCES users("id") ON DELETE CASCADE
);

CREATE TABLE budgets (
    id SERIAL NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL,
    amount INTEGER NOT NULL
);

CREATE TABLE cards (
    id SERIAL NOT NULL UNIQUE,
    name TEXT NOT NULL UNIQUE,
    credit_limit INTEGER NOT NULL,
    minimum_payment INTEGER,
    card_number TEXT NOT NULL UNIQUE,
    balance INTEGER NOT NULL,
    budget_id INTEGER REFERENCES budgets("id") ON DELETE CASCADE
);

CREATE TABLE transactions (
    id SERIAL NOT NULL UNIQUE,
    description TEXT NOT NULL,
    date TIMESTAMP,
    price INTEGER NOT NULL,
    card_id INTEGER NOT NULL REFERENCES cards("id") ON DELETE CASCADE
);
