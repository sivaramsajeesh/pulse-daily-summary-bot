import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
    
    # Attempt to send email
    today = date.today().strftime("%Y-%m-%d")
    send_email(f"Pulse Daily Summary - {today}", summary)

if __name__ == "__main__":
    run()
