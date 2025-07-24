from sqlalchemy.orm import Session
from datetime import datetime
from apps.verifications.interface import VerificationMethod
from apps.verifications.crud import record_credential, mark_used

class GeofenceMethod(VerificationMethod):
    name = "geofence"

    def generate_credential(self, db: Session, ticket_id: int, geo_info: dict) -> dict:
        # geo_info = { "lat": ..., "lng": ..., "radius_meters": ..., "entry_window": {"start": ..., "end": ...} }
        record_credential(db, ticket_id, self.name, geo_info)
        return geo_info

    def verify_credential(self, db: Session, ticket_id: int, presented: dict) -> bool:
        # presented = { "lat": ..., "lng": ..., "timestamp": ... }
        from geopy.distance import geodesic

        stored = self.get_stored_credential(db, ticket_id)
        center = (stored["lat"], stored["lng"])
        user_loc = (presented["lat"], presented["lng"])
        distance = geodesic(center, user_loc).meters

        now = datetime.fromisoformat(presented["timestamp"])
        start = datetime.fromisoformat(stored["entry_window"]["start"])
        end = datetime.fromisoformat(stored["entry_window"]["end"])

        if distance <= stored["radius_meters"] and start <= now <= end:
            return mark_used(db, ticket_id, self.name, {"checked_in": True, "distance": distance})
        return False
        # If the user is within the geofence and the time is within the entry window, mark as used
        # Otherwise, return False