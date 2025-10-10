import os
from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseModel):
    DATA: str = os.getenv("DATA", "./data")
    # gerar tokens JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "changeme")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")

settings = Settings()
