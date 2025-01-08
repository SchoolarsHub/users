from datetime import UTC, date, datetime
from uuid import UUID

from app.domain.model.education.education import Education
from app.domain.model.education.events import (
    EducationCreated,
    EducationDegreeChanged,
    EducationDeleted,
    EducationFieldChanged,
    EducationGradeChanged,
    EducationOrganizationChanged,
    EducationPeriodChanged,
)
from app.domain.model.education.exceptions import EducationAlreadyExistsError, EducationNotFoundError
from app.domain.model.experience.events import (
    ExperienceCompanyNameChanged,
    ExperienceCreated,
    ExperienceDeleted,
    ExperienceDescriptionChanged,
    ExperiencePeriodChanged,
    ExperienceSpecializationChanged,
)
from app.domain.model.experience.exceptions import ExperienceAlreadyExistsError, ExperienceNotFoundError
from app.domain.model.experience.experience import Experience
from app.domain.model.user.enums import Languages, Specializations, Statuses
from app.domain.model.user.events import (
    BioChanged,
    DateOfBirthChanged,
    EmailChanged,
    FullnameChanged,
    LanguagesChanged,
    SkillsChanged,
    SpecializationChanged,
    UserActivated,
    UserPermanentlyDeleted,
    UserRecoveried,
    UserTemporarilyDeleted,
)
from app.domain.model.user.exceptions import InactiveUserError, UserAlreadyActiveError, UserTemporarilyDeletedError
from app.domain.model.user.value_objects import Fullname
from app.domain.shared.base_entity import BaseEntity
from app.domain.shared.event import Event
from app.domain.shared.unit_of_work import UnitOfWorkTracker


