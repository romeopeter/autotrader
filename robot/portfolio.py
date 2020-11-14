from typing import List, Dict, Union, Tuple, Optional


class Portfolio:
    """
    Portfolio object handles stock trading positions
    """

    def __init__(self, account_number: str = None):
        """
        Parameters
        ---------
        account_number: str
            An account associated with portfolio
        """

        self.positions = {}
        self.positions_count = 0
        self.market_value = 0.0
        self.profit_loss = 0.0
        self.risk_tolerance = 0.0
        self.account_number = account_number

    def add_position(
        self,
        symbol: str,
        asset_type: str,
        quantity: int = 0,
        purchase_price: float = 0.00,
        purchase_date: str = None,
    ) -> dict:
        """
        Adds single position to Portfolio

        Parameters
        ---------
        symbol: str
            Financial instrument symbol, e.g: 'TSLA' or 'AAPL'
        asset_type: str
            The type of financial instrument, e.g: equity, stock, forex, futures, option

        Keyword parameters
        -------------------
        quantity: int
            Quantity of shares or contracts owned
        purchase_price: float
            Price of purchased position
        purchase_date: str, optional
            Date of purchased asset. Must be ISO format (YYYY-MM-DD):
                2020-11-14

        Return
        -------
        object: dict
            A dictionary object that represents a position in the portfolio.

        """
        self.positions[symbol] = {}
        self.positions[symbol]["symbol"] = symbol
        self.positions[symbol]["quantity"] = quantity
        self.positions[symbol]["purchase_price"] = purchase_price
        self.positions[symbol]["purchase_date"] = purchase_date
        self.positions[symbol]["asset_type"] = asset_type

        return self.positions

    def add_positions(self, positions: List(dict)) -> dict:
        """
        Add multiple positions to portfolio.
        This method take an interable of values and pass each position
        to the 'add_position' method

        Parameter
        --------
        positions: List[dict]
            List of dictionanary of multiple positions

        Returns
        -------
        dict
            Returns current position in portfolio
        """

        if isinstance(positions, list):
            for position in positions:
                self.add_position(
                    symbol=position["symbol"],
                    asset_type=position["asset_type"],
                    quantity=position.get("quantity", 0),
                    purchase_price=position.get("purchase_price", 0.00),
                    purchase_date=position.get("purchase_date", None),
                )
            return self.positions
        else:
            raise TypeError("positions must be a list of dictionaries")

    def remove_position(self, symbol: str) -> Tuple[bool, str]:
        """
        Removes single position from portfolio

        Paremeter
        --------
        symbol: str
            Symbol to identify position to be removed. e.g: 'TSLA' or 'AAPL'

        Return
        ------
        Tuple: bool, str
            Returns True with messsage if deleted, otherwise False
            with message
        """

        if symbol in self.positions:
            del self.positions[symbol]
            return (True, f"{symbol} was successfully removed")

        return (False, f"{symbol} does not exist in portfolio")

    def in_position(self, symbol: str) -> bool:
        """
        Checks if symbol is in portfolio

        Paremeter
        --------
        symbol: str
            Symbol to identify position. e.g: 'TSLA' or 'AAPL'

        Return
        ------
        bool
            True if position exist in the portfolio, False otherwise
        """

        if symbol in self.position:
            return True
        return False

    def is_profitable(self, symbol: str, current_price: float) -> bool:
        if symbol in self.positions:
            # Grab purchase price
            purchase_price = self.positions[symbol].get("purchase_price", 0.0)

            if purchase_price <= current_price:
                return True

            return False

    def total_allocation(self):
        """
        Return summary of portfolio by asset allocation
        """
        pass

    def risk_exposure(self):
        pass

    def total_market_value(self):
        pass
