from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    APP_NAME:str
    APP_VERSION:str
    
    
    GOOGLE_API_KEY : str
    COLLECTION_NAME :str
    FILE_ALLOWED_EXTENSIONS: list
    FASTAPI_URL : str
    
    class Config:
        env_file = ".env"
        
def get_settings():
    return Settings()