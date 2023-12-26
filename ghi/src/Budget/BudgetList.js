import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import BudgetCard from "./BudgetCard";

const BudgetList = () => {
    const [budgets, setBudgets] = useState([[]]);

    const fetchData = async() => {
        const response = await fetch(
            `${process.env.REACT_APP_API_HOST}/budgets`
        );
        if (response.ok) {
            const data = await response.json();
            setBudgets(data);
        } else {
            console.error(response);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    return (
        <>
        <div className="px-4 py-5 mt-0 text-center bg-info">
            <h1 className="display-5 fw-bold">Your Budgets</h1>
            <div className="col-lg-6 mx-auto">
                <p className="lead mb-4">
                    The only resource you'll ever need to plan an run your in-person or
                    virtual conference for thousands of attendees and presenters.
                </p>
                <div className="d-grid gap-2 d-sm-flex justify-content-sm-center">
                    <Link to="/budgets/create" className="btn btn-primary btn-lg px-4 gap-3">New Budget</Link>
                </div>
            </div>
        </div>
        <div className="container">
            <h2>Budgets</h2>
            <div className="row">
                {budgets.map((budget, index) => {
                    return (
                        <BudgetCard key={index} list={budget} />
                    );
                })}
            </div>
        </div>
        </>
    );
};

export default BudgetList;
