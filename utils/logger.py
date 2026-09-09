from datetime import datetime

class Logger:
    @staticmethod
    def info(texto):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ℹ️ {texto}")
    
    @staticmethod
    def exito(texto):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ {texto}")
    
    @staticmethod
    def error(texto):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ {texto}")
