from pydantic_settings import BaseSettings, SettingsConfigDict

class DataBaseSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    DB_HOST_TEST: str
    DB_PORT_TEST: str
    DB_NAME_TEST: str
    DB_USER_TEST: str
    DB_PASS_TEST: str

    @property
    def DATABASE_URL_asyncpg(self):
        print(f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def DATABASE_URL_alembic(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@db:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def DATABASE_URL_TEST(self):
        return f"postgresql+asyncpg://{self.DB_USER_TEST}:{self.DB_PASS_TEST}@{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.DB_NAME_TEST}"
    
    model_config = SettingsConfigDict(env_file=".env")

db_settings = DataBaseSettings() # type: ignore