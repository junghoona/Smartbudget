import { configureStore } from '@reduxjs/toolkit';
import budgetsReducer from "./Budget/BudgetsSlice";



export const store = configureStore({
    reducer: {
        budgets: budgetsReducer,
        transactions: transactionReducer,
    },
});
