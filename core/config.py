from pathlib import Path
from pydantic_settings import BaseSettings
from sqlalchemy import URL
project_path = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    model_config = {
        "env_file": [".env", "../.env"],
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }
    
    db_host: str = ""
    db_user: str = ""
    db_port: int = 3306
    db_name: str = "user"
    db_password: str = ""
    @property
    def DATABASE_URL(self) -> URL:
        return URL.create(
            drivername="mysql+aiomysql",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            query={"charset": "utf8mb4"}
        )
    
    secret_key: str = ""
    algorithm: str = ""
    access_token_expires_minutes : int = 60
        
    
settings = Settings()