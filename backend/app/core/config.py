from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "thy500"

    cors_allow_origins: str = "*"

    # AWS / S3 (private)
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    aws_region: str = "eu-north-1"
    s3_bucket: str | None = None
    s3_prefix: str = ""
    presign_expires_seconds: int = 900

    # JWT settings
    jwt_secret_key: str = ""
    jwt_algorithm: str = ""
    access_token_expire_minutes: int = 120  # 2 hours

    # Admin seed settings
    admin_email: str = "admin@alpaco.com"
    admin_password: str = "alpacothy500"


settings = Settings()
