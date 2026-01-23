"""
Bot Playwright SIMPLIFICADO - Solo para probar el flujo completo
"""
from playwright.sync_api import sync_playwright
import time
from datetime import datetime
from config.settings import TRANSBANK_RUT, TRANSBANK_PASSWORD, LOGIN_URL
from bot.utils import logger, format_rut

def main():
    logger.info("🚀 TRANSBANK BOT - PLAYWRIGHT SIMPLIFICADO (HEADLESS)")
    
    with sync_playwright() as p:
        logger.info("Iniciando Chromium VISIBLE (para debug)...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # LOGIN
            logger.info(f"📍 Navegando a {LOGIN_URL}")
            page.goto(LOGIN_URL, timeout=60000)
            logger.info("✅ Página cargada")
            
            # RUT
            logger.info("Ingresando RUT...")
            page.fill('#_LoginWebPortlet_username', format_rut(TRANSBANK_RUT))
            
            # Contraseña
            logger.info("Ingresando contraseña...")
            page.fill('#_LoginWebPortlet_contrasena', TRANSBANK_PASSWORD)
            
            # Click ingresar
            logger.info("Click en 'Ingresar'...")
            page.click('#_LoginWebPortlet_btnIngresar', force=True)  # Force porque el botón puede estar oculto por CSS
            
            # Esperar respuesta
            logger.info("Esperando respuesta...")
            time.sleep(5)
            
            # Verificar modal
            logger.info("Buscando modal...")
            modal_count = page.locator('#_LoginWebPortlet_modal_org_select').count()
            logger.info(f"Modales encontrados: {modal_count}")
            
            if modal_count > 0:
                logger.info("✅ Modal detectado - tomando screenshot...")
                page.screenshot(path=f'modal_simple_{datetime.now().strftime("%H%M%S")}.png')
                
                # Click en "Iniciar sesión"
                logger.info("Click en 'Iniciar sesión' del modal...")
                page.click('#_LoginWebPortlet_modal_org_select button.button--primary')
                time.sleep(5)
            
            # URL final
            logger.info(f"📍 URL final: {page.url}")
            
            # Dashboard
            if '/portal-3.0' in page.url and '/login' not in page.url:
                logger.info("✅ LOGIN EXITOSO")
                page.screenshot(path=f'dashboard_simple_{datetime.now().strftime("%H%M%S")}.png')
            else:
                logger.error("❌ Login falló")
            
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()
            logger.info("✅ Navegador cerrado")

if __name__ == '__main__':
    main()
