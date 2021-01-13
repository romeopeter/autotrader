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
        self.mult_leg = False

    def new_trade(
        self,
        trade_id: str,
        order_type: str,
        side: str,
        enter_exit: str,
        price: float,
        stop_limit_price: float,
    ) -> Dict:
        """
        Create new trade object template

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

        Price: float
            Specifies the price for a trade

        stop_limit_price: float
            Specifies the limit price to stop a trade
        """
