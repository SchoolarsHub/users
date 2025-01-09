from app.domain.shared.exception import DomainError


class UserSkillNotFoundError(DomainError):
    pass


class UserSkillAlreadyExistsError(DomainError):
    pass
