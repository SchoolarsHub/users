from app.domain.shared.exception import DomainError


class ExperienceNotFoundError(DomainError):
    pass


class ExperienceAlreadyExistsError(DomainError):
    pass
