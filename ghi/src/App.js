import * as React from "react";
import { ChakraProvider } from "@chakra-ui/react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import BudgetForm from "./Budget/BudgetForm.js";


const router = createBrowserRouter([
  { path: "budgets/new", Component: BudgetForm },
]);

function App() {
  return (
    <ChakraProvider>
      <RouterProvider router={router} />
    </ChakraProvider>
  );
}

export default App;
