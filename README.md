# Pulse - Daily Summary Bot ☀️📝

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![GitHub Actions](https://img.shields.io/badge/actions-enabled-brightgreen.svg)](https://github.com/features/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Pulse** is a lightweight, automated Python bot that generates a fresh morning digest every day. It fetches current weather updates and retrieves a daily motivational quote, saving the final report as an artifact directly in your GitHub Actions runs.

---

## 🚀 How It Works

1. **Weather Fetching**: Connects to the `wttr.in` API to get the current weather conditions for Thiruvananthapuram (customizable).
2. **Motivational Quote**: Fetches a random daily quote and author from the `ZenQuotes` API.
3. **Daily Summary Generation**: Merges these details into a formatted text file named `daily_summary.txt`.
4. **GitHub Actions Automation**: Triggers automatically every morning at **08:00 IST (02:30 UTC)**, running on a serverless Ubuntu runner, and uploads the summary file as a downloadable workflow artifact.

---

## 📁 Project Structure

```bash
pulse/
│
├── bot.py             # Main Python script
├── requirements.txt   # Third-party dependencies
├── daily_summary.txt  # Generated daily report output
│
└── .github/
    └── workflows/
        └── daily.yml  # GitHub Actions automated workflow
```

---

## 🛠️ Local Setup & Run

To run the bot locally on your machine, follow these steps:

1. Clone or navigate to the directory:
   ```bash
   cd pulse
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the bot:
   ```bash
   python bot.py
   ```

4. View the output in the console and open the newly created `daily_summary.txt` file.

---

## 🤖 GitHub Actions Workflow

The bot is automated to run via GitHub Actions. The workflow configuration [daily.yml](.github/workflows/daily.yml) does the following:
- Triggers on a schedule (`02:30 UTC` / `08:00 IST` daily).
- Supports manual trigger (`workflow_dispatch`).
- Uploads the resulting `daily_summary.txt` as a workflow artifact named `daily_summary` which can be downloaded directly from your GitHub repository under the **Actions** tab.

---

## 📝 Example Output

```text
PULSE - Daily Summary

12 June 2026

WEATHER
Thiruvananthapuram: 🌦️  +28°C

TODAY'S QUOTE
The happiest people in the world are those who feel absolutely terrific about themselves. — Brian Tracy
```

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE details for more info.
