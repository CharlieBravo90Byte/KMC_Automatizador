"""
Script principal usando Playwright (solución moderna y estable)
"""
import time
from bot.transbank_playwright import TransbankPlaywrightBot
from bot.utils import logger
from datetime import datetime, timedelta


def main():
    logger.info("=" * 60)
    logger.info("🚀 TRANSBANK BOT - PLAYWRIGHT (CHROMIUM EMBEBIDO)")
    logger.info("=" * 60)
    
    bot = TransbankPlaywrightBot(headless=True)  # Modo invisible - no interfiere
    
    try:
        # PASO 1: Login
        logger.info("\n📍 FASE 1: LOGIN")
        if not bot.login():
            logger.error("❌ Login falló")
            return
        
        logger.info("\n✅ Login completado (navegador invisible - no interfiere con tu trabajo)")
        logger.info("Esperando 5 segundos...")
        time.sleep(5)
        
        # PASO 2: Navegar a documentos
        logger.info("\n📍 FASE 2: NAVEGACIÓN A DOCUMENTOS")
        if not bot.navegar_a_documentos():
            logger.error("❌ No se pudo navegar a documentos")
            return
        
        logger.info("\n⏸️ PAUSA: Observa el iframe de documentos")
        logger.info("Esperando 5 segundos...")
        time.sleep(5)
        
        # PASO 3: Buscar documentos
        logger.info("\n📍 FASE 3: BÚSQUEDA DE DOCUMENTOS")
        fecha_hasta = datetime.now()
        fecha_desde = fecha_hasta - timedelta(days=30)
        
        if bot.buscar_documentos(
            fecha_desde.strftime('%d/%m/%Y'),
            fecha_hasta.strftime('%d/%m/%Y')
        ):
            logger.info("\n⏸️ PAUSA: Observa los resultados")
            logger.info("Esperando 5 segundos...")
            time.sleep(5)
            
            # PASO 4: Seleccionar documentos
            logger.info("\n📍 FASE 4: SELECCIÓN DE DOCUMENTOS")
            bot.seleccionar_documentos()
            
            logger.info("\n⏸️ PAUSA: Verifica la selección")
            logger.info("Esperando 5 segundos...")
            time.sleep(5)
            
            # PASO 5: Descargar
            logger.info("\n📍 FASE 5: DESCARGA MASIVA")
            bot.descargar_masiva()
        
        logger.info("\n✅ PROCESO COMPLETADO")
        logger.info("Esperando 10 segundos antes de cerrar...")
        time.sleep(10)
        
    except KeyboardInterrupt:
        logger.info("\n⚠️ Proceso interrumpido por el usuario")
    except Exception as e:
        logger.error(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        logger.info("Esperando 10 segundos antes de cerrar...")
        time.sleep(10)
    finally:
        bot.close()


if __name__ == '__main__':
    main()
