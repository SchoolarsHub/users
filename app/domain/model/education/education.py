from datetime import date
from typing import Self
from uuid import UUID, uuid4

from app.domain.model.education.value_objects import EducationPeriod
from app.domain.shared.base_entity import BaseEntity
from app.domain.shared.unit_of_work import UnitOfWorkTracker


class Education(BaseEntity[UUID]):
    def __init__(
        self,
        education_id: UUID,
        user_id: UUID,
        unit_of_work: UnitOfWorkTracker,
        period: EducationPeriod,
        organization: str,
        degree: str,
        field: str,
        grade: str | None = None,
    ) -> None:
        super().__init__(education_id)

        self.education_id = education_id
        self.user_id = user_id
        self.unit_of_work = unit_of_work
        self.period = period
        self.organization = organization
        self.degree = degree
        self.field = field
        self.grade = grade

    @classmethod
    def create_education(
        cls,
        user_id: UUID,
        unit_of_work: UnitOfWorkTracker,
        start_date: date,
        finish_date: date,
        organization: str,
        degree: str,
        field: str,
        grade: str | None = None,
    ) -> Self:
        education = cls(uuid4(), user_id, unit_of_work, start_date, finish_date, organization, degree, field, grade)

        unit_of_work.register_new(education)

        return education

    def change_organization(self, new_organization: str) -> None:
        self.organization = new_organization
        self.unit_of_work.register_dirty(self)

    def change_degree(self, new_degree: str) -> None:
        self.degree = new_degree
        self.unit_of_work.register_dirty(self)

    def change_field(self, new_field: str) -> None:
        self.field = new_field
        self.unit_of_work.register_dirty(self)

    def change_grade(self, new_grade: str | None) -> None:
        self.grade = new_grade
        self.unit_of_work.register_dirty(self)

    def change_education_period(self, start_date: date, finish_date: date) -> None:
        education_period = EducationPeriod(start_date, finish_date)

        self.period = education_period
        self.unit_of_work.register_dirty(self)

    def ensure_is_current_studying(self) -> bool:
        return self.finish_date == self.start_date

    def delete_education(self) -> None:
        self.unit_of_work.register_deleted()
