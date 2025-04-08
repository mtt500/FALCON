from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # OpenAI 配置
    OPENAI_API_KEY: str = "k-42kUEMoma40GUNhl595bE5D53e994eC59a7a469534564f11"
    OPENAI_API_BASE: str = "https://api.gptapi.us/v1"
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # 项目路径配置
    BASE_DIR: Path = Path(__file__).parent.parent
    CACHE_DIR: Path = BASE_DIR / "cache"
    LOG_DIR: Path = BASE_DIR / "logs"
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"