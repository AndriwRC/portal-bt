from fastapi import Response, status
from app.core.models import APIResponse, BaseService
from .queries import UserQueries


class UserService(BaseService):
    queries = UserQueries

    def get_all(self, response: Response):
        # Business logic, permissions, exceptions
        response.status_code = status.HTTP_200_OK
        return APIResponse(
            message="",
            data=self.queries.get_all(),
        )
