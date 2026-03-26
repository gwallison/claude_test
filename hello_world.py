import datetime
import urllib.request
import json

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

def greet(name="World"):
    today = datetime.date.today().strftime("%B %d, %Y")
    weather = get_weather()
    print(f"Hello, {name}!")
    print(f"Today is {today}.")
    print(f"Columbus, OH: {weather}")

if __name__ == "__main__":
    greet()
