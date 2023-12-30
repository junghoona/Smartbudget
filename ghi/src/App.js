import * as React from "react";
import { ChakraProvider } from "@chakra-ui/react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import TransactionForm from "./Transaction/TransactionForm.js";
import TransactionList from "./Transaction/TransactionList.js";
import BudgetForm from "./Budget/BudgetForm.js";
import BudgetList from "./Budget/BudgetList.js";
import CardForm from "./Card/CardForm.js";

import NavBar from "./Navbar.js";
import CardList from "./Card/CardList.js";


function App() {
  return (
    <ChakraProvider>
      <BrowserRouter>
        <NavBar />
        <Routes>
          <Route exact path="/"></Route>
          <Route></Route>
          <Route></Route>
          <Route path="budgets/">
            <Route path="create" element={<BudgetForm />} />
            <Route index element={<BudgetList />} />
          </Route>
          <Route path="cards/">
            <Route path="create" element={<CardForm />} />
            <Route index element={<CardList />} />
          </Route>
          <Route path="transactions/">
            <Route path="create" element={<TransactionForm />} />
            <Route index element={<TransactionList />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ChakraProvider>
  );
}

export default App;
