import React, { useState } from "react";
import { NavLink, Link } from "react-router-dom";
import './Navbar.css';  // Import CSS File for styling

const NavBar = () => {
    const [isMobile, setIsMobile] = useState(false);

    const handleMenuClick = () => { setIsMobile(!isMobile); };

    return(
        <nav className="navbar">
            <div className="logo">Your Logo</div>
            <ul className={isMobile ? 'nav-menu active' : 'nav-menu'}>
                <li className="nav-item">
                    <Link to="/">Home</Link>
                </li>
                <li className="nav-item dropdown">
                    <Link to="/cards">Cards</Link>
                    <div className="dropdown-content">
                        <Link to="/cards/create">Create a Card</Link>
                    </div>
                </li>
                <li className="nav-item dropdown">
                    <Link to="/budgets">Budgets</Link>
                    <div className="dropdown-content">
                        <Link to="/budgets/create">Create a Budget</Link>
                    </div>
                </li>
                <li className="nav-item dropdown">
                    <Link to="/transactions">Transactions</Link>
                    <div className="dropdown-content">
                        <Link to="/transactions/create">Create a Transaction</Link>
                    </div>
                </li>
            </ul>
            <div className="mobile-menu" onClick={handleMenuClick}>
                <span className={isMobile ? 'burger active' : 'burger'}></span>
            </div>
        </nav>
    )
};

export default NavBar;
