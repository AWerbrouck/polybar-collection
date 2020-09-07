import argparse
import json
import urllib.request

# This API KEY is for my personal usage.
# Please get your own API KEY here https://openweathermap.org/api,
# because the number of request per day is limited.
OPENWEATHER_API_KEY = "970606528befaa317698cc75083db8b2"
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

USAGE_MESSAGE = """%(prog)s [-c [CITY_NAME]] [-u [UNIT]] [-a [API_KEY]] [-v]

Some examples:
\t%(prog)s
\t%(prog)s -c london
\t%(prog)s -u imperial -v
\t%(prog)s -c florida -u imperial
\t%(prog)s -c "rio de janeiro" -u metric -a 439d4b804bc8187953eb36d2a8c26a02 -v
"""


def getip():
    request = urllib.request.urlopen("https://api.ipify.org?format=json")
    if request.getcode() == 200:
        data = json.loads(request.read())
        return data["ip"]


def getcity():
    request = urllib.request.urlopen("http://ip-api.com/json/" + getip())
    if request.getcode() == 200:
        data = json.loads(request.read())
        return data["city"]


def openweather(city_name, units, api_key, verbose):
    try:
        request = urllib.request.urlopen(
            f"{OPENWEATHER_URL}?q={city_name.replace(' ', '+')}&units={units}&appid={api_key}"
        )
        if request.getcode() == 200:
            data = json.loads(request.read())

            _id = data["id"]
            name = data["name"]
            timezone = data["timezone"]
            country = data["sys"]["country"]
            sunrise = data["sys"]["sunrise"]
            sunset = data["sys"]["sunset"]

            temp = data["main"]["temp"]
            temp_min = data["main"]["temp_min"]
            temp_max = data["main"]["temp_max"]
            humidity = data["main"]["humidity"]
            feels_like = data["main"]["feels_like"]
            description = data["weather"][0]["description"]

            if units == "metric":
                unit = "ºC"
            elif units == "imperial":
                unit = "ºF"
            else:
                unit = " K"

            if verbose:
                print(f"{temp:.0f}{unit}, {description.title()}")
            else:
                print(f"{temp:.0f}{unit}")

        else:
            print(f"E: {request.getcode()}")

    except urllib.error.HTTPError as e:
        print(e)


parser = argparse.ArgumentParser(
    usage=USAGE_MESSAGE, description="Display information about the weather.",
)
parser.add_argument(
    "-c",
    metavar="CITY",
    dest="city",
    type=str,
    nargs=1,
    help="city name (default: try to get your city using your ip address)",
)
parser.add_argument(
    "-u",
    metavar="metric/imperial",
    choices=("metric", "imperial"),
    dest="unit",
    type=str,
    nargs=1,
    help="unit of temperature (default: kevin)",
)
parser.add_argument(
    "-a", metavar="API_KEY", dest="api_key", nargs=1, help="API Key",
)
parser.add_argument(
    "-v", "--verbose", action="store_true", dest="verbose", help="verbose mode",
)

args = parser.parse_args()

openweather(
    args.city[0] if args.city else getcity(),
    args.unit[0] if args.unit else "",
    api_key=args.api_key[0] if args.api_key else OPENWEATHER_API_KEY,
    verbose=args.verbose,
)
