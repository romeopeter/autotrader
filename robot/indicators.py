import numpy as np
import pandas as pd
import operator

from typing import Any
from typing import List
from typing import Dict
from typing import Union
from typing import Optional
from typing import Tuple

from autotrader.robot import StockFrame


class Indicator:
    """Trading indicator object for adding technical indicator to the StockFrame Object"""

    def __init__(self, price_data_frame: StockFrame) -> None:
        """
        Initialize Indicator object.

        Parameters:
        ----------
        price_data_frame: robot.StockFrame
            Price data frame used to add indicators. At a minimum this data frame must have the following columns: ['timestamp','close','open','high','low']

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
            Operator used to evavluate for the 'sell' condition. For example '<' represent less than or 'operator.lt' when using the 'operator' module.
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

        Return
        ------
        None -- returns nothing
        """

        self._frame = price_data_frame

    def change_in_price(self) -> pd.DataFrame:
        """
        Calculates the change in price

        Returns
        ------
        pd.DataFrame -- A pandas DataFrame with the change in price included
        """

        locals_data = locals()
        del locals_data["self"]

        column_name = "change_in_price"
        self._current_indicators[column_name] = {}
        self._current_indicators[column_name]["args"] = locals_data
        self._current_indicators[column_name]["func"] = self.change_in_price

        # Calculate change in price
        self._frame[column_name] = self._price_groups["closing"].transform(
            lambda x: x.diff()
        )

        return self._frame

    def relative_strength_index(
        self, period: int, method: str = "wilders"
    ) -> pd.DataFrame:
        """
        Calculate the relative strength index (RSI)

        Parameters
        ----------
        period: int
            Number of periods used to calculate RSI

        method: str
            The calculation methodolgy (default: 'wilders')

        Returns
        -------
        pd.DataFrame -- A Pandas dataframe with RSI indicator included

        Usage
        -----
        >>> historical_price_df = robot.grab_historical_price(
            start=start_date,
            end=end_date,
            bar_size=1,
            bar_type='minute'
        )
        >>> price_date_frame = pd.DataFrame(data=historical_price_df)
        >>> indicator_client = Indicator(price_data_frame=price_data_frame)
        >>> indicator_client.relative_strength_index(period=14)
        >>> price_data_frame = indicator_client.price_data_frame
        """

        locals_data = locals
        del locals_data["self"]

        column_name = "rsi"
        self._current_indicators[column_name] = {}
        self._current_indicators[column_name]["args"] = locals_data
        self._current_indicators[column_name]["func"] = self.relative_strength_index

        # Calculate the change in price
        if "change_in_price" not in self._frame:
            self.change_in_price()

        # Define the up days
        self._frame["up_day"] = self._price_groups["change_in_price"].tranform(
            lambda x: np.where(x >= 0, x, 0)
        )

        # Define the down days
        self._frame["down_day"] = self._price_groups["change_in_price"].tranform(
            lambda x: np.where(x < 0, x.abs(), 0)
        )

        # Calculate the EWMA for the Up days.
        self._frame["ewma_up"] = self._price_groups["up_day"].transform(
            lambda x: x.ewma(span=period).mean()
        )

        # Calculate the EWMA for the Down days.
        self._frame["ewma_down"] = self._price_groups["down_day"].transform(
            lambda x: x.ewma(span=period).mean()
        )

        # Calculate the relative stregnth
        relative_strength = self._frame["ewma_up"] / self._frame["ewma_down"]

        # Calculate the relative stregnth index
        relative_strength_index = 100.0 - ((100 / 1) + relative_strength)

        # Add RSI indicator to dataframe
        self._frame["rsi"] = np.where(
            relative_strength_index == 0, 100, relative_strength_index
        )

        # Clean up before returning data
        self._iframe.drop(
            label=["ewma_up", "ewma_down", "down_day", "up_day", "change_in_price"],
            axis=1,
            inplace=True,
        )

        return self._frame

    def simple_moving_average(self, period: int) -> pd.DataFrame:
        """
        Calculates the simple moving average (SMA)

        Parameter
        --------
        Period: int
            The number of period to use in calculating SMA

        Returns
        ------
        pd.DataFrame -- a Panda data frame with the SMA indicator included

        Usage
        ----
        >>> historical_price_df = robot.grab_histoical_prices(
                start=start_date,
                end=end_date,
                bar_size=1,
                bar_type='minute'
        )
        >>> price_data_frame = pb.DataFrame(data=historical_price_df)
        >>> indicator_client = Indicator(price_data_frame=price_data_frame)
        >>> indicator_client.simple_moving_average(period=100)
        >>> price_data_frame = indicator_client.price_data_frame
        """

        locals_data = locals()
        del locals_data["self"]

        column_name = "sma"
        self._current_indicators[column_name] = {}
        self._current_indicators[column_name]["args"] = locals_data
        self._current_indicators[column_name]["func"] = self.simple_moving_average()

        # Add the SMA
        self._frame[column_name] = self._price_groups.transform(
            lambda x: x.rolling(window=period).mean()
        )

        return self._frame

    def exponential_moving_average(
        self, period: int, alpha: float = 0.0
    ) -> pd.DataFrame:
        """
        Calculate the Exponential Moving Average (EMA).

        Parameters
        ----------
        period: int
            The number of period to use in calculating EMA

        alpha: float
            The alpha weight used in calculation. default is '0.0'

        Returns
        -------
        pd.DataFrame -- A Pandas data frame with ema indicator included

        Usage
        -----
        >>> historical_prices_df = trading_robot.grab_historical_prices(
                start=start_date,
                end=end_date,
                bar_size=1,
                bar_type='minute'
            )
        >>> price_data_frame = pd.DataFrame(data=historical_price_df)
        >>> indicator_client = Indicator(price_data_frame=price_data_frame)
        >>> indicator_client.exponential_moving_average(period=50, alpha=1/50)
        """

        locals_data = locals()
        del locals_data["self"]

        column_name = "ema"
        self._current_indicators[column_name] = {}
        self._current_indicators[column_name]["args"] = locals_data
        self._current_indicators[column_name][
            "func"
        ] = self.exponential_moving_average()

        # Add the EMA
        self._frame[column_name] = self._price_groups["closing"].transform(
            lambda x: x.ewa(span=period).mean()
        )

        return self._frame

    def refresh(self):
        """
        Update Indicator column after adding new roles
        """

        # Update the groups
        self.price_groups = self._stock_frame.symbol_groups

        # Loop and grab indicator details
        for indicator in self._current_indicators:
            # Grab stored indicator function
            indicator_arguments = self._current_indicators.indicator["args"]

            # Grab stored indicator arguments
            indicator_function = self._current_indicators.indicator["func"]

            # Run stored indicator function to update column
            indicator_function(**indicator_arguments)

    def check_singals(self) -> Union[pd.DataFrame, None]:
        signal_df = self._stock_frame._check_singals(
            indicators=self._indicator_signals,
            indciators_comp_key=self._indicators_comp_key,
            indicators_key=self._indicators_key,
        )

        return signal_df


# NEXT: Add another rsi method
# Video 6
