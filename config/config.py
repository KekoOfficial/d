import json
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TOKEN = os.getenv("TOKEN_DISCORD")
    DUENO_ID = int(os.getenv("DUENO_ID"))
    
    @staticmethod
    def cargar():
        with open("config/config.json", "r", encoding="utf-8") as f:
            return json.load(f)

def cargar_config():
    return Config.cargar()
