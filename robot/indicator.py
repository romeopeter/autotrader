import numpy as np
import pandas as pd
import operator

from typing import Any, List, Dict, Union, Optional, Tuple

from autotrader.robot import StockFrame


class Indicator:
    """
    Trading indicator object for adding technical indicator to a StockFrame
    """

    def __init__(self, price_data_frame: StockFrame) -> None:
        """
        Initialize Indicator object

        Parameters:
        ----------
        price_data_frame: robot.StockFrame
            Price date frame used to add indicators. At a minimum this data frame must have the following columns: ['timestamp','close','open','high','low']

        Usage
        -----
        >>> historical_price_df = trading_robot.grab_historical_prices (
            start=start_date,
            end=end_date,
            bar_size=1,
            bar_type='minute'
        )
        >>>price_data_frame = pd.DataFrame(data=historical_price_df)
        >>>indicator_client = Indicator(price_data_frame=price_data_frame)
        >>> indicator_client.price_data_frame
        """

        self._stock_frame: StockFrame = price_data_frame
        self._price_groups = self._stock_frame.symbol_groups

        # Saves current input from user
        self._current_indicators = {}

        self._indicator_signals = {}
        self._frame = self._stock_frame.frame

    def get_indicator(self, indicator: Optional[str]) -> Dict:
        """
        Return the raw Pandas Dataframe Object.

        Parameters
        --------
        indicator: Optional[str]
            The indicator key, for example `ema` or `sma`.

        Returns:
            dict -- Either all of the indicators or the specified indicator.
        """

        if indicator and indicator in self._indicator_signals:
            return self._indicator_signals[indicator]
        else:
            return self._indicator_signals

    def set_indicators(
        self,
        indicator: str,
        buy: float,
        sell: float,
        condition_to_buy: Any,
        condition_to_sell: Any,
    ) -> None:
        """
        Sets trade indicator where signal crosses above and below a certain numerical threshold.

        Parameters
        ---------
        indicattor: str
            Indicator key, for example 'ema' or 'sma'.

        buy: float
            The buy signal threshold for the indicator

        sell: float
            The sell signal threshold for the indicator

        condition_to_buy: Any
            Operator used to evavluate for the 'buy' condition. For example '>' represent greater than or 'operator.gt' when using the 'operator' module.

        condition_to_sell: Any
            Operator used to evavluate for the 'sell' condition. For example '>' represent greater than or 'operator.gt' when using the 'operator' module.
        """

        # Add key if it doen't exist.
        if indicator not in self._indicator_signals:
            self._indicator_signals[indicator] = {}

        # Add signals
        self._indicator_signals[indicator]["buy"] = buy
        self._indicator_signals[indicator]["sell"] = sell
        self._indicator_signals[indicator]["buy_operator"] = condition_to_buy
        self._indicator_signals[indicator]["sell_operator"] = condition_to_sell

    @property
    def price_data_frame(self) -> pd.DataFrame:
        """
        Return the raw Pandas DataFrame object

        Returns
        ---------
        pd.DataFrame -- A multi-index data frame
        """

        return self._frame

    @price_data_frame.setter
    def price_data_frame(self, price_data_frame: pd.DataFrame) -> None:
        """
        Sets the price data frame

        Parameter
        --------
        price_data_frame: pd.Dataframe
            A multi-index data frame.
        """

        self._frame = price_data_frame


# NEXT: Adding indicators
# Video 6
