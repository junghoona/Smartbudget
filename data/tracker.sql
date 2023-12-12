DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS cards;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS budgets;

CREATE TABLE accounts (
    id SERIAL NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    avatar TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL
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
    balance INTEGER NOT NULL
);

CREATE TABLE transactions (
    id SERIAL NOT NULL UNIQUE,
    date TIMESTAMP,
    price INTEGER NOT NULL,
    description TEXT NOT NULL
);
