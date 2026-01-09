"""
Script principal para ejecutar el bot de Transbank
"""
import sys
from config.settings import TRANSBANK_RUT, TRANSBANK_PASSWORD, TRANSBANK_EMPRESA
from config.selectors import ProductoValues
from bot.transbank_bot import TransbankBot
from bot.utils import logger


def main():
    """
    Función principal
    """
    # Verificar que las credenciales estén configuradas
    if not TRANSBANK_RUT or not TRANSBANK_PASSWORD:
        logger.error("❌ ERROR: Credenciales no configuradas")
        logger.error("Por favor, edita el archivo .env con tus credenciales")
        sys.exit(1)
    
    logger.info("Iniciando bot de Transbank...")
    logger.info(f"RUT: {TRANSBANK_RUT}")
    logger.info(f"Empresa: {TRANSBANK_EMPRESA}")
    
    # Crear instancia del bot
    bot = TransbankBot(headless=False)  # Cambiar a True para modo sin interfaz
    
    # Configurar parámetros de búsqueda
    # Ejemplo: buscar documentos de enero 2026
    dia = None  # None = todo el mes, o un número 1-31
    mes = 1     # 1 = Enero
    year = 2026
    producto = ProductoValues.TODOS  # Todos los productos
    max_docs = 10  # Máximo 10 documentos
    
    # Ejecutar proceso completo
    exito = bot.ejecutar_descarga_completa(
        rut=TRANSBANK_RUT,
        password=TRANSBANK_PASSWORD,
        empresa=TRANSBANK_EMPRESA,
        dia=dia,
        mes=mes,
        year=year,
        producto=producto,
        max_docs=max_docs
    )
    
    if exito:
        logger.info("✅ Bot ejecutado exitosamente")
        logger.info(f"📁 Revisa la carpeta 'downloads' para ver los archivos descargados")
        sys.exit(0)
    else:
        logger.error("❌ El bot falló. Revisa los logs y las capturas de pantalla.")
        sys.exit(1)


if __name__ == '__main__':
    main()