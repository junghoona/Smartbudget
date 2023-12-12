import React, { useState } from "react";
import {
    Box,
    Button,
    Flex,
    FormControl,
    FormLabel,
    Heading,
    Input,
    InputGroup,
    InputLeftElement,
    VStack
} from "@chakra-ui/react";
import { Field, Formik } from "formik";


const CardForm = () => {
    const [name, setName] = useState('');
    const [credit, setCredit] = useState(0);
    const [payment, setPayment] = useState(0);
    const [cardNumber, setCardNumber] = useState('');
    const [balance, setBalance] = useState(0);

    const handleNameChange = (event) => {
        const value = event.target.value;
        setName(value);
    }

    const handleCreditChange = (event) => {
        const value = event.target.value;
        setCredit(value);
    }

    const handlePaymentChange = (event) => {
        const value = event.target.value;
        setPayment(value);
    }

    const handleCardNumberChange = (event) => {
        const value = event.target.value;
        setCardNumber(value);
    }

    const handleBalanceChange = (event) => {
        const value = event.target.value;
        setBalance(value);
    }

    const handleSubmit = async(event) => {
        event.preventDefault();

        const data = {
            name: name,
            credit_limit: credit,
            minimum_payment: payment,
            card_number: cardNumber,
            balance: balance
        };

        console.log('DATA: ', data);

        const response = await fetch(
            `${process.env.REACT_APP_API_HOST}/cards`,
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
            const newCard = response.json();

            setName('');
            setCredit(0);
            setPayment(0);
            setCardNumber('');
            setBalance(0);
        } else {
            console.error(response);
        }
    };

    return (
    <Flex bg="green.100" align="center" justify="center" h="100vh">
        <Box bg="white" maxWidth="500px" w="100%" p={6} rounded="md">
        <Heading as="h1" size="lg" align="center" justify="center" h="10vh">Add a new Card</Heading>
            <Formik
                initialValues={{
                    name: "",
                    credit_limit: 0,
                    minimum_payment: 0,
                    card_number: "",
                    balance: 0,
                }}
            >
                <form onSubmit={handleSubmit}>
                    <VStack spacing={6} align="flex-start">
                        <FormControl>
                            <FormLabel htmlFor="name">Name: </FormLabel>
                            <Field
                                as={Input}
                                id="name"
                                name="name"
                                type="text"
                                variant="filled"
                                onChange={handleNameChange}
                                placeholder="Enter card name"
                                value={name}
                            />
                        </FormControl>
                        <FormControl>
                            <FormLabel htmlFor="credit_limit">Credit Limit: </FormLabel>
                            <InputGroup>
                                <InputLeftElement
                                    pointerEvents="none"
                                    color="gray.300"
                                    fontSize="1.2em"
                                    children="$"
                                />
                                <Input 
                                    placeholder="Enter amount"
                                    onChange={handleCreditChange}
                                    value={credit}
                                />
                            </InputGroup>
                        </FormControl>
                        <FormControl>
                            <FormLabel htmlFor="minimum_payment">Minimum Payment Due: </FormLabel>
                            <InputGroup>
                                <InputLeftElement
                                    pointerEvents="none"
                                    color="gray.300"
                                    fontSize="1.2em"
                                    children="$"
                                />
                                <Input 
                                    placeholder="Enter amount"
                                    onChange={handlePaymentChange}
                                    value={payment} 
                                />
                            </InputGroup>
                        </FormControl>
                        <FormControl>
                            <FormLabel htmlFor="card_number">Card Number: </FormLabel>
                            <Field
                                as={Input}
                                id="card_number"
                                name="card_number"
                                type="text"
                                variant="filled"
                                onChange={handleCardNumberChange}
                                placeholder="0000 0000 0000 0000"
                                value={cardNumber}
                            />
                        </FormControl>
                        <FormControl>
                            <FormLabel htmlFor="balance">Balance: </FormLabel>
                            <InputGroup>
                                <InputLeftElement
                                    pointerEvents="none"
                                    color="gray.300"
                                    fontSize="1.2em"
                                    children="$"
                                />
                                <Input
                                    placeholder="Enter amount"
                                    onChange={handleBalanceChange}
                                    value={balance} 
                                />
                            </InputGroup>
                        </FormControl>
                        <Button type="submit" colorScheme="green" width="full">
                            Create Card
                        </Button>
                    </VStack>
                </form>
            </Formik>
        </Box>
    </Flex>
    );
};

export default CardForm;