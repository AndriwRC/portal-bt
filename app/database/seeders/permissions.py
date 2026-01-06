from sqlmodel import select, Session

from app.features.auth.models import Permission
from app.features.auth.permissions import PERMISSION_METADATA

from .base import BaseSeeder


class PermissionSeeder(BaseSeeder):

    def run(self, db: Session):
        """Sync permissions on database.

        Check if the default permissions exists in database and load them if not.
        This functions should be called on app startup.

        Parameters
        ----------
        db: Session
            The session to access the database.
        """
        for permissions_enum, meta in PERMISSION_METADATA.items():
            perm = db.exec(
                select(Permission).where(Permission.name == permissions_enum.value)
            ).first()

            if not perm:
                perm = Permission(
                    name=permissions_enum.value,
                    label=meta["label"],
                    module=meta["module"],
                    description=meta.get("description"),
                )
                db.add(perm)

        db.commit()
