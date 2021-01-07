import operator
import numpy as np
import pandas as pd

from typing import Any, List, Dict, Union, Optional, Tuple

from autotrader.robot import StockFrame


class Indicator:
    """
    Trading technincal indicator object.
    """

    def __init__(self, price_data_frame: StockFrame) -> None:
        """
        Initialize Indicator object
        """
        self._stock_frame: StockFrame = price_data_frame
        self._price_groups = self._stock_frame.symbol_group

        # Saves current input from user
        self._current_indicators = {}

        self._indicator_signals = {}
        self._frame = self._stock_frame.frame

    def set_indicators(
        self,
        indicator: str,
        buy: float,
        sell: float,
        condition_to_buy: Any,
        condition_to_sell: Any,
    ) -> None:
        """
        Sets trade indicator for signal thresholds

        Parameters
        ---------
        indicattor: str
            Required indicator type

        buy: float
            ...

        sell: float
            ...

        condition_to_buy: Any
            ...

        condition_to_sell: Any
            ...
        """
        pass

        # Add signal as template
        if indicator not in self._indicator_signals:
            self._indicator_signals[indicator] = {}

        # Modify currrent signal template
        self._indicator_signals[indicator]["buy"] = buy
        self._indicator_signals[indicator]["sell"] = sell
        self._indicator_signals[indicator]["buy_operator"] = condition_to_buy
        self._indicator_signals[indicator]["sell_operator"] = condition_to_sell

    def get_indicator(self, indicator: Optional[str]) -> Dict:
        if indicator and indicator in self._indicator_signals:
            return self._indicator_signals[indicator]
        else:
            return self._indicator_signals

    @property
    def price_data_frame(self) -> pd.DataFrame:
        return self._frame

    @price_data_frame.setter
    def price_data_frame(self, price_data_frame: pd.DataFrame) -> None:
        self._frame = price_data_frame


# NEXT: Adding indicators
# Video 6
