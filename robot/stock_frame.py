import numpy as np
import pandas as pd

from datetime import time, datetime, timezone

from typing import List, Dict, Union

from pandas.core.groupby import DataFrameGroupBy
from pandas.core.window import RollingGroupby


class StockFrame:
    """
   StockFrame object for manipulating and parsing stock data
    """

    def __init__(self, data: List[dict]) -> None:
        """
        Initializes the stock data frame object

        Parameter
        ---------
        List: List[dict]
            Data to convert to frame, normally this is from the historic price endpoint
        """

        self._data = data
        self._frame: pd.DataFrame = self.create_frame()
        self._symbol_groups = None
        self._symbol_rolling_groups = None

    @property
    def frame(self) -> pd.DataFrame:
        """
        Frame object

        Returns
        -------
        DataFame
            Pandas data frame with price data
        """
        return self._frame

    @property
    def symbol_group(self) -> DataFrameGroupBy:
        """
        Returns symbol groups in the StockFrame.

        Overview
        --------
        The '_symbol_groups' property returns dataframe grouped by each symbol. This is used for performing operations on the symbol group.

        Returns
        -------
        DataFrameGroupBy
            A `pandas.core.groupby.GroupBy` object with each symbol.
        """

        self._symbol_groups = self._frame.groupby(
            by="symbol", as_index=False, sort=True
        )

        return self._symbol_groups

    def symbol_rolling_groups(self, size: int) -> RollingGroupby:
        """
        Grab the windows for each group

        Parameter
        ---------
        size: int
            Window size

        Returns
        -------
        RollingGroupby
            A `pandas.core.window.RollingGroupby` object.
        """

        # If no symbol, then create symbol
        if not self._symbol_groups:
            self.symbol_group

        self._symbol_rolling_groups: RollingGroupby = self._symbol_groups.rolling(size)

        return self._symbol_rolling_groups

    def create_frame(self) -> pd.DataFrame:
        """
        Creates a new data frame with data passed through

        Return
        ------
        pd.DataFrame
            A pandas datafrane
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
            Price Dataframe containting the price column

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
            Price data frame object

        Returns
        -------
        pd.DataFrame
            A pandas dataframe
        """

        price_df = price_df.set_index(keys=["symbol", "datetime"])

        return price_df

    def add_rows(self, data: dict) -> None:
        """
        Adds a new row to StockFrame

        Parameters
        ----------
        data: Dict
            A stock quote

        Return
        ------
        None
            Returns no data
        """

        column_names = ["open", "close", "high", "low", "volume"]

        for symbol in data:

            # Parse the time stamp
            time_stamp = pd.to_datetime(
                data[symbol]["quoteTimeInLong"], unit="ms", origin="unix"
            )

            # Define the index Tuple
            row_id = (symbol, time_stamp)

            # Define the StockFrame values
            new_values = [
                data[symbol]["openPrice"],
                data[symbol]["closePrice"],
                data[symbol]["highPrice"],
                data[symbol]["lowPrice"],
                data[symbol]["askPrice"] + data[symbol]["bidPrice"],
            ]

            # Create the new row
            new_row = pd.Series(data=new_values)

            # Add the new row
            self.frame.loc[row_id, column_names] = new_row.values

            # Sort dataframe
            self.frame.sort_index(inplace=True)

    # Add method to check if indicators exists and to check signals
    # Know the difference btween indicators and signals
