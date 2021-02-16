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
    credential_path=JSON_PATH,
    trading_account=ACCOUNT_NUMBER,
    paper_trading=True,
)
