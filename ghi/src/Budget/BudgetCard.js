import React from "react"

const BudgetCard = (props) => {
    return (
        <div className="col">
            <div key={props.list.id} className="card mb-3 shadow">
                <div className="card-body">
                    <h5 className="card-title">{props.list.category}</h5>
                    <p className="card-text">
                        {props.list.amount}
                    </p>
                </div>
                <div className="card-footer">
                </div>
            </div>
        </div> 
    );
}

export default BudgetCard;
