import React, { useState, useEffect } from "react";
import { TransactionCard } from "./TransactionCard";
import { Link } from "react-router-dom";

const TransactionList = () => {
    const [transactions, setTransactions] = useState([]);

    const fetchData = async() => {
        const response = await fetch(
            `${process.env.REACT_APP_API_HOST}/transactions`
        );
        if (response.ok) {
            const data = await response.json();
            console.log('DATA: ', data);
            setTransactions(data);
        } else {
            console.error(response);
            return response.status(500).json({ error: "Transactions data fetch unsuccessful" });
        }
    }

    useEffect(() => {
        fetchData();
    }, []);

    return (
        <>
        <div className="px-4 py-5 mt-0 text-center bg-info">
            <h1 className="display-5 fw-bold"></h1>
            <div className="col-lg-6 mx-auto">
                <p className="lead mb-4">
                    The resource that you can count on to track your spending and monitor transaction details on your card.
                </p>
                <div className="d-grid gap-2 d-sm-flex justify-content-sm-center">
                    <Link to="/transactions/create" className="btn btn-primary btn-lg px-4 gap-3">New Transaction</Link>
                </div>
            </div>
        </div>
        <div className="container">
            <h2>Transactions</h2>
            <div className="row">
                {transactions.map((transaction, index) => {
                    return (
                        <TransactionCard key={index} list={transaction} />
                    );
                })}
            </div>
        </div>
        </>
    );
};

export default TransactionList;
