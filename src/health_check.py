import sys
import pandas as pd
import requests

print("python version",sys.version)
print("pandas version",pd.__version__)

response = requests.get(
    "https://www.nseindia.com",
    headers = {"User-Agent": "Mozilla/5.0"})

print("NSE status code:", response.status_code)