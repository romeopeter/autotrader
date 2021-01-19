from datetime import datetime

from typing import List, Dict, Union, Optional


class Trades:
    """
    Object represents stock trades. This is used to create new trade, add customisation trades, and modify excisting content.
    """

    def __init__(self):
        self.order = {}
        self.trade_id = ""

        self.side = ""
        self.side_opposite = ""
        self.enter_exit = ""
        self.enter_exit_opposite = ""

        self.order_response = ""
        self.trigger_added = False
        self.multi_leg = False

    def new_trade(
        self,
        trade_id: str,
        order_type: str,
        side: str,
        enter_exit: str,
        price: float,
        stop_limit_price: float,
    ) -> dict:
        """
        Create new trade object template.

        A trade object is a template that can be used to help build complex trades that normally are prone to errors when writing the JSON. Additionally, it will help the process of storing trades easier.

        Parameter
        --------
        trade_id: str
            ID associated with trade

        order_type: str
            The type of order to be created. one of the following: ['mkt', 'lmt', 'stop', 'stop_lmt', 'trailing_stop']

        side: str
            The for the trade. It can be one of the following: ['long', 'short']

        enter_exit: str
            Specifies whether trade will enter a new position, or exit an existing position. If ENTER then specify 'enter', if EXIT then specify 'exit'

        price: float
            Specifies the price for a trade

        stop_limit_price: float
            Specifies the limit price to stop a trade

        Returns
        -------
        {dict} -- [A dictionary representing new trade]
        """

        self.trade_id = trade_id

        self.order_types = {
            "mkt": "MARKET",
            "lmt": "LIMIT",
            "stop": "STOP",
            "stop_lmt": "STOP_LIMIT",
            "trailing_stop": "TRAILING_STOP",
        }

        self.order_instructions = {
            "enter": {"long": "BUY", "short": "SELL_SHORT"},
            "exit": {"long": "SELL", "short": "SELL_TO_COVER"},
        }

        self.order = {
            "orderStrategyType": "SINGLE",
            "orderType": self.order_types[order_type],
            "session": "NORMAL",
            "duration": "DAY",
            "orderLegCollection": [
                {
                    "instructions": self.order_instructions[enter_exit][side],
                    "quantity": 0,
                    "instrument": {"symbol": None, "assetType": None},
                }
            ],
        }

        if self.order["orderType"] == "STOP":
            self.order["stopPrice"] = price
        elif self.order["orderType"] == "LIMIT":
            self.order["price"] = price
        elif self.order["orderType"] == "STOP_LIMIT":
            self.order["price"] = stop_limit_price
            self.order["stopPrice"] = price
        elif self.order["orderType"] == "TRAILING_STOP":
            self.order["stopPriceLinkBasis"] = ""
            self.order["stopPriceLinkType"] = ""
            self.order["stopPriceOffset"] = 0.00
            self.order["stopType"] = "STANDARD"

        # Capture parameters passed in.
        # Useful when adding other components
        self.enter_exit = enter_exit
        self.side = side
        self.order_type = order_type
        self.price = price

        """Store parameter value for later use if conditions are met"""
        if order_type == "stop":
            self.stop_price = price
        elif order_type == "stop_lmt":
            self.stop_limit_price = stop_limit_price
        else:
            self.stop_price = 0.00
            self.stop_limit_price = 0.00

        # Set enter or exit
        if enter_exit == "enter":
            self.enter_exit = enter_exit
        elif enter_exit == "exit":
            self.enter_exit = enter_exit

        # Set sides
        if side == "long":
            self.side_opposite = "short"
        elif side == "short":
            self.side_opposite = "long"

        return self.order

    def instrument(
        self,
        symbol: str,
        quantity: int,
        asset_type: str,
        sub_asset_type: str = None,
        order_leg_id: int = 0,
    ) -> dict:
        """
        Adds instrument to a trade.

        Parameter
        ---------
        symbol: str
            The instrument ticker symbol.

        quantity: int
            The quantity of shares to be purchased.

        asset_type: str
            The instrument asset type. For example, `EQUITY`.

        Keyword Parammeter
        ------------------
        sub_asset_type: int
            The instrument sub-asset type. Not always needed

        Returns
        --------
        dict -- A dictionary with the instrument
        """

        leg = self.order["orderLegCollection"][order_leg_id]

        leg["instrument"]["symbol"] = symbol
        leg["instrument"]["assetType"] = asset_type
        leg["quantity"] = quantity

        self.order_size = quantity
        self.symbol = symbol
        self.asset_type = asset_type

        return leg

    def good_till_cancel(self, cancel_time: datetime) -> None:
        """
        Converts an order to a 'Good Till Cancel' order.

        Parameters
        ----------
        cancel_time: datetime.datetime
            A datetime object representing the cancel time of the order

        Returns
        ------
        None -- Returns nothing
        """

        self.order["duration"] = "GOOD_TILL_CANCEL"
        self.order["cancelTime"] = cancel_time.isoformat()

    def modify_sides(self, side: Optional[str], order_leg_id: int = 0) -> None:
        """
        Modify the sides of the order

        Parameters
        ----------
        side:
        The side to set. Can be any of the following: ['buy', 'sell', 'sell_short', 'buy_to_cover']

        Keyword parameters
        -----------------
        order_leg_int: int
            The leg to be adjusted. Default is 0

        Raise
        -----
        ValueError -- If 'side' is not valid then raise a ValueError
        """

        if side and side not in [
            "buy",
            "sell",
            "sell_short",
            "buy_to_cover",
            "sell_to_close",
            "buy_to_open",
        ]:
            raise ValueError("Specified side is not valid. Please chose a valid side")

        if side:
            self.order["orderLegCollection"]["instructions"] = side.upper()
        else:
            self.order["orderLegCollection"]["instructions"] = self.order_instructions[
                self.enter_exit
            ][self.side_opposite]
