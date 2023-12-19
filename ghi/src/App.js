import * as React from "react";
import { ChakraProvider } from "@chakra-ui/react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import TransactionForm from "./Transaction/TransactionForm.js";
import BudgetForm from "./Budget/BudgetForm.js";
import BudgetList from "./Budget/BudgetList.js";
import CardForm from "./Card/CardForm.js";
import Navbar from "./Navbar.js";


function App() {
  return (
    <ChakraProvider>
      <BrowserRouter>
        <Navbar />
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
          </Route>
          <Route path="transactions/">
            <Route path="create" element={<TransactionForm />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ChakraProvider>
  );
}

export default App;
