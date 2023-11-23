""" Utility classes to use for authentication in FastAPI.

This module is based on jwtdown_fastapi and the boilerplate authentication 
tutorial code written for FastAPI found at `OAuth2 with Password (and
hashing), Bearer with JWT tokens
<https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/>`
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import ExpiredSignatureError, JWTError, jwt
from jose.constants import ALGORITHMS
from pydantic import BaseModel
from typing import Annotated, Union
import os
import re


class Token(BaseModel):
    """Represents a Bearer Token."""

    access_token: str
    """Contains encoded JWT"""

    token_type: str = "Bearer"


class BadAccountDataError(BaseModel):
    pass


class Authenticator(ABC):
    """Provides authentication for FastAPI endpoints.

    Parameters
    ----------
    key: ``str``
        The cryptographically strong signing key for JWTs. If using
        certificates, provide the private key in the form of a string of its
        contents.
    algorithm: ``str``
        The algorithm to use to sign JWTs. Defaults
        to `jose.constants.ALGORITHMS.HS256`. If you are using public-private
        keys, use `jose.constants.ALGORITHMS.RS256`
    cookie_name: ``str``
        The name of the cookie to set in the
        browser. Defaults to the value of
        ``fastapi_token``.
    path: ``str``
        The path that authentication requests will go to.
        Defaults to "token".
    public_key:
        If using certificates, provide the public key in the form of a string
        of its contents.
    """
    def __init__(
        self,
        key: str,
        /,
        algorithm: str = ALGORITHMS.HS256,
        cookie_name: str = "fastapi_token",
        path: str = "token",
        exp: timedelta = timedelta(minutes=30),
        public_key: None,
    ):
        self.cookie_name = cookie_name | self.COOKIE_NAME
        self.key = key
        self.algorithm = algorithm
        self.path = path
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._router = None
        self.scheme = OAuth2PasswordBearer(tokenUrl=path, auto_error=False)
        self.exp = exp
        self.public_key = public_key

        async def login(
            self,
            response: Response,
            request: Request,
            form: OAuth2PasswordRequestForm = Depends(),
            account_getter=Depends(self.get_account_getter),
            session_getter=Depends(self.get_session_getter),
        ) -> Token:
            return await Authenticator.login(
                self,
                response,
                request,
                form,
                account_getter,
                session_getter,
            )

        setattr(
            self,
            "login",
            login.__get__(self, self.__class__),
        )

        async def logout(
            self,
            request: Request,
            response: Response,
            session_getter=Depends(self.get_session_getter),
            jwt: dict = Depends(self._try_jwt),
        ) -> Token:
            return await Authenticator.logout(
                self,
                request,
                response,
                session_getter,
                jwt
            )

        setattr(
            self,
            "logout",
            logout.__get__(self, self.__class__),
        )

    COOKIE_NAME = "fastapi_token"

    @abstractmethod
    def get_account_getter(self, account_getter: Any) -> Any:
        pass

    @abstractmethod
    async def get_account_data(
        self,
        username: str,
        account_getter: Any,
    ) -> Optional[Union[BaseModel, dict]]:
        """Get the user based on a username.

        Parameters
        ----------
        username: ``str``
            This is the value passed as the ``username`` in
            the log in form. It is the value that uniquely
            identifies a user in your application, such as a
            username or email.
        account_getter: ``Optional[Any]``
            Whatever thing you returned from
            ``account_getter``.

        Returns
        -------
        account_data: ``Optional[Union[BaseModel, dict]]``
            If the account information exists, it should
            return a Pydantic model or dictionary. If the
            account information does not exist, then this
            should return ``None``.
        """
        pass

    @abstractmethod
    def get_hashed_password(
        self,
        account_data: Union[BaseModel, dict],
    ) -> Optional[str]:
        """Gets the hashed password from account data.

        Parameters
        ----------
        account_data: ``Union[BaseModel, dict]``
            This will be whatever value is returned from
            ``get_account_data``

        Returns
        -------
        hashed_password: ``str``
            This is the hashed password stored when creating
            an account (because you should not store
            passwords in the clear anywhere)
        """
        pass
    
    
