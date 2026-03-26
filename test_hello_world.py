import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import json

import hello_world


FAKE_WEATHER_JSON = json.dumps({
    "current_condition": [{
        "temp_F": "61",
        "weatherDesc": [{"value": "Sunny"}]
    }]
}).encode("utf-8")

FAKE_ART = "   \\  /\n _ /\"\".-.  Sunny\n".encode("utf-8")


class TestGetWeather(unittest.TestCase):

    def _mock_response(self, data):
        mock_resp = MagicMock()
        mock_resp.read.return_value = data
        mock_resp.__enter__ = lambda s, *a: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        return mock_resp

    @patch("hello_world.urllib.request.urlopen")
    def test_returns_description_and_temp(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response(FAKE_WEATHER_JSON)
        result = hello_world.get_weather("TestCity")
        self.assertEqual(result, "Sunny, 61°F")

    @patch("hello_world.urllib.request.urlopen")
    def test_network_failure_returns_unavailable(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("network error")
        result = hello_world.get_weather("TestCity")
        self.assertEqual(result, "weather unavailable")


class TestGetWeatherArt(unittest.TestCase):

    def _mock_response(self, data):
        mock_resp = MagicMock()
        mock_resp.read.return_value = data
        mock_resp.__enter__ = lambda s, *a: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        return mock_resp

    @patch("hello_world.urllib.request.urlopen")
    def test_returns_art_string(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response(FAKE_ART)
        result = hello_world.get_weather_art("TestCity")
        self.assertIn("Sunny", result)

    @patch("hello_world.urllib.request.urlopen")
    def test_network_failure_returns_empty_string(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("network error")
        result = hello_world.get_weather_art("TestCity")
        self.assertEqual(result, "")


class TestGreet(unittest.TestCase):

    @patch("hello_world.get_weather_art", return_value="   \\  /\n _ Sunny\n")
    @patch("hello_world.get_weather", return_value="Sunny, 61°F")
    def test_greeting_contains_name(self, mock_weather, mock_art):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            hello_world.greet("Alice")
            output = mock_out.getvalue()
        self.assertIn("Hello, Alice!", output)

    @patch("hello_world.get_weather_art", return_value="   \\  /\n _ Sunny\n")
    @patch("hello_world.get_weather", return_value="Sunny, 61°F")
    def test_greeting_contains_weather(self, mock_weather, mock_art):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            hello_world.greet("World")
            output = mock_out.getvalue()
        self.assertIn("Sunny, 61°F", output)

    @patch("hello_world.get_weather_art", return_value="")
    @patch("hello_world.get_weather", return_value="Sunny, 61°F")
    def test_no_art_when_empty(self, mock_weather, mock_art):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            hello_world.greet()
            output = mock_out.getvalue()
        # Should end after weather line, no blank line + art
        lines = [l for l in output.splitlines() if l]
        self.assertEqual(len(lines), 3)


if __name__ == "__main__":
    unittest.main()
