from pprint import pprint

import pandas as pd

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
            External API consumer ID
        redirect_url: str
            API fallback URL
        credential_path: str, optional
            Path to API client credential
        trading_account: str, optional
            Trading account number

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
        None
            Nothing is returned
        """
        self.client_id: str = client_id
        self.redirect_url: str = redirect_url
        self.credential_path: str = credential_path
        self.session: TDClient = self._create_session()
        self.trades: dict = {}
        self.historical_prices: dict = {}
        self.stock_frame = None

    def _create_session(self) -> TDClient:
        """
        Create session with stock API

        Returns
        -------
        object
            TDClient object with authenticated session
        """
        td_api_client = TDClient(
            client_id=self.client_id,
            redirect_url=self.redirect_url,
            credential_path=self.credential_path,
        )

        # Start session
        td_api_client.login()

        return td_api_client

    # NOTE: Search python @property
    @property
    def pre_market_open(self) -> bool:
        """
        Check for US market activities before actual market hours

        Returns
        -------
        bool:
            True if there's pre market, else false
        """
        pre_market_time = (
            datetime.now()
            .replace(hour=12, minute=00, second=00, tzinfo=timezone.utc)
            .timestamp()
        )
        market_start_time = (
            datetime.now()
            .replace(hour=13, minute=30, second=00, tzinfo=timezone.utc)
            .timestamp()
        )
        right_now = datetime.now().replace(tzinfo=timezone.utc).timestamp()

        if market_start_time >= right_now >= pre_market_time:
            return True
        return False

    @property
    def post_market_open(self) -> bool:
        """
        Check for US market activities after actual market hours

        Returns
        -------
        bool:
            True if there's post market, else false
        """
        post_market_end_time = (
            datetime.now()
            .replace(hour=22, minute=30, second=00, tzinfo=timezone.utc)
            .timestamp()
        )
        market_end_time = (
            datetime.now()
            .replace(hour=20, minute=30, second=00, tzinfo=timezone.utc)
            .timestamp()
        )
        right_now = datetime.now().replace(tzinfo=timezone.utc).timestamp()

        if post_market_end_time >= right_now >= market_end_time:
            return True
        return False

    @property
    def regular_market(self) -> bool:
        """
        Check for US stock market activities

        Returns
        -------
        bool
            True if there's market activities, else false
        """
        market_start_time = (
            datetime.now()
            .replace(hour=13, minute=30, second=00, tzinfo=timezone.utc)
            .timestamp()
        )
        market_end_time = (
            datetime.now()
            .replace(hour=20, minute=30, second=00, tzinfo=timezone.utc)
            .timestamp()
        )
        right_now = datetime.now().replace(tzinfo=timezone.utc).timestamp()

        if market_end_time >= right_now >= market_start_time:
            return True
        return False

    def portfolio(self):
        """
        Portfolio object store recognize and store positions

        Returns
        -------
        Portfolio: object
            portfolio object to store positions

        """
        pass

    def trade(self):
        """
        Builds order with with pre-build templates that can be easily modified to include complex strategies.

        Calls TD Ameritrade Quotes endpoint to get all
        the positions in the portfolio. returns single dicitionary for one position, else a nested dictionary.

        Returns
        -------
        Trade: object
            Trade object with specified template
        """
        pass

    def stock_frame():
        """
        Parameter
        ---------
        data: List[dict]
            Data to add to stock frame object

        Returns
        -------
        Stock-frane: object
            Multi-indexed data-frame for trading
        """
        pass

    def get_quotes() -> dict:
        """
        Get current quotes for all positions in portfolio

        Returns
        -------
        dict
            dictionary object containing all quotes and positions
        """
        pass

    def get_historical_prices() -> List[Dict]:
        """
        Historical prices for positions in portfolio

        Returns
        -------
        List[Dict]
            The historical price candles.
        """
        pass
