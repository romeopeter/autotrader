import numpy as np
import pandas as pd

from datetime import time, datetime, timezone

from typing import List, Dict, Union

from pandas.core.groupby import DataFrameGroupBy
from pandas.core.window import RollingGroupby


class StockFrame:
    """
    Initializes the Stock Data Frame Object.

    StockFrame object stores all price data, adds indicator and handles the appending, organizing and deleting of data.
    """

    def __init__(self, data: List[dict]) -> None:
        """
        Initializes the StockFrame object.

        Parameter
        ---------
        data: List[dict]
            Data to convert to frame, normally this is from the historic price endpoint.

        Returns
        -------
        None -- Nothing is returned
        """

        self._data = data
        self._frame: pd.DataFrame = self.create_frame()
        self._symbol_groups = None
        self._symbol_rolling_groups = None

    @property
    def frame(self) -> pd.DataFrame:
        """
        The frame object

        Returns
        -------
        pd.DataFrame
           A Pandas data frame with the price data.
        """
        return self._frame

    @property
    def symbol_groups(self) -> DataFrameGroupBy:
        """
        Returns groups in the StockFrame.

        Overview
        --------
        The '_symbol_groups' property returns dataframe grouped by each symbol. This is used for performing operations on the symbol group.

        Returns
        -------
        DataFrameGroupBy
            A `pandas.core.groupby.GroupBy` object with each symbol.
        """

        self._symbol_groups: DataFrameGroupBy = self._frame.groupby(
            by="symbol", as_index=False, sort=True
        )

        return self._symbol_groups

    def symbol_rolling_groups(self, size: int) -> RollingGroupby:
        """
        Grab the windows for each symbol group

        Parameter
        ---------
        size: int
            Window size

        Parameter
        ---------
        size: int
            The size of the window

        Returns
        -------
        RollingGroupby: object -- A `pandas.core.window.RollingGroupby` object.
        """

        # If no symbol, then create symbol
        if not self._symbol_groups:
            self.symbol_groups()

        self._symbol_rolling_groups: RollingGroupby = self._symbol_groups.rolling(size)

        return self._symbol_rolling_groups

    def create_frame(self) -> pd.DataFrame:
        """
        Creates a new data frame with data passed through

        Return
        ------
        pd.DataFrame: object -- A pandas datafrane
        """

        # Make data frame
        price_df = pd.DataFrame(data=self._data)
        price_df = self._parse_datetime_column(price_df=price_df)
        price_df = self._set_multiple_index(price=price_df)

        return price_df

    def _parse_datetime_column(self, price_df: pd.DataFrame) -> pd.DataFrame:
        """
        Parses the datatime column in the dataframe

        Parameters
        ----------
        price_df: pd.DataFrame
            Price Dataframe with datatime column.

        Returns
        -------
        pd.DataFrame
            A pandad DataFrame object
        """

        price_df["datetime"] = pd.to_datetime(
            price_df["datetime"], unit="ms", origin="unix"
        )

        return price_df

    def _set_multiple_index(self, price_df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert dataframe to multi-index data frame

        Parameters
        --------
        price_df: pd.DataFrame
            Price data frame

        Returns
        -------
        pd.DataFrame
            A pandas dataframe
        """

        price_df = price_df.set_index(keys=["symbol", "datetime"])

        return price_df

    def add_rows(self, data: List[dict]) -> None:
        """
        Adds a new row to StockFrame

        Parameters
        ----------
        data: dict
            List of stock quote

        Return
        ------
        None
            Returns no data

        Usage
        -----
            >>> fake_data = {
                "datetime": 1586390396750,
                "symbol": "MSFT",
                "close": 165.7,
                "open": 165.67,
                "high": 166.67,
                "low": 163.5,
                "volume": 48318234
            }
            >>> # Add row to Stock Frame
            >>> stock_frame.add_rows(data=fake_data)
        """

        column_names = ["open", "close", "high", "low", "volume"]

        for quote in data:

            # Parse the time stamp
            time_stamp = pd.to_datetime(
                data[quote]["datetime"], unit="ms", origin="unix"
            )

            # Define the index Tuple
            row_id = (quote, time_stamp)

            # Define the StockFrame values
            new_values = [
                data[quote]["open"],
                data[quote]["close"],
                data[quote]["high"],
                data[quote]["low"],
                data[quote]["volume"],
            ]

            # Create the new row
            new_row = pd.Series(data=new_values)

            # Add the new row
            self.frame.loc[row_id, column_names] = new_row.values

            # Sort dataframe
            self.frame.sort_index(inplace=True)

    def do_indicators_exists(self, column_names: List[str]) -> bool:
        """
        Checks if indicators column exists before updating.

        Overview
        --------
        The user can append multiple indicator column to the StockFrame object. In some cases, columns need to be modified (modified via indicators) before making trades. This method helps to check those columns exists before modifying.

        Parameter
        ---------
        column_names: List[str]
            List of column names to be checked

        Raises
        ------
        KeyError: Raises KeyError if column is not found in the StockFrame.

        Return
        ------
        bool
            True if all columns exist, otherwise false

        """

        pass

    def _check_signals(self, indicators: dict) -> Union[pd.Series, None]:
        """
        Returns the last row of StockFrame if conditions are met.

        Overview
        --------
        Before a trade is executed, make sure condition warrant a 'buy' or 'sell' signal are met. This method will take the last row for each symbol in the StockFrame and compare the indicator column values with the conditions specifies by the user.

        Parameter
        --------
        indicators: dict
            A dictionary containing all the indicators checked, along with their buy and sell criteria.

        Return
        ------
        Union[pd.Series, None]
            Return pandas.Series object if signals are generated. If no signals are generated, return nothing.
        """

        pass
