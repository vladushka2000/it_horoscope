# thirdparty
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings


class PostgresConfig(BaseSettings):
    user: str = Field(
        alias="POSTGRES_USER", title="Имя пользователя БД", default="admin"
    )
    password: str = Field(
        alias="POSTGRES_AI_AGENTS_PASSWORD", title="Пароль пользователя БД", default="admin"
    )
    host: str = Field(
        alias="POSTGRES_HOST", title="Хост подключения к БД", default="localhost"
    )
    port: int = Field(
        alias="POSTGRES_PORT", default=5432, title="Порт подключения к БД"
    )
    db_name: str = Field(alias="POSTGRES_DB", title="Имя БД", default="it_horoscope")
    connection_pool_size: int = Field(
        alias="POOL_SIZE", title="Размер пула соединений", default=10
    )

    @property
    def postgres_dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.db_name,
        )


pg_config = PostgresConfig()
