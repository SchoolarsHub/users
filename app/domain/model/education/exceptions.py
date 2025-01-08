from app.domain.shared.exception import DomainError


class EducationNotFoundError(DomainError):
    pass


class EducationAlreadyExistsError(DomainError):
    pass
