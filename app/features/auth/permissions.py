from enum import Enum


class PermissionEnum(str, Enum):
    USER_VIEW = "user.view"
    ROLE_MANAGE = "role.manage"


PERMISSION_METADATA = {
    PermissionEnum.USER_VIEW: {
        "label": "Ver usuarios",
        "module": "Usuarios",
        "description": "Listar los usuarios registrados en la plataforma."
    },
    PermissionEnum.ROLE_MANAGE: {
        "label": "Administrar roles",
        "module": "Roles",
        "description": "Crear, asignar, editar y eliminar roles.",
    }
}
