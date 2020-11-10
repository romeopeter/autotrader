from pprint import pprint

import panda as pdb

from td.client import TDClient
from td.utils import TDUtilities

from datetime import datetime, timezone, time

from typing import List, Dict, Union


# Timestamp conversion to milliseconds
time_since_epoch = TDUtilities().milliseconds_since_epoch


class Robot:
    """
    Robot class handldes interaction with stock API and makes related requests
    """

    def __init__(
        self,
        client_id: str,
        redirect_url: str,
        credential_path: str = None,
        trading_account: str = None,
    ) -> None:
        """
        Paramenters
        -----------
        client-id: str
            External API client id
        redirect_url: str
            API fallbacl URL
        credential_path: str, optional
            Path to API client credential
        trading_account: str
            Represents trading account

        Attributes
        ----------
        session: object
            API connection session
        trades: dict
            Key-value pair of trade orders
        historical_prices: dict
            key-value pair of prices
        stock-frame: optional
            Price data, and trade signal indicators

        Returns
        -------
        None: Nothing is returned
        """
        self.client_id: str = client_id
        self.redirect_url: str = redirect_url
        self.credential_path: str = credential_path
        self.session: TDClient = self._create_session()
        self.trades: dict = {}
        self.historical_prices: dict = {}
        self.stock_frame = None

    def _create_session(self) -> TDClient:
        td_api_client = TDClient(
            client_id=self.client_id,
            redirect_url=self.redirect_url,
            credential_path=self.redential_path,
        )

        # Start session
        td_api_client.login()

        return td_api_client
