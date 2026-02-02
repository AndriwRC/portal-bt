from enum import Enum


class PermissionEnum(str, Enum):
    USER_VIEW = "user.manage"
    ROLE_MANAGE = "role.manage"
    HOUR_MANAGE = "hour.manage"
    SCHOOL_MANAGE = "school.manage"


PERMISSION_METADATA = {
    PermissionEnum.USER_VIEW: {
        "label": "Administrar usuarios",
        "module": "Usuarios",
        "description": "Crear, editar, actualizar y eliminar los usuarios registrados en la plataforma.",
    },
    PermissionEnum.ROLE_MANAGE: {
        "label": "Administrar roles",
        "module": "Roles",
        "description": "Crear, asignar, editar y eliminar roles.",
    },
    PermissionEnum.HOUR_MANAGE: {
        "label": "Administrar horas",
        "module": "Horas",
        "description": "Aprobar o rechazar horas.",
    },
    PermissionEnum.SCHOOL_MANAGE: {
        "label": "Eliminar colegios",
        "module": "Schools",
        "description": "Eliminar los colegios registrados en la plataforma",
    },
}
