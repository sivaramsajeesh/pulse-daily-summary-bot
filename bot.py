import requests
from datetime import date

def get_weather(city="Thiruvananthapuram"):
    url = f"https://wttr.in/{city}?format=3"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip()
    
    except Exception:
        return "Weather unavailable"

def get_quote():
    url = "https://zenquotes.io/api/random"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        quote = data[0]["q"]
        author = data[0]["a"]

        return f"{quote} — {author}"

    except Exception:
        return "Quote unavailable"

def build_summary():
    today = date.today().strftime("%d %B %Y")

    weather = get_weather()
    quote = get_quote()

    summary = f"""PULSE - Daily Summary

{today}

WEATHER
{weather}

TODAY'S QUOTE
{quote}
"""
    return summary

def run():
    summary = build_summary()

    print(summary)

    with open("daily_summary.txt", "w") as f:
        f.write(summary)

    print("Pulse ran successfully.")

if __name__ == "__main__":
    run()
