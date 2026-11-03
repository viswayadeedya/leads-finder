from pydantic import BaseModel


class Review(BaseModel):
    rating: int | None = None
    text: str = ""
    published: str = ""


class GoogleProfile(BaseModel):
    id: str
    name: str = ""
    rating: float | None = None
    review_count: int | None = None
    reviews: list[Review] = []
    hours: list[str] = []
    photo_count: int = 0
    website: str | None = None
    phone: str | None = None

