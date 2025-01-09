from uuid import UUID

from app.domain.model.enums.languages import Languages
from app.domain.shared.base_entity import BaseEntity


class Language(BaseEntity[UUID]):
    def __init__(
        self,
        language_id: UUID,
        user_id: UUID,
        language: Languages,
    ) -> None:
        super().__init__(language_id)

        self.user_id = user_id
        self.language_id = language_id
        self.language = language
