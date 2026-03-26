import datetime
import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

def get_weather(city="Columbus,Ohio"):
    url = f"https://wttr.in/{city}?format=j1"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read())
        current = data["current_condition"][0]
        temp_f = current["temp_F"]
        desc = current["weatherDesc"][0]["value"]
        return f"{desc}, {temp_f}°F"
    except Exception:
        return "weather unavailable"

def get_weather_art(city="Columbus,Ohio"):
    url = f"https://wttr.in/{city}?0"
    req = urllib.request.Request(url, headers={"User-Agent": "curl/7.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.read().decode("utf-8")
    except Exception:
        return ""

def greet(name="World"):
    today = datetime.date.today().strftime("%B %d, %Y")
    weather = get_weather()
    art = get_weather_art()
    print(f"Hello, {name}!")
    print(f"Today is {today}.")
    print(f"Columbus, OH: {weather}")
    if art:
        print()
        print(art)

if __name__ == "__main__":
    greet()
