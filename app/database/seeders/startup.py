from sqlmodel import select, Session

from app.features.auth.models import Permission, Role
from app.features.auth.permissions import PERMISSION_METADATA


def sync_permissions(db: Session):
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


def sync_roles(db: Session):
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
