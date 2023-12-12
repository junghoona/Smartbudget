import * as React from "react";
import { ChakraProvider } from "@chakra-ui/react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import BudgetForm from "./Budget/BudgetForm.js";
import CardForm from "./Card/CardForm.js";


const router = createBrowserRouter([
  { path: "budgets/new", Component: BudgetForm },
  { path: "cards/new", Component: CardForm },
]);

function App() {
  return (
    <ChakraProvider>
      <RouterProvider router={router} />
    </ChakraProvider>
  );
}

export default App;
