from typing import List
from sqlalchemy import func
from models import GoogleProfile
from sqlalchemy.dialects.postgresql import insert
from db import get_db
from tables import Lead


def load_profile(db, trade: str, city: str, state: str, google_profile: List[GoogleProfile]):
    rows = [
    {
        "place_id": profile.id,
        "trade": trade,
        "city": city,
        "state": state,
        "google_profile": profile.model_dump(),
    }
    for profile in google_profile]
    if rows:  # inserting an empty list raises an error
        stmt = insert(Lead).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=[Lead.place_id],
            set_={"google_profile": stmt.excluded.google_profile, "fetched_at": func.now()},
        )
        db.execute(stmt)
        db.commit()