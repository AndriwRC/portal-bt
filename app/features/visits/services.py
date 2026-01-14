from sqlmodel import Session
from fastapi import HTTPException, status

from app.core.constants import CRUDMessages
from app.core.services.base import BaseService, CreateServiceMixin
from app.core.schemas.http import HTTPResponseModel, error_detail
from sqlalchemy.exc import IntegrityError

from .models import Visit
from app.features.users.models import User
from app.features.schools.models import School
from .queries import VisitQueries
from app.features.users.queries import UserQueries
from app.features.schools.queries import SchoolQueries
from .schemas import VisitCreate, VisitUpdate


class VisitService(BaseService[Visit, VisitQueries], CreateServiceMixin[VisitCreate]):
    model = Visit
    query_class = VisitQueries

    def __init__(self, db: Session):
        super().__init__(db)

        self.queries = VisitQueries(db)

        self.user_queries = UserQueries(db)

        self.school_queries = SchoolQueries(db)

    def create(self, data: VisitCreate, user_obj: User):
        # Get school record
        school_record = self.school_queries.get_by_id(data.school_id)

        # Verify if school exist on the bd
        if not school_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_detail(
                    msg=CRUDMessages.CREATE_FAILED,
                    ctx=CRUDMessages.GET_NOT_FOUND,
                ),
            )

        # Validate if doesn't exist a visit in the same range on time with to the same school
        has_conflict = self.queries.check_overlap(
            school_id=data.school_id,
            visit_date=data.date,
            start=data.time_start,
            end=data.time_end,
        )

        if has_conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=error_detail(
                    msg=CRUDMessages.CREATE_FAILED, ctx=CRUDMessages.CONFLICT_SCHEDULE
                ),
            )

        # Create the object with all the fields
        visit_obj = Visit(**data.model_dump(), responsible_id=user_obj.id)

        # Try to create the objet and load the relationships
        try:
            created_visit = self.queries.create(visit_obj)

            created_visit.responsible = user_obj
            created_visit.school = school_record

            return HTTPResponseModel(
                status_code=status.HTTP_201_CREATED,
                message=CRUDMessages.CREATE_SUCCESS,
                data=created_visit,
            )
        # In case some oh the relationships doesn't exist
        except IntegrityError as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_detail(
                    msg=CRUDMessages.CREATE_FAILED,
                    ctx=str(ex.args),
                ),
            )

    def update(self, id: int, data: VisitUpdate):
        # Verify if the visit exists
        record = self.queries.get_by_id(id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_detail(
                    msg=CRUDMessages.UPDATE_FAILED,
                    ctx=CRUDMessages.GET_NOT_FOUND,
                ),
            )

        # Save the new information
        new_data = data.model_dump(exclude_unset=True)

        if any(i in new_data for i in ["date", "time_start", "time_end"]):
            check_date = data.date or record.date
            check_start = data.time_start or record.time_start
            check_end = data.time_end or record.time_end

            has_conflict = self.queries.check_overlap(
                school_id=record.school_id,
                visit_date=check_date,
                start=check_start,
                end=check_end,
                exclude_visit_id=id,  # <-- Pasamos el ID actual para no chocar con nosotros mismos
            )

            if has_conflict:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=error_detail(
                        msg=CRUDMessages.UPDATE_FAILED,
                        ctx=CRUDMessages.CONFLICT_SCHEDULE,
                    ),
                )

        # Verify if the assignee ids exists
        assignee_ids = new_data.pop("assignee_ids", None)
        if assignee_ids is not None:
            users = self.user_queries.get_by_ids(assignee_ids)
            record.assignees = users

        for key, value in new_data.items():
            setattr(record, key, value)

        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)

        return HTTPResponseModel(
            status_code=status.HTTP_200_OK,
            message=CRUDMessages.UPDATE_SUCCESS,
            data=record,
        )

    def delete(self, id: int):
        record = self.queries.get_by_id(id)

        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_detail(
                    msg=CRUDMessages.DELETE_FAILED,
                    ctx=CRUDMessages.GET_NOT_FOUND,
                ),
            )

        _ = record.school  # Esto carga school
        _ = record.responsible  # Esto carga responsible
        _ = record.assignees  # Esto carga assignees
        deleted = self.queries.delete(record)

        return HTTPResponseModel(
            status_code=status.HTTP_200_OK,
            message=CRUDMessages.DELETE_SUCCESS,
            data=deleted,
        )
