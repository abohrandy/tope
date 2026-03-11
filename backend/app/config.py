from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./news_monitor.db"
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SENDER_EMAIL: str = ""
    DIGEST_HOUR: int = 7
    DIGEST_MINUTE: int = 0

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def fix_postgres_scheme(cls, v: str) -> str:
        """SQLAlchemy requires 'postgresql://' instead of 'postgres://'."""
        if not v:
            return v
            
        # If it starts with postgres://, just fix the scheme
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
            
        # If it lacks a scheme (no '://'), try to construct it if it looks like a host:port
        if "://" not in v:
            import os
            user = os.getenv("PGUSER") or os.getenv("POSTGRES_USER")
            password = os.getenv("PGPASSWORD") or os.getenv("POSTGRES_PASSWORD")
            database = os.getenv("PGDATABASE") or os.getenv("POSTGRES_DB") or "railway"
            
            # If we have basic components, construct the URL
            if user and password:
                return f"postgresql://{user}:{password}@{v}/{database}"
            
            # If it's just a host and we don't have enough info, 
            # at least prepend the scheme to avoid the parse error, 
            # though it might fail later on authentication.
            return f"postgresql://{v}"
            
        return v

    class Config:
        env_file = ".env"


settings = Settings()
