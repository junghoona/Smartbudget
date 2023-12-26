export const TransactionCard = (props) => {
    return (
        <div className="col">
            <div key={props.list.id} >
                <div className="card-body">
                    <h5 className="card-title">{props.list.date}</h5>
                    <p className="card-text">
                        {props.list.description}
                    </p>
                </div>
                <div className="card-footer">
                    {props.list.price}
                </div>
            </div>
        </div>
    );
};
