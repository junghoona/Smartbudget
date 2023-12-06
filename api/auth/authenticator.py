import os
from fastapi import Depends
from .authentication import Authenticator
from queries.accounts import (
    AccountQueries,
    AccountOut,
    AccountIn,
)


class UserAuthenticator(Authenticator):
    async def get_account_data(
        self,
        username: str,
        accounts: AccountQueries,
    ):
        """
        Uses AccountQueries to get the account based on username (which could be email)
        """
        return accounts.get_account(username)

    def get_account_getter(
        self,
        accounts: AccountQueries = Depends(),
    ):
        """
        Returns the accounts
        """
        return accounts

    def get_hashed_password(self, account: AccountIn):
        """
        Returns the encrypted password value from the account object
        """
        return account.hashed_password

    def get_account_data_for_cookie(self, account: AccountIn):
        """
        Return the username and the data for the cookie.
        Return TWO Values from this method.
        """
        return account.username, AccountOut(**account.dict())


authenticator = Authenticator(os.environ["SIGNING_KEY"])
