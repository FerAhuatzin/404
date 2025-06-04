from app.models.base import Base
from app.models.user import User
from app.models.individual import Individual
from app.models.organization import Organization
from app.models.authToken import AuthToken
from app.models.trips import Trip
from app.models.activitySegments import ActivitySegment

# Importa aquí todos los modelos que crees
__all__ = ["Base", "User", "Individual", "Organization", "AuthToken", "Trip", "ActivitySegment"]
