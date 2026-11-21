import requests
import sys

# ==========================================
# WEATHER INFORMATION SYSTEM
# ==========================================

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


# STEP 1: LOCATION SEARCH FUNCTION

def search_location(place, state, country_code):

    search_name = place

    if state:
        search_name = f"{place}, {state}"

    params = {
        "name": search_name,
        "count": 10,
        "language": "en",
        "format": "json"
    }

    if country_code:
        params["countryCode"] = country_code

    try:
        response = requests.get(
            GEO_URL,
            params=params,
            timeout=20
        )

        response.raise_for_status()
        data = response.json()

        if data.get("error"):
            print("API Error:", data.get("reason"))
            return None

        return data.get("results", [])

    except requests.exceptions.RequestException as e:
        print("Location search failed:", e)
        return None


# STEP 2: WEATHER CONDITION FUNCTION

def get_weather_condition(code):

    conditions = {
        0: "Clear Sky",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing Rime Fog",
        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Dense Drizzle",
        56: "Freezing Drizzle",
        57: "Heavy Freezing Drizzle",
        61: "Slight Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",
        66: "Freezing Rain",
        67: "Heavy Freezing Rain",
        71: "Slight Snow",
        73: "Moderate Snow",
        75: "Heavy Snow",
        77: "Snow Grains",
        80: "Rain Showers",
        81: "Moderate Rain Showers",
        82: "Violent Rain Showers",
        85: "Snow Showers",
        86: "Heavy Snow Showers",
        95: "Thunderstorm",
        96: "Thunderstorm with Hail",
        99: "Heavy Thunderstorm with Hail"
    }

    return conditions.get(code, "Unknown Condition")


# STEP 3: WEATHER FETCH FUNCTION

def get_weather(latitude, longitude):

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "is_day,"
            "precipitation,"
            "weather_code,"
            "wind_speed_10m,"
            "wind_direction_10m"
        ),

        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh",
        "precipitation_unit": "mm",
        "timezone": "auto"
    }

    try:
        response = requests.get(
            WEATHER_URL,
            params=params,
            timeout=20
        )

        response.raise_for_status()
        data = response.json()

        if data.get("error"):
            print("Weather API Error:", data.get("reason"))
            return None

        return data.get("current")

    except requests.exceptions.RequestException as e:
        print("Weather data failed:", e)
        return None


# STEP 4: MAIN PROGRAM

def main():

    print("\n====================================")
    print("       WEATHER INFORMATION SYSTEM")
    print("====================================")

    place = input(
        "Enter City/Village Name: "
    ).strip()

    state = input(
        "Enter State (or leave blank): "
    ).strip()

    country_code = input(
        "Enter Country Code (e.g. IN): "
    ).strip().upper()

    if not place:
        print("Error: Location cannot be empty.")
        return

    print("\nSearching location...")

    locations = search_location(
        place, state, country_code
    )

    if locations is None:
        return

    # STEP 5: NEARBY LOCATION OPTION

    if not locations:

        print("\nLocation not found.")

        nearby = input(
            "Enter nearby city name (e.g. Phagwara): "
        ).strip()

        if not nearby:
            print("No nearby location entered.")
            return

        print("\nSearching nearby location...")

        locations = search_location(
            nearby, state, country_code
        )

        if locations is None:
            return

        if not locations:
            print("No matching location found.")
            return

    # STEP 6: DISPLAY LOCATIONS

    print("\n========== MATCHING LOCATIONS ==========")

    for i, loc in enumerate(locations, start=1):

        print(f"\n{i}. {loc.get('name', 'Unknown')}")
        print("   State:", loc.get("admin1", "N/A"))
        print("   District:", loc.get("admin2", "N/A"))
        print("   Country:", loc.get("country", "N/A"))

    # STEP 7: SELECT LOCATION

    while True:

        try:

            choice = int(input(
                "\nSelect location number: "
            ))

            if 1 <= choice <= len(locations):
                break

            print("Invalid selection. Try again.")

        except ValueError:
            print("Please enter a valid number.")

    selected = locations[choice - 1]

    latitude = selected["latitude"]
    longitude = selected["longitude"]

    # STEP 8: FETCH WEATHER

    print("\nFetching current weather...")

    current = get_weather(latitude, longitude)

    if not current:
        print("Weather information unavailable.")
        return

    # STEP 9: EXTRACT WEATHER DATA

    temperature = current.get("temperature_2m")
    feels_like = current.get("apparent_temperature")
    humidity = current.get("relative_humidity_2m")
    wind_speed = current.get("wind_speed_10m")
    wind_direction = current.get("wind_direction_10m")
    precipitation = current.get("precipitation")
    weather_code = current.get("weather_code")
    is_day = current.get("is_day")

    condition = get_weather_condition(weather_code)

    # STEP 10: DISPLAY WEATHER REPORT

    print("\n====================================")
    print("           WEATHER REPORT")
    print("====================================")

    print("City/Village:", selected.get("name", "N/A"))
    print("State:", selected.get("admin1", "N/A"))
    print("District:", selected.get("admin2", "N/A"))
    print("Country:", selected.get("country", "N/A"))

    print("------------------------------------")

    print("Latitude:", latitude)
    print("Longitude:", longitude)

    print("------------------------------------")

    print("Date and Time:", current.get("time", "N/A"))
    print("Temperature:", temperature, "°C")
    print("Feels Like:", feels_like, "°C")
    print("Humidity:", humidity, "%")
    print("Wind Speed:", wind_speed, "km/h")
    print("Wind Direction:", wind_direction, "°")
    print("Precipitation:", precipitation, "mm")
    print("Weather Condition:", condition)

    if is_day == 1:
        print("Time: Day")
    elif is_day == 0:
        print("Time: Night")
    else:
        print("Time: N/A")

    print("------------------------------------")
    print("Weather Report Generated Successfully!")
    print("====================================")


# STEP 11: RUN PROGRAM

if __name__ == "__main__":
    main()