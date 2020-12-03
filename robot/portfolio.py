from typing import List, Dict, Union, Tuple, Optional


class Portfolio:
    """
    Portfolio object handles stock trading positions
    """

    def __init__(self, account_number: str = None):
        """
        Initialies new instance of the Portfolio object

        Parameters
        ---------
        account_number: str, None
            An account associated with portfolio. defaukt is set to nothing
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
            Price at which the position was purchased (default: 0.00)
        purchase_date: str, optional
            Date at which the positioned was purchased. Must be ISO format (YYYY-MM-DD):
                2020-11-14

        Return
        -------
        object: dict
            A dictionary object that represents a position in the portfolio.

        Usage
        -----
        >>> portfolio = Portfolio()
        >>> new_position = portfolio.add_position(symbol='TSLA',
                asset_type='stocks',
                quantity=2,
                purchase_price=4.00,
                purchase_date="2020-11-1"
            )

        >>> new_position
        {
            'asset_type': 'equity',
            'quantity': 2,
            'purchase_price': 4.00,
            'symbol': 'MSFT',
            'purchase_date': '2020-11-11'
        }
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

        Usage
        -----
        >>> # Multiple position
        >>> # multi_position = [
            {
            'asset_type': 'equity',
            'quantity': 2,
            'purchase_price': 4.00,
            'symbol': 'TSLA',
            'purchase_date': '2020-01-31'
            },
            {
                'asset_type': 'equity',
                'quantity': 2,0
                'purchase_price': 4.00,
                'symbol': 'AAPL',
                'purchase_date': '2020-01-31'
            }
        ]

        >>> new_positions = robot.portfolio.Portfolio.add_position(positions=multi_position)
        {
            'AAPL': {
            'asset_type': 'equity',
                'quantity': 2,0
                'purchase_price': 4.00,
                'symbol': 'AAPL',
                'purchase_date': '2020-01-31'
            },
            'TSLA': {
                'asset_type': 'equity',
                'quantity': 2,
                'purchase_price': 4.00,
                'symbol': 'TSLA',
                'purchase_date': '2020-01-31'
            }
        }
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

        Usage
        -----
        >>> portfolio = Portfolio()
        >>> new_position = portfolio.add_position(
                symbol='MSFT',
                asset_type='equity',
                quantity=2,
                purchase_price=4.00,
                purchase_date="2020-01-31"
            )

            >>> # Remove position
            >>> delete_status = portfolio.remove_position(symbol='MSFT')
            >>> delete_status
            (True, 'MSFT was successfully removed')
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
        """Checks whether a position is profitable

        Parameter
        ---------
        symbol: str
            Symobol of the financial instrument used check profitability

        current_price: float
            Current trading rice of financial instrument

        Return
        -----
        bool
            Returns True if profitable, else false if flat
        """

        if symbol in self.positions:
            # Grab purchase price
            purchase_price = self.positions[symbol].get("purchase_price", 0.0)

            if purchase_price <= current_price:
                return True

            return False

    def total_allocation(self):
        """Returns a summary of portfolio by asset allocation"""
        pass

    def risk_exposure(self):
        pass

    def total_market_value(self):
        pass
