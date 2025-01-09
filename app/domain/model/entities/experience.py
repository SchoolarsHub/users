from datetime import date
from uuid import UUID

from app.domain.model.value_objects.experience_value_objects import ExperiencesPeriod
from app.domain.shared.base_entity import BaseEntity
from app.domain.shared.unit_of_work import UnitOfWorkTracker


class Experience(BaseEntity[UUID]):
    def __init__(
        self,
        experience_id: UUID,
        user_id: UUID,
        specialization: str,
        company_name: str,
        period: ExperiencesPeriod,
        description: str,
        unit_of_work: UnitOfWorkTracker,
    ) -> None:
        super().__init__(experience_id)

        self.experience_id = experience_id
        self.user_id = user_id
        self.specialization = specialization
        self.company_name = company_name
        self.period = period
        self.description = description
        self.unit_of_work = unit_of_work

    def change_specialization(self, new_specialization: str) -> None:
        self.specialization = new_specialization
        self.unit_of_work.register_dirty(self)

    def change_company_name(self, new_company_name: str) -> None:
        self.company_name = new_company_name
        self.unit_of_work.register_dirty(self)

    def change_experience_period(self, start_date: date, finish_date: date) -> None:
        experience_period = ExperiencesPeriod(start_date, finish_date)

        self.period = experience_period
        self.unit_of_work.register_dirty(self)

    def change_description(self, new_description: str) -> None:
        self.description = new_description
        self.unit_of_work.register_dirty(self)

    def ensure_is_current_job(self) -> bool:
        return self.finish_date == self.start_date

    def delete_experience(self) -> None:
        self.unit_of_work.register_deleted()
