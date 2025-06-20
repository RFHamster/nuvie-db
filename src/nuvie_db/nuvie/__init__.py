from src.nuvie_db.nuvie.core import SQLModelNuvie as SQLModelNuvie

## Import all Models here
## To alembic see they

from src.nuvie_db.nuvie.models.patient import Patient

print(Patient.__tablename__)
from src.nuvie_db.nuvie.models.user import User
