import os
import unittest
from unittest.mock import patch
import bot

class TestWeatherAlerts(unittest.TestCase):

    @patch('bot.requests.get')
    def test_high_temperature_alert(self, mock_get):
        # Mocking OWM response for high temperature
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "main": {"temp": 38.5},
            "weather": [{"main": "Clear", "description": "clear sky"}]
        }
        
        # Mocking email send
        with patch('bot.send_email') as mock_send_email:
            # Set a dummy API Key so it executes OWM branch
            with patch.dict(os.environ, {"WEATHER_API_KEY": "test_key", "SENDER_EMAIL": "test@gmail.com", "SENDER_PASSWORD": "pass", "RECEIVER_EMAIL": "recv@gmail.com"}):
                bot.run()
                mock_send_email.assert_called_once()
                subject = mock_send_email.call_args[0][0]
                self.assertIn("⚠️ PULSE WEATHER ALERT", subject)
                body = mock_send_email.call_args[0][1]
                self.assertIn("High Temperature Alert: Current temperature is 38.5°C", body)

    @patch('bot.requests.get')
    def test_rain_alert(self, mock_get):
        # Mocking OWM response for rain
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "main": {"temp": 24.0},
            "weather": [{"main": "Rain", "description": "moderate rain"}]
        }
        
        # Mocking email send
        with patch('bot.send_email') as mock_send_email:
            with patch.dict(os.environ, {"WEATHER_API_KEY": "test_key", "SENDER_EMAIL": "test@gmail.com", "SENDER_PASSWORD": "pass", "RECEIVER_EMAIL": "recv@gmail.com"}):
                bot.run()
                mock_send_email.assert_called_once()
                body = mock_send_email.call_args[0][1]
                self.assertIn("Rain Alert: Rain/drizzle/thunderstorm", body)

    @patch('bot.requests.get')
    def test_no_alert(self, mock_get):
        # Mocking OWM response for normal conditions
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "main": {"temp": 28.0},
            "weather": [{"main": "Clouds", "description": "few clouds"}]
        }
        
        # Mocking email send
        with patch('bot.send_email') as mock_send_email:
            with patch.dict(os.environ, {"WEATHER_API_KEY": "test_key", "SENDER_EMAIL": "test@gmail.com", "SENDER_PASSWORD": "pass", "RECEIVER_EMAIL": "recv@gmail.com"}):
                bot.run()
                mock_send_email.assert_not_called()

if __name__ == "__main__":
    unittest.main()
