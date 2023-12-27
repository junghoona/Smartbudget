import React, { useState } from "react";
import {
    Box,
    Button,
    Flex,
    FormControl,
    FormLabel,
    Heading,
    NumberInput,
    NumberInputField,
    NumberInputStepper,
    NumberIncrementStepper,
    NumberDecrementStepper,
    Slider,
    SliderFilledTrack,
    SliderTrack,
    SliderThumb,
    Select,
    VStack
} from "@chakra-ui/react";
import { Formik } from "formik";


const BudgetForm = () => {
    const [category, setCategory] = useState('');
    const [amount, setAmount] = useState(0.0);

    const handleSubmit = async(event) => {
        event.preventDefault();
        const data = {
            category: category,
            amount: amount
        };

        const response = await fetch (
            `${process.env.REACT_APP_API_HOST}/budgets`,
            {
                credentials: "include",
                method: "POST",
                body: JSON.stringify(data),
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );
        if (response.ok) {
            const newBudget = await response.json();

            setCategory('');
            setAmount(0);
        } else {
            console.error(response);
            return event.status(500).json({ error: "Create Budget Failed" });
        }
    };

    return (
        <Flex bg="purple.100" minWidth="max-content" align="center" justify="center" h="100vh">
            <Box bg="white" maxWidth="450px" w="100%" p={6} rounded="md">
            <Heading as="h1" size='lg' align="center" justify="center" h="10vh">Create a new Budget</Heading>
                <Formik>
                    <form onSubmit={(e) => handleSubmit(e)}>
                        <VStack spacing={6} align="flex-start">
                            <FormControl id="create-budget-form">
                                <FormLabel htmlFor="category">Category</FormLabel>
                                <Select onChange={(e) => setCategory(e.target.value)} placeholder="Select Category" size="md">
                                    <option>Shopping</option>
                                    <option>Personal Care</option>
                                    <option>Auto & Transport</option>
                                    <option>Bills & Utilities</option>
                                    <option>Dining & Drinks</option>
                                </Select>
                            </FormControl>
                            <FormControl>
                                <FormLabel htmlFor="amount">Amount</FormLabel>
                                <NumberInput onChange={(e) => setAmount(e)} value={amount}>
                                    <NumberInputField />
                                    <NumberInputStepper>
                                        <NumberIncrementStepper />
                                        <NumberDecrementStepper />
                                    </NumberInputStepper>
                                </NumberInput>
                            </FormControl>
                            <FormControl>
                                <Slider
                                    flex='1'
                                    focusThumbOnChange={false}
                                    value={amount}
                                >
                                    <SliderTrack>
                                        <SliderFilledTrack />
                                    </SliderTrack>
                                    <SliderThumb fontSize='sm' boxSize='32px' children={amount} />
                                </Slider>
                            </FormControl>
                            <Button type="submit" colorScheme="purple" width="full">
                                Create Budget
                            </Button>
                        </VStack>
                    </form>
                </Formik>
            </Box>
        </Flex>
    );
};

export default BudgetForm;
