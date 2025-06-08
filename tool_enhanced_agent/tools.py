# tools.py
import datetime
import re

def get_current_datetime() -> str:
    """
    Returns the current date and time as a formatted string.
    """
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def calculate_sum(a: float, b: float) -> str:
    """
    Calculates the sum of two numbers and returns it as a string.
    """
    try:
        result = float(a) + float(b)
        return f"The sum of {a} and {b} is {result}."
    except ValueError:
        return "Error: Invalid numbers provided for sum calculation."

def get_weather(city: str) -> str:
    """
    Returns a dummy weather string for a given city.
    In a real scenario, this would call a weather API.
    """
    if not city or not isinstance(city, str) or not city.strip():
        return "Error: City name not provided or invalid for weather lookup."

    # Simple list of cities for more "realistic" dummy responses
    known_cities_weather = {
        "london": "cloudy with a chance of rain",
        "paris": "sunny and pleasant",
        "tokyo": "experiencing light showers",
        "new york": "clear and cool",
        "berlin": "windy"
    }
    city_lower = city.strip().lower()
    if city_lower in known_cities_weather:
        return f"The weather in {city.strip()} is {known_cities_weather[city_lower]}."
    return f"The weather in {city.strip()} is sunny and clear." # Default dummy response

if __name__ == '__main__':
    print("Testing tools...")
    print(f"Current Datetime: {get_current_datetime()}")
    print(f"Calculate Sum (5, 3): {calculate_sum(5, 3)}")
    print(f"Calculate Sum (10.5, 2.1): {calculate_sum(10.5, 2.1)}")
    print(f"Calculate Sum (text, 3): {calculate_sum('text', 3)}") # Error case
    print(f"Weather (London): {get_weather('London')}")
    print(f"Weather (Paris): {get_weather('Paris')}")
    print(f"Weather (UnknownCity): {get_weather('UnknownCity')}")
    print(f"Weather (New York): {get_weather('New York')}")
    print(f"Weather (empty city): {get_weather('')}") # Error case
    print(f"Weather (None city): {get_weather(None)}") # Error case (though type hint helps)
