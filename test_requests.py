"""
Script de prueba para el bot basado en Requests (sin navegador)
"""
from bot.transbank_requests import TransbankRequestsBot
from bot.utils import logger
from datetime import datetime, timedelta


def main():
    logger.info("=" * 60)
    logger.info("🚀 TRANSBANK BOT - MODO REQUESTS (SIN NAVEGADOR)")
    logger.info("=" * 60)
    
    bot = TransbankRequestsBot()
    
    try:
        # PASO 1: Login
        logger.info("\n📍 FASE 1: LOGIN")
        if not bot.login():
            logger.error("❌ Login falló")
            return
        
        logger.info("\n⏸️ Login completado. Presiona ENTER para continuar...")
        input()
        
        # PASO 2: Navegar a documentos
        logger.info("\n📍 FASE 2: NAVEGACIÓN A DOCUMENTOS")
        if not bot.navegar_a_documentos():
            logger.error("❌ No se pudo navegar a documentos")
            return
        
        logger.info("\n⏸️ Navegación completada. Presiona ENTER para continuar...")
        input()
        
        # PASO 3: Buscar documentos
        logger.info("\n📍 FASE 3: BÚSQUEDA DE DOCUMENTOS")
        fecha_hasta = datetime.now()
        fecha_desde = fecha_hasta - timedelta(days=30)
        
        bot.buscar_documentos(
            fecha_desde.strftime('%d/%m/%Y'),
            fecha_hasta.strftime('%d/%m/%Y')
        )
        
        logger.info("\n✅ PROCESO COMPLETADO")
        logger.info("📁 Revisa los archivos debug_*.html generados para análisis")
        
    except KeyboardInterrupt:
        logger.info("\n⚠️ Proceso interrumpido por el usuario")
    except Exception as e:
        logger.error(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        bot.close()


if __name__ == '__main__':
    main()
