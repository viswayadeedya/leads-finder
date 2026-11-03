import httpx 
from settings import settings


def check_limit(limit):
    if limit > 20 :
            raise ValueError("Limit cannot higher than 20")
    if limit == 0 :
            raise ValueError("Limit cannot be zero")
    if limit < 1 :
            raise ValueError("Limit cannot be negative")

def search(trade, city, state, limit):
    check_limit(limit)

    custom_headers= {
        'X-Goog-FieldMask': 'places.id',
        'X-Goog-Api-Key': settings.google_api_key.get_secret_value()
                     }

    response = httpx.post("https://places.googleapis.com/v1/places:searchText",
                          headers= custom_headers,
                          json = {
                              'textQuery': trade + " in " + city+ ", " + state,
                              'pageSize': limit
                              },
                            timeout=settings.http_timeout_seconds
                        )
    response.raise_for_status()
    return response.json()


