import { createSlice } from "@reduxjs/toolkit";

// Define what the initial data should look like
const initialState = {
    transactions: [],
};

// Create the "slice of data that is the transactions data"
export const transactionSlice = createSlice({
    name: "transactions",
    // Set the initial state
    initialState,
    reducers: {
        // Define logic about how to add new transaction
        // to the list of transactions in the state
        addTransaction: (state, action) => {
            // Action's payload is the data we want to add
            const newTransaction = action.payload;
            // Use the push method to add new transaction
            state.transactions.push(newTransaction);
        },
    },
});

// Export actions for use in components
export const { addTransaction } = transactionSlice.actions;

// Export the reducer to use in the declaration of store in store.js
export default transactionSlice.reducer;
