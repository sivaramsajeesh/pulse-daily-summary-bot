import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import date

def get_weather(city="Thiruvananthapuram"):
    api_key = os.environ.get("WEATHER_API_KEY")
    if not api_key:
        print("WEATHER_API_KEY environment variable is missing!")
        return "Weather unavailable (API Key missing)", None, False

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        main_weather = [w["main"].lower() for w in data["weather"]]
        
        # Check if rain/drizzle/thunderstorm is in the weather conditions
        is_rain = any(any(r in cond for r in ["rain", "drizzle", "thunderstorm"]) for cond in main_weather)
        
        weather_text = f"{city}: {temp}°C, {description.capitalize()}"
        return weather_text, temp, is_rain
    except Exception as e:
        print(f"Error fetching weather from OpenWeatherMap: {e}")
        return "Weather unavailable", None, False

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

def send_email(subject, body):
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    receiver_email = os.environ.get("RECEIVER_EMAIL")

    if not sender_email or not sender_password or not receiver_email:
        print("Email credentials not configured. Skipping email notification.")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Connect to Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def run():
    # Fetch weather and check alert criteria
    weather_text, temp, is_rain = get_weather()
    quote = get_quote()
    today = date.today().strftime("%d %B %Y")

    summary = f"""PULSE - Daily Summary

{today}

WEATHER
{weather_text}

TODAY'S QUOTE
{quote}
"""

    print(summary)

    with open("daily_summary.txt", "w") as f:
        f.write(summary)

    print("Pulse ran successfully.")
    
    # Check alert conditions
    alerts = []
    if temp is not None:
        if temp > 35:
            alerts.append(f"High Temperature Alert: Current temperature is {temp}°C (exceeds 35°C).")
        if is_rain:
            alerts.append("Rain Alert: Rain/drizzle/thunderstorm is currently observed or predicted.")

    if alerts:
        alert_msg = "\n".join(alerts)
        subject = f"⚠️ PULSE WEATHER ALERT - {today}"
        body = f"""Attention! A weather alert has been triggered:

{alert_msg}

Full Daily Summary:
------------------
{summary}
"""
        print("Alert condition met! Sending email...")
        send_email(subject, body)
    else:
        print("No weather alerts triggered (Temperature <= 35°C and no rain). Skipping email alert.")

if __name__ == "__main__":
    run()
