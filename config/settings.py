"""
Configuración general del bot de Transbank
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Credenciales
TRANSBANK_RUT = os.getenv('TRANSBANK_RUT')
TRANSBANK_PASSWORD = os.getenv('TRANSBANK_PASSWORD')
TRANSBANK_EMPRESA = os.getenv('TRANSBANK_EMPRESA', 'ZD PACK DISTRIBUCION Y LOGISTICA SPA')

# URLs
BASE_URL = 'https://privado.transbank.cl'
LOGIN_URL = f'{BASE_URL}/group/portal-3.0/login'
DOCUMENTOS_URL = f'{BASE_URL}/group/portal-3.0/documentos-electronicos-28451'

# Configuración del navegador
HEADLESS = False  # Cambiar a True para ejecución sin interfaz gráfica
DOWNLOAD_PATH = os.path.join(os.getcwd(), 'downloads')

# Tiempos de espera (segundos)
WAIT_SHORT = 5
WAIT_MEDIUM = 10
WAIT_LONG = 20
WAIT_CRITICAL = 30  # Para elementos críticos como login
WAIT_DOWNLOAD = 30

# Crear carpeta de descargas si no existe
os.makedirs(DOWNLOAD_PATH, exist_ok=True)