from dataclasses import dataclass
from uuid import UUID

from app.application.common.dto.user_dto import UserDTO
from app.application.common.persistence.user_gateway import UserGateway


@dataclass(frozen=True)
class GetUserByIdQuery:
    user_id: UUID


class GetUserById:
    def __init__(self, gateway: UserGateway) -> None:
        self.gateway = gateway

    async def execute(self, query: GetUserByIdQuery) -> UserDTO | None:
        user = await self.gateway.with_id(query.user_id)

        return user
