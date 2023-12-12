import * as React from "react";
import { ChakraProvider } from "@chakra-ui/react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import TransactionForm from "./Transaction/TransactionForm.js";
import BudgetForm from "./Budget/BudgetForm.js";
import CardForm from "./Card/CardForm.js";


const router = createBrowserRouter([
  { path: "budgets/create", Component: BudgetForm },
  { path: "cards/create", Component: CardForm },
  { path: "transactions/create", Component: TransactionForm }
]);

function App() {
  return (
    <ChakraProvider>
      <RouterProvider router={router} />
    </ChakraProvider>
  );
}

export default App;
