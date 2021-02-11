from pprint import pprint

import pandas as pd

from td.client import TDClient
from td.utils import TDUtilities

from datetime import datetime, timezone, time

from typing import List, Dict, Union

from robot import Trade
from robot import Portfolio
from robot import Stockframe


# Timestamp conversion to milliseconds
time_since_epoch = TDUtilities().milliseconds_since_epoch


class Robot:
    """
    Robot class handles interaction with stock API and makes related requests
    """

    def __init__(
        self,
        client_id: str,
        redirect_url: str,
        credential_path: str = None,
        trading_account: str = None,
    ) -> None:
        """
        Initialize instance of robot and logs into stock API platform

        Paramenters
        -----------
        client_id: str
            API consumer ID assigned to application

        redirect_url: str
            API fallback URL associated with TDAmeritrade

        credential_path: str, optional
            Path to API client credential

        trading_account: str, optional
            Trading account associated with TDAmeritrade account

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
        Start a new session

        Create a new session with TD Ameritrade API and log user into session

        Returns
        -------
            TDClient{object} -- A TDClient object with authenticated sessions
        """

        # Create a new instance instance of the client
        td_api_client = TDClient(
            client_id=self.client_id,
            redirect_url=self.redirect_url,
            credential_path=self.credential_path,
        )

        # Start session by loging in client
        td_api_client.login()

        return td_api_client

    @property
    def pre_market_open(self) -> bool:
        """
        Check for pre-market actitivies

        Uses the datetime module to create US pre-market Equity hours in UTC time.

        Usage:
            >>> autotrader = Robot(
            client_id=CLIENT_ID,
            redirect_uri=REDIRECT_URI,
            credentials_path=CREDENTIALS_PATH
            )

            >>> pre_market_open_flag = autotrader.pre_market_open
            >>> pre_market_open_flag()
            True


        Returns
        -------
        bool:
            True if there's pre-market, else false
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
        Check for post-market actitivities.

        Use the datetime module to create US post-market Equity hours in UTC time.

         Usage:
            >>> autotrader = Robot(
            client_id=CLIENT_ID,
            redirect_uri=REDIRECT_URI,
            credentials_path=CREDENTIALS_PATH
            )

            >>> post_market_open_flag = autotrader.pre_market_open
            >>> post_market_open_flag()
            True

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
    def regular_market_open(self) -> bool:
        """
        Check for US stock market activities.

        Uses the datetime module to create US Regular Market Equity hours in
        UTC time.

         Usage:
            >>> autotrader = Robot(
            client_id=CLIENT_ID,
            redirect_uri=REDIRECT_URI,
            credentials_path=CREDENTIALS_PATH
            )

            >>> regular_market_open_flag = autotrader.pre_market_open
            >>> regular_market_open_flag()
            True

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

    def create_portfolio(self) -> Portfolio:
        """
        Creates new portfolio

        Creates a Portfolio Object to help store and organize positions
        as they are added and removed during trading.

        Usage:
        ----
            >>> autotrader = Robot(
            client_id=CLIENT_ID,
            redirect_uri=REDIRECT_URI,
            credentials_path=CREDENTIALS_PATH
            )
            >>> portfolio = autotrader.create_portfolio()
            >>> portfolio
            autotrader.portfolio.Portfolio object at 0x0392BF88>

        Returns
        -------
        Portfolio: object
            portfolio object to store positions

        """
        pass

    def create_trade(self) -> Trade:
        """
        Initialize a new instance of a Trade Object

        Simplifies the process of building an order with with pre-built templates that can be easily modified to include complex strategies.


        Returns
        -------
        Trade: object
            Trade object with specified template
        """
        pass

    def create_stock_frame(self) -> Stockframe:
        """
        Generates a new Stockframe Object.

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
