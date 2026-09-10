from datetime import datetime

class Logger:
    """Sistema de registro simple para el bot KR EMPIRE"""

    @staticmethod
    def info(mensaje):
        hora = datetime.now().strftime("%H:%M:%S")
        print(f"{hora}  INFO     {mensaje}")

    @staticmethod
    def exito(mensaje):
        hora = datetime.now().strftime("%H:%M:%S")
        print(f"{hora}  ✅ EXITO   {mensaje}")

    @staticmethod
    def error(mensaje):
        hora = datetime.now().strftime("%H:%M:%S")
        print(f"{hora}  ❌ ERROR   {mensaje}")
