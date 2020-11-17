import numpy as np
import pandas as pd

from datetime import time, datetime, timezone

from typing import List, Dict, Union

from pandas.core.groupby import DataFrameGroupBy
from pandas.core.window import RollingGroupby


class StockFrame:
    """
    Stock frane handles all neccessary trading data requrie: price data, indicators
    """

    def __init__(self, data: List[dict]) -> None:
        """
        Initializes the stock data frame object

        Parameter
        ---------
        List: List[dict]
            Data to convert to frame, normally this from the historic price endpoint
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
        Symbol groups in the StockFrame. The '_symbol_groups' property returns dataframe groups by each symbol

        Returns
        -------
        DataFrameGroupBy
            A `pandas.core.groupby.GroupBy` object with each symbol.
        """
        pass