class User(BaseEntity[UUID]):
    def __init__(
        self,
        user_id: UUID,
        unit_of_work: UnitOfWorkTracker,
        fullname: Fullname,
        email: str,
        status: Statuses,
        created_at: datetime,
        bio: str | None = None,
        specialization: Specializations | None = None,
        date_of_birth: date | None = None,
        languages: list[Languages] | None = None,
        education: list[Education] | None = None,
        experiences: list[Experience] | None = None,
        skills: list[str] | None = None,
        deleted_at: datetime | None = None,
    ) -> None:
        super().__init__(user_id)

        self.unit_of_work = unit_of_work
        self.user_id = user_id
        self.fullname = fullname
        self.email = email
        self.status = status
        self.created_at = created_at
        self.deleted_at = deleted_at
        self.bio = bio
        self.date_of_birth = date_of_birth
        self.languages = languages or []
        self.specialization = specialization
        self.skills = skills or []
        self.education = education or []
        self.experiences = experiences or []

        self._events: list[Event] = []

    def record_event(self, event: Event) -> None:
        self._events.append(event)

    def raise_events(self) -> list[Event]:
        events = self._events.copy()
        self._events.clear()

        return events

    def change_bio(self, new_bio: str | None) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        self.bio = new_bio
        self.unit_of_work.register_dirty(self)
        self.record_event(BioChanged(user_id=self.user_id, bio=new_bio))

    def change_date_of_birth(self, new_date_of_birth: date | None) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        self.date_of_birth = new_date_of_birth
        self.unit_of_work.register_dirty(self)
        self.record_event(DateOfBirthChanged(user_id=self.user_id, date_of_birth=new_date_of_birth))

    def change_languages(self, new_languages: list[Languages]) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        self.languages = new_languages
        self.unit_of_work.register_dirty(self)
        self.record_event(LanguagesChanged(user_id=self.user_id, languages=new_languages))

    def change_skills(self, new_skills: list[str]) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        self.skills = new_skills
        self.unit_of_work.register_dirty(self)
        self.record_event(SkillsChanged(user_id=self.user_id, skills=new_skills))

    def change_specialization(self, specialization: Specializations | None) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        self.specialization = specialization
        self.unit_of_work.register_dirty(self)
        self.record_event(SpecializationChanged(user_id=self.user_id, specialization=specialization))

    def add_education(self, organization: str, degree: str, education_field: str, grade: str | None, start_date: date, finish_date: date) -> UUID:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        for education in self.education:
            if education.organization == organization and education.degree == degree and education.grade == grade:
                raise EducationAlreadyExistsError(f"Education {organization} {degree} {grade} already exists")

        education = Education.create_education(self.user_id, self.unit_of_work, start_date, finish_date, organization, degree, education_field, grade)

        self.education.append(education)
        self.record_event(
            EducationCreated(education.education_id, self.user_id, organization, degree, education_field, grade, start_date, finish_date)
        )

        return education.education_id

    def change_education_organization(self, education_id: UUID, new_organization: str) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        for education in self.education:
            if education.education_id == education_id:
                education.change_organization(new_organization)
                self.record_event(EducationOrganizationChanged(education_id, self.user_id, new_organization))

        raise EducationNotFoundError(f"Education with id: {education_id} not found")

    def change_education_degree(self, education_id: UUID, new_degree: str) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        for education in self.education:
            if education.education_id == education_id:
                education.change_degree(new_degree)
                self.record_event(EducationDegreeChanged(education_id, self.user_id, new_degree))

        raise EducationNotFoundError(f"Education with id: {education_id} not found")

    def change_education_field(self, education_id: UUID, new_field: str) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        for education in self.education:
            if education.education_id == education_id:
                education.change_field(new_field)
                self.record_event(EducationFieldChanged(education_id, self.user_id, new_field))

        raise EducationNotFoundError(f"Education with id: {education_id} not found")

    def change_education_grade(self, education_id: UUID, new_garde: str | None) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        for education in self.education:
            if education.education_id == education_id:
                education.change_grade(new_garde)
                self.record_event(EducationGradeChanged(education_id, self.user_id, new_garde))

        raise EducationNotFoundError(f"Education with id: {education_id} not found")

    def change_education_period(self, education_id: UUID, start_date: date, finish_date: date) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        for education in self.education:
            if education.education_id == education_id:
                education.change_period(start_date, finish_date)
                self.record_event(EducationPeriodChanged(education_id, self.user_id, start_date, finish_date))

        raise EducationNotFoundError(f"Education with id: {education_id} not found")

    def remove_education(self, education_id: UUID) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        for education in self.education:
            if education.education_id == education_id:
                education.delete_education()
                self.record_event(EducationDeleted(education_id, self.user_id))

        raise EducationNotFoundError(f"Education with id: {education_id} not found")

    def add_experience(self, specialization: str, company_name: str, start_date: date, finish_date: date, description: str) -> UUID:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        for experience in self.experiences:
            if experience.company_name == company_name and experience.specialization == specialization:
                raise ExperienceAlreadyExistsError(f"Experience {company_name} {start_date} {finish_date} already exists")

        experience = Experience.create_experience(self.user_id, self.unit_of_work, specialization, company_name, start_date, finish_date, description)

        self.experiences.append(experience)
        self.record_event(
            ExperienceCreated(experience.experience_id, self.user_id, specialization, company_name, description, start_date, finish_date)
        )

        return experience.experience_id

    def change_experience_specialization(self, experience_id: UUID, new_specialization: str) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        for experience in self.experiences:
            if experience.experience_id == experience_id:
                experience.change_specialization(new_specialization)
                self.record_event(ExperienceSpecializationChanged(experience_id, self.user_id, new_specialization))

        raise ExperienceNotFoundError(f"Experience with id: {experience_id} not found")

    def change_experience_company_name(self, experience_id: UUID, new_company_name: str) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        for experience in self.experiences:
            if experience.experience_id == experience_id:
                experience.change_company_name(new_company_name)
                self.record_event(ExperienceCompanyNameChanged(experience_id, self.user_id, new_company_name))

        raise ExperienceNotFoundError(f"Experience with id: {experience_id} not found")

    def change_experience_period(self, experience_id: UUID, new_start_date: date, new_finish_date: date) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        for experience in self.experiences:
            if experience.experience_id == experience_id:
                experience.change_period(new_start_date, new_finish_date)
                self.record_event(ExperiencePeriodChanged(experience_id, self.user_id, new_start_date, new_finish_date))

        raise ExperienceNotFoundError(f"Experience with id: {experience_id} not found")

    def change_experience_description(self, experience_id: UUID, description: str) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        for experience in self.experiences:
            if experience.experience_id == experience_id:
                experience.change_description(description)
                self.record_event(ExperienceDescriptionChanged(experience_id, self.user_id, description))

        raise ExperienceNotFoundError(f"Experience with id: {experience_id} not found")

    def remove_experience(self, experience_id: UUID) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        for experience in self.experiences:
            if experience.experience_id == experience_id:
                experience.delete_experience()
                self.record_event(ExperienceDeleted(experience_id, self.user_id))

        raise ExperienceNotFoundError(f"Experience with id: {experience_id} not found")

    def activate_user(self) -> None:
        if self.status == Statuses.ACTIVE:
            raise UserAlreadyActiveError(message=f"User with id: {self.user_id} already have active status")

        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        self.status = Statuses.ACTIVE
        self.unit_of_work.register_dirty(self)
        self.record_event(UserActivated(user_id=self.user_id, status=self.status))

    def change_fullname(self, firstname: str, lastname: str) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        self.fullname = Fullname(firstname, lastname)
        self.unit_of_work.register_dirty(self)
        self.record_event(FullnameChanged(user_id=self.user_id, firstname=firstname, lastname=lastname))

    def change_email(self, email: str) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} is temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        self.email = email
        self.unit_of_work.register_dirty(self)
        self.record_event(EmailChanged(user_id=self.user_id, email=email))

    def delete_user_temporarily(self) -> None:
        if self.status == Statuses.DELETED:
            raise UserTemporarilyDeletedError(message=f"User with id: {self.user_id} already temporarily deleted")

        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        self.status = Statuses.DELETED
        self.deleted_at = datetime.now(UTC)
        self.unit_of_work.register_dirty(self)
        self.record_event(UserTemporarilyDeleted(user_id=self.user_id, deleted_at=self.deleted_at, status=self.status))

    def recovery_user(self) -> None:
        if self.status == Statuses.INACTIVE:
            raise InactiveUserError(message=f"User with id: {self.user_id} is inactive")

        if self.status == Statuses.ACTIVE:
            raise UserAlreadyActiveError(message=f"User with id: {self.user_id} already have active status")

        self.status = Statuses.ACTIVE
        self.deleted_at = None
        self.unit_of_work.register_dirty(self)
        self.record_event(UserRecoveried(user_id=self.user_id, status=self.status))

    def delete_user_permanently(self) -> None:
        for linked_account in self.linked_accounts:
            linked_account.delete_linked_account()

        for experience in self.experiences:
            experience.delete_experience()

        for education in self.education:
            education.delete_education()

        self.record_event(UserPermanentlyDeleted(user_id=self.user_id))
