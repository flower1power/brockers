from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    base_url_api: str = Field(..., description="REST API base URL for user registration/activation")
    kafka_producer: str = Field(..., description="Kafka broker address")
    topic_register_events: str = Field(default="register-events", description="Kafka topic for registration events")
    topic_register_events_errors: str = Field(
        default="register-events-errors", description="Kafka topic for registration error events"
    )
    rmq_publisher_url: str = Field(..., description="Rmq publisher url")
    dm_mail_sending_exchange: str = Field(default="dm.mail.sending", description="Rmq mail sending exchange")


settings = Settings()
