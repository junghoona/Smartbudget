import React, { useState } from "react";
import {
    Box,
    Button,
    Flex,
    FormControl,
    FormLabel,
    Heading,
    VStack,
    Input,
    InputGroup,
    InputLeftElement,
    Textarea
} from "@chakra-ui/react";
import { Formik } from "formik";

const TransactionForm = () => {
    const [date, setDate] = useState('');
    const [price, setPrice] = useState(0);
    const [description, setDescription] = useState('');

    const handleSubmit = async(event) => {
        event.preventDefault();
        const data = {
            date: date,
            price: price,
            description: description
        };

        const response = await fetch(
            `${process.env.REACT_APP_API_HOST}/transactions`,
            {
                credentials: "include",
                method: "POST",
                body: JSON.stringify(data),
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );

        if(response.ok) {
            const newTransaction = await response.json();
            setDate('');
            setPrice(0);
            setDescription('');
        } else {
            console.error(response);
        }
    };

    return (
        <Flex bg="red.100" align="center" justify="center" h="100vh">
            <Box bg="white" maxWidth="500px" w="100%" p={6} rounded="md">
            <Heading as="h1" size="lg" align="center" justify="center" h="10vh">Add new Transaction</Heading>
                <Formik
                    initialValues={{
                        date: "",
                        price: 0,
                        description: "",
                    }}
                >
                    <form onSubmit={(e)=> handleSubmit(e)}>
                        <VStack spacing={6} align="flex-start">
                            <FormControl>
                                <FormLabel htmlFor="date">Date: </FormLabel>
                                <Input
                                    placeholder="Select Date and Time"
                                    onChange={(e) => setDate(e.target.value)}
                                    value={date}
                                    size="md"
                                    type="datetime-local"
                                />
                            </FormControl>
                            <FormControl>
                                <FormLabel htmlFor="price">Price: </FormLabel>
                                <InputGroup>
                                    <InputLeftElement
                                        pointerEvents="none"
                                        color="gray.300"
                                        fontSize="1.2em"
                                        children="$"
                                    />
                                    <Input
                                        placeholder="Enter amount"
                                        onChange={(e) => setPrice(e.target.value)}
                                        value={price}
                                    />
                                </InputGroup>
                            </FormControl>
                            <FormControl>
                                <FormLabel htmlFor="description">Description: </FormLabel>
                                <Textarea
                                    placeholder="Enter Transaction Description Here"
                                    onChange={(e) => setDescription(e.target.value)}
                                    value={description}
                                    size="sm"
                                    resize="horizontal"
                                />
                            </FormControl>
                            <Button onClick={handleSubmit} type="submit" colorScheme="red" width="full">
                                Create Transaction
                            </Button>
                        </VStack>
                    </form>
                </Formik>
            </Box>
        </Flex>
    );
};

export default TransactionForm;
