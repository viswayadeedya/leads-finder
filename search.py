import httpx 
from settings import settings
from models import Review, GoogleProfile


def check_limit(limit):
    if limit > 20 :
            raise ValueError("Limit cannot higher than 20")
    if limit == 0 :
            raise ValueError("Limit cannot be zero")
    if limit < 1 :
            raise ValueError("Limit cannot be negative")

def to_profile(place: dict) -> GoogleProfile:
    return GoogleProfile(
        id=place["id"],
        name=place.get("displayName", {}).get("text", ""),
        rating=place.get("rating"),
        review_count=place.get("userRatingCount"),
        reviews=[
            Review(
                rating=review.get("rating"),
                text=review.get("text", {}).get("text", ""),
                published=review.get("relativePublishTimeDescription", ""),
            )
            for review in place.get("reviews", [])
        ],
        hours=place.get("regularOpeningHours", {}).get("weekdayDescriptions", []),
        photo_count=len(place.get("photos", [])),
        website=place.get("websiteUri"),
        phone=place.get("nationalPhoneNumber"),
    )

def search(trade, city, state, limit):
    check_limit(limit)

    custom_headers= {
        'X-Goog-FieldMask': 'places.id,places.displayName,places.rating,places.userRatingCount,places.reviews,places.regularOpeningHours,places.photos,places.websiteUri,places.nationalPhoneNumber',
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
    data = response.json()
    google_profile = []
    for i in data.get("places", []):
          google_profile.append(to_profile(i))
    return google_profile

