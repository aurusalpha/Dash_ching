# utils/dhan_api.py → now using Angel One SmartAPI
import requests
import os

ANGEL_API_KEY = os.getenv("ANGEL_API_KEY")
ANGEL_CLIENT_CODE = os.getenv("ANGEL_CLIENT_CODE")
ANGEL_ACCESS_TOKEN = os.getenv("ANGEL_ACCESS_TOKEN")
BASE_URL = "https://apiconnect.angelbroking.com/rest/secure/angelbroking"

HEADERS = {
    "X-UserType": "USER",
    "X-SourceID": "WEB",
    "X-ClientLocalIP": "127.0.0.1",
    "X-ClientPublicIP": "127.0.0.1",
    "X-MACAddress": "00:00:00:00:00:00",
    "X-PrivateKey": ANGEL_API_KEY,
    "X-ClientCode": ANGEL_CLIENT_CODE,
    "Authorization": f"Bearer {ANGEL_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Full NIFTY 50 token mapping from Angel SmartAPI instrument file
SYMBOL_MAP = {
    "RELIANCE": "2885",
    "INFY": "1594",
    "HDFCBANK": "1333",
    "ICICIBANK": "4963",
    "TCS": "11536",
    "KOTAKBANK": "1922",
    "SBIN": "3045",
    "LT": "11483",
    "ITC": "1660",
    "BHARTIARTL": "122",
    "ASIANPAINT": "604",
    "MARUTI": "1593",
    "SUNPHARMA": "3351",
    "AXISBANK": "212",
    "ULTRACEMCO": "2475",
    "BAJFINANCE": "317",
    "NTPC": "2973",
    "HINDUNILVR": "1394",
    "POWERGRID": "14977",
    "INDUSINDBK": "5258",
    "TITAN": "3506",
    "BAJAJFINSV": "367",
    "GRASIM": "10738",
    "TATASTEEL": "3499",
    "ONGC": "2476",
    "JSWSTEEL": "11723",
    "TECHM": "13538",
    "CIPLA": "1975",
    "NESTLEIND": "17963",
    "ADANIENT": "25",
    "ADANIPORTS": "15083",
    "DIVISLAB": "10940",
    "DRREDDY": "881",
    "BRITANNIA": "547",
    "HEROMOTOCO": "1348",
    "HCLTECH": "7229",
    "HDFCLIFE": "11915",
    "BPCL": "526",
    "COALINDIA": "20374",
    "EICHERMOT": "910",
    "HINDALCO": "1344",
    "BAJAJ-AUTO": "371",
    "SBILIFE": "13467",
    "SHREECEM": "11067",
    "APOLLOHOSP": "157",
    "TATAMOTORS": "3456",
    "UPL": "11287",
    "WIPRO": "378",
    "NIFTY50": "99926000"
}

def get_ltp(symbol):
    token = SYMBOL_MAP.get(symbol)
    if not token:
        return None

    payload = {
        "mode": "LTP",
        "exchangeTokens": {
            "NSE": [token]
        }
    }
    try:
        response = requests.post(
            f"{BASE_URL}/marketData/v1/quote/ltp",
            headers=HEADERS,
            json=payload
        )
        if response.status_code == 200:
            data = response.json()
            return data['data']['fetched']['NSE'][token]['ltp']
        else:
            print(f"Error from SmartAPI: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Exception in get_ltp: {e}")
        return None

def fetch_ticker_data(symbols):
    data = {}
    for sym in symbols:
        ltp = get_ltp(sym)
        data[sym] = ltp if ltp else "—"
    return data
