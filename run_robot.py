import time as true_time
import pprint
import pathlib
import operator
import pandas as pd
import settings

from datetime import datetime
from datetime import timedelta

from robot.robot import Robot
from robot.indicators import Indicator

# Grab config values
CLIENT_ID = settings.CLIENT_ID
REDIRECT_URI = settings.REDIRECT_URI
JSON_PATH = settings.JSON_PATH
ACCOUNT_NUMBER = settings.ACCOUNT_NUMBER

# Initialize robot
trading_robot = Robot(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    credentials_path=JSON_PATH,
    trading_account=ACCOUNT_NUMBER,
    paper_trading=True,
)

# Create a new portfolio
autotrader_portfolio = trading_robot.create_portfolio()

# Add muultiple positions
multi_positions = [
    {
        "asset_type": "equity",
        "quantity": 2,
        "purchase_price": 4.00,
        "symbol": "TSLA",
        "purchase_date": "2020-02-18",
    },
    {
        "asset_type": "equity",
        "quantity": 2,
        "purchase_price": 4.00,
        "symbol": "GME",
        "purchase_date": "2020-02-18",
    },
]

new_positions = autotrader_portfolio.add_positions(positions=multi_positions)
print(new_positions)
