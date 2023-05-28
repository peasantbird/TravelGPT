import requests
from flight_data import FlightData

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = "vmickVy9y-5TmvG0yHIvuM-o-PvLMxbH"

class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    # Tequila Flight Search API Docs: https://tequila.kiwi.com/portal/docs/tequila_api

    def get_IATA_code(self, city_name):
        # Uses Tequila Location API Get to retrieve IATA Code of a city
        # https://tequila.kiwi.com/portal/docs/tequila_api/locations_api
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        query = {
            "term": city_name,
            "location_types": "city"
        }
        headers = {"apikey": TEQUILA_API_KEY}
        response = requests.get(url=location_endpoint, params=query, headers=headers)
        code = response.json()["locations"][0]["code"] # refer to example output to understand this line
        return code

    def get_flight_data(self, origin_city_code, destination_city_code, from_time, to_time):
        # Uses Tequila Search API Get to retrieve flight data for specified flights
        # https://tequila.kiwi.com/portal/docs/tequila_api/search_api
        search_endpoint = f"{TEQUILA_ENDPOINT}/v2/search"
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }
        headers = {"apikey": TEQUILA_API_KEY}
        response = requests.get(url=search_endpoint, params=query, headers=headers)
        try:
            data = response.json()["data"][0]
        except IndexError: # If no flight found, print error msg and return None
            print(f"No flights found for {destination_city_code}.")
            return None

        # If no exceptions raised, means data is non-empty. We can then format data as a flight_data object.
        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: £{flight_data.price}")
        return flight_data