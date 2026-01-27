from enum import Enum


class PermissionEnum(str, Enum):
    USER_VIEW = "user.view"
    ROLE_MANAGE = "role.manage"
    HOUR_MANAGE = "hour.manage"
    SCHOOL_MANAGE = "school.manage"


PERMISSION_METADATA = {
    PermissionEnum.USER_VIEW: {
        "label": "Ver usuarios",
        "module": "Usuarios",
        "description": "Listar los usuarios registrados en la plataforma.",
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
