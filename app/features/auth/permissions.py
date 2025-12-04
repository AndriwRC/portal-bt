from enum import Enum


class PermissionEnum(str, Enum):
    MANAGE_STOREROOM = "manage_storeroom"
    HANDLE_HOURS = "handle_hours"


PERMISSION_METADATA = {
    PermissionEnum.MANAGE_STOREROOM: {
        "label": "Administrar Bodega",
        "module": "Bodega",
        "description": "Ingresar y recibir elementos de bodega.",
    },
    PermissionEnum.HANDLE_HOURS: {
        "label": "Gestionar Horas",
        "module": "Horas",
        "description": "Aprobar y rechazar horas ingresadas por los becados.",
    },
}
