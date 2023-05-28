import requests

# Get the accessToken that is needed for each API call
AMADEUS_API_KEY = "2Rf0TrqmIvU4wOaqA9rQtOkgcIYqoIZn"
AMADEUS_API_SECRET = "cjmMBywvWTA6pjfP"

url = "https://test.api.amadeus.com/v1/security/oauth2/token"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = {"grant_type": "client_credentials", "client_id": AMADEUS_API_KEY, "client_secret" : AMADEUS_API_SECRET}

# Parameters that are needed for every API call
accessToken = requests.post(url=url, headers=headers, data=data).json()["access_token"]
headers = {"Authorization" : f"Bearer {accessToken}"}

# Getting a list of hotels in a city

def findHotelsByCity(cityCode):
    endpoint = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"
    query = {"cityCode": cityCode}
    response = requests.get(url=endpoint, headers=headers, params=query)
    # hotelList = response.json()["data"]
    # return hotelList
    hotel = response.json()["data"][0]
    # returns the first hotel in the list
    return hotel

# this function doesn't work
def findCheapestHotel(hotelIds):
    endpoint = "https://test.api.amadeus.com/v3//shopping/hotel-offers"
    query = {"hotelIds" : hotelIds}
    response = requests.get(url=endpoint, headers=headers, params=query)
    print(response)
    # hotel = response.json()["data"][0]
    # hotelPrice = hotel["offers"][0]["price"]["total"]
    # print(hotelPrice)

findHotelsByCity("PAR")




