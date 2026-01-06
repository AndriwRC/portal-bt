from sqlmodel import select, Session

from .base import BaseSeeder
from app.features.auth.models import Permission, Role


class RoleSeeder(BaseSeeder):

    def run(self, db: Session):
        """Sync roles on database.

        Check if the default roles exists in database and load them if not.

        Parameters
        ----------
        db: Session
            The session to access the database.
        """

        admin = db.exec(select(Role).where(Role.name == "admin")).first()

        if not admin:
            admin = Role(name="admin", is_protected=True)
            db.add(admin)

        db.commit()
        db.refresh(admin)

        permissions = db.exec(select(Permission)).all()

        for permission in permissions:
            if permission not in admin.permissions:
                admin.permissions.append(permission)

        db.commit()
