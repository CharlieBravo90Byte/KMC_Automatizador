"""
Módulo para cambiar de empresa desde el dashboard
Usa el selector dropdown visible en la esquina superior del portal
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.selectors import DashboardSelectors
from bot.utils import logger


def cambiar_empresa_dashboard(driver, nombre_empresa_objetivo):
    """
    Cambia de empresa usando el selector del dashboard (después del login)
    VERSIÓN SIMPLIFICADA SIN SCREENSHOTS INTERMEDIOS
    """
    try:
        logger.info(f"Cambiando a empresa: {nombre_empresa_objetivo}")
        
        # PASO 1: Buscar selector de empresa (intentar varios)
        logger.info("Buscando selector de empresa...")
        wait = WebDriverWait(driver, 10)
        
        selectores_candidatos = [
            (By.CSS_SELECTOR, "button.org-tbk"),
            (By.CSS_SELECTOR, ".change_sessions button"),
            (By.CSS_SELECTOR, "button[data-toggle='dropdown']"),
            (By.XPATH, "//button[contains(@class, 'org-')]"),
            (By.XPATH, "//span[@nombredisplay]//parent::button"),
        ]
        
        boton_empresa = None
        for by, selector in selectores_candidatos:
            try:
                boton_empresa = wait.until(EC.element_to_be_clickable((by, selector)))
                logger.info(f"✅ Selector encontrado: {selector}")
                break
            except:
                continue
        
        if not boton_empresa:
            logger.error("❌ No se encontró el selector de empresa")
            return False
        
        # PASO 2: Click en el selector
        logger.info("Abriendo dropdown...")
        driver.execute_script("arguments[0].click();", boton_empresa)
        time.sleep(2)
        
        # PASO 3: Buscar empresas en la lista
        logger.info("Buscando empresas en la lista...")
        selectores_items = [
            "li[data-org-rut]",
            "ul.list-org li",
            ".list-org li",
            "li[onclick*='organization']",
            "ul li a",
        ]
        
        empresas_encontradas = []
        for selector in selectores_items:
            try:
                items = driver.find_elements(By.CSS_SELECTOR, selector)
                if items:
                    empresas_encontradas = items
                    logger.info(f"✅ {len(items)} items encontrados")
                    break
            except:
                continue
        
        if not empresas_encontradas:
            logger.error("❌ No se encontraron empresas en dropdown")
            return False
        
        # PASO 4: Seleccionar empresa objetivo
        empresa_target = None
        for item in empresas_encontradas:
            try:
                texto = item.text.strip()
                if nombre_empresa_objetivo.upper() in texto.upper():
                    empresa_target = item
                    logger.info(f"✅ Empresa encontrada: {texto}")
                    break
            except:
                pass
        
        if not empresa_target:
            logger.error(f"❌ No se encontró: {nombre_empresa_objetivo}")
            return False
        
        # PASO 5: Click en empresa
        logger.info("Seleccionando empresa...")
        driver.execute_script("arguments[0].click();", empresa_target)
        time.sleep(5)
        
        logger.info("✅ Cambio de empresa completado")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error cambiando empresa: {e}")
        return False
