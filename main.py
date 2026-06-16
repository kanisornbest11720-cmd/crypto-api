from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Crypto API by Best", "status": "running"}

@app.get("/price/{coin}")
def get_price(coin: str):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin,
        "vs_currencies": "usd,thb"
    }
    response = requests.get(url, params=params)
    data = response.json()

    if coin not in data:
        return {"error": f"ไม่พบ {coin}"}

    return {
        "coin": coin,
        "usd": data[coin]["usd"],
        "thb": data[coin]["thb"]
    }

@app.get("/portfolio")
def get_portfolio():
    coins = {
        "bitcoin": 0.01,
        "ethereum": 0.5,
        "solana": 10
    }
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(coins.keys()),
        "vs_currencies": "thb"
    }
    response = requests.get(url, params=params)
    prices = response.json()

    result = {}
    total = 0

    for coin, amount in coins.items():
        price = prices[coin]["thb"]
        value = amount * price
        total += value
        result[coin] = {
            "amount": amount,
            "price_thb": price,
            "value_thb": value
        }

    return {
        "portfolio": result,
        "total_thb": total
    }
