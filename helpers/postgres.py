from __future__ import annotations

from typing import TYPE_CHECKING

from asyncpg import UniqueViolationError

from .models.account import Account

if TYPE_CHECKING:
    from asyncpg import Pool


class AccountExists(Exception):
    pass


class PostgresManager:
    def __init__(self, pool: Pool):
        self.pool = pool

    async def get_account(self, user_id: int) -> Account | None:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM accounts WHERE user_id = $1",
                user_id
            )

        if row is not None:
            account = Account(**row)
            return account

        return None

    async def create_account(self, user_id: int) -> None:
        async with self.pool.acquire() as conn:
            try:
                await conn.execute(
                    "INSERT INTO accounts(user_id) VALUES($1)",
                    user_id
                )
            except UniqueViolationError as e:
                raise AccountExists from e

    async def update_account(
        self,
        user_id: int,
        *,
        description: str
    ):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "UPDATE accounts SET description = $1 WHERE user_id = $2",
                description,
                user_id
            )
            