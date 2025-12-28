from typing import Optional
from pathlib import Path
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"


class AuthSettings(BaseSettings):
    """Authentication settings"""
    model_config = SettingsConfigDict(
        env_prefix="SETTINGS__",
        env_file=str(ENV_FILE),
        extra="ignore"
    )
    
    secret_key: str = Field(..., description="Secret key for JWT")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=6000)


class OpenAISettings(BaseSettings):
    """OpenAI API settings"""
    model_config = SettingsConfigDict(
        env_prefix="OPENAI__",
        env_file=str(ENV_FILE),
        extra="ignore"
    )
    
    api_key: str = Field(..., description="OpenAI API key")
    embedding_model: str = Field(default="text-embedding-3-large")
    model_name: str = Field(default="gpt-4o")
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)


class PostgresSettings(BaseSettings):
    """PostgreSQL settings"""
    model_config = SettingsConfigDict(
        env_prefix="POSTGRES__",
        env_file=str(ENV_FILE),
        extra="ignore"
    )
    
    host: str = Field(default="postgres")
    port: int = Field(default=5432)
    username: str = Field(...)
    password: str = Field(...)
    db: str = Field(...)

    @computed_field
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.db}"

    @computed_field
    @property
    def async_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.db}"


class QdrantSettings(BaseSettings):
    """Qdrant settings"""
    model_config = SettingsConfigDict(
        env_prefix="QDRANT__",
        env_file=str(ENV_FILE),
        extra="ignore"
    )
    
    host: str = Field(default="qdrant")
    port: int = Field(default=6333)

    @computed_field
    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"


class MinioSettings(BaseSettings):
    """MinIO settings"""
    model_config = SettingsConfigDict(
        env_prefix="MINIO__",
        env_file=str(ENV_FILE),
        extra="ignore"
    )
    
    host: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)

    @computed_field
    @property
    def endpoint(self) -> str:
        return f"http://{self.host}"


class RedisSettings(BaseSettings):
    """Redis settings"""
    model_config = SettingsConfigDict(
        env_prefix="REDIS__",
        env_file=str(ENV_FILE),
        extra="ignore"
    )
    
    host: str = Field(default="redis")
    port: int = Field(default=6379)

    @computed_field
    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/0"


class Settings(BaseSettings):
    """Main settings"""
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        extra="ignore"
    )
    
    base_url: str = Field(default="http://localhost:8000")
    
    auth: Optional[AuthSettings] = None
    openai: Optional[OpenAISettings] = None
    postgres: Optional[PostgresSettings] = None
    qdrant: Optional[QdrantSettings] = None
    minio: Optional[MinioSettings] = None
    redis: Optional[RedisSettings] = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth = AuthSettings()
        self.openai = OpenAISettings()
        self.postgres = PostgresSettings()
        self.qdrant = QdrantSettings()
        self.minio = MinioSettings()
        self.redis = RedisSettings()


settings = Settings()
