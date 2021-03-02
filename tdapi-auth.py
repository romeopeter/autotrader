import requests
import urllib
import time
from splinter import Browser
from decouple import config


# -------------------App Authentication automation-------------------
splinter_browser_executable_path = {
  "executable_path": R"C:\Users\Romeo\Downloads\geckodriver-v0.29.0-win64\geckodriver.exe"
}

# Component to build auth url
method = "GET"
url = "https://auth.tdameritrade.com/auth?"
client_id = config("CLIENT_ID", cast=str) + "@AMER.OAUTHAP"
payload = {
  "response_type": "code",
  "redirect_uri": config("REDIRECT_URI", cast=str),
  "client_id": client_id,
}

# Build url for Splinter
prepare_url = requests.Request(method=method, url=url, params=payload)
auth_url = prepare_url.prepare().url

# Instantiate splinter
with Browser(
  "firefox",
  **splinter_browser_executable_path,
  headless=False,
  incognito=True) as browser:

  # Define form item to fill out
  form_fields = {
    "username": config("USERNAME", cast=str),
    "password": config("PASSWORD", cast=str),
  }

  username = browser.find_by_id("username0").fill(form_fields["username"])
  password = browser.find_by_id("password1").fill(form_fields["password"])

 # Click accept button to login
  browser.find_by_id("accept").first.click()
