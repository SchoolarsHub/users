from app.domain.models.user.repositories.user_repository import UserRepository


class AccessControlService:
    def __init__(
        self,
        repository: UserRepository,
    ) -> None:
        self._repository = repository
