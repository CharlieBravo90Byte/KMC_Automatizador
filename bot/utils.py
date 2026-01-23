"""
Funciones auxiliares para el bot
"""
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def wait_and_find(driver, by, value, timeout=10):
    """
    Espera a que un elemento esté presente y lo retorna
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        logger.error(f"Timeout esperando elemento: {value}")
        raise

def wait_and_click(driver, by, value, timeout=10):
    """
    Espera a que un elemento sea clickeable y hace click
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()
        return element
    except TimeoutException:
        logger.error(f"Timeout esperando elemento clickeable: {value}")
        raise

def safe_send_keys(element, text):
    """
    Envía texto a un elemento de forma segura
    """
    try:
        element.clear()
        element.send_keys(text)
        return True
    except Exception as e:
        logger.error(f"Error enviando texto: {e}")
        return False

def wait_for_element_invisible(driver, by, value, timeout=10):
    """
    Espera a que un elemento se vuelva invisible
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((by, value))
        )
        return True
    except TimeoutException:
        logger.warning(f"Elemento aún visible después de {timeout}s: {value}")
        return False

def take_screenshot(driver, filename):
    """
    Toma una captura de pantalla
    """
    try:
        driver.save_screenshot(filename)
        logger.info(f"Captura guardada: {filename}")
        return True
    except Exception as e:
        logger.error(f"Error tomando captura: {e}")
        return False

def format_rut(rut):
    """
    Formatea el RUT chileno (12345678-9)
    """
    return rut.strip().replace('.', '').upper()

def close_blocking_elements(driver):
    """
    Cierra elementos que pueden bloquear la interfaz (popups, modales, banners)
    """
    blocking_selectors = [
        '.modal .close',
        '.modal .btn-close', 
        '[aria-label="close"]',
        '[aria-label="Close"]',
        '.popup-close',
        '[class*="cookie"] button',
        '.alert .close'
    ]
    
    for selector in blocking_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                if element.is_displayed() and element.is_enabled():
                    element.click()
                    logger.info(f"Cerrado elemento de bloqueo: {selector}")
                    time.sleep(1)
        except Exception:
            continue

def wait_for_page_ready(driver, timeout=20):
    """
    Espera a que la página esté completamente cargada
    """
    try:
        # Esperar a que se complete la carga de la página
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        
        # Espera adicional para JavaScript dinámico
        time.sleep(2)
        
        # Cerrar elementos de bloqueo
        close_blocking_elements(driver)
        
        logger.info("Página completamente cargada")
        return True
    except TimeoutException:
        logger.warning(f"Timeout esperando carga de página ({timeout}s)")
        return False

def wait_and_find_with_retry(driver, by, value, timeout=15, max_retries=3):
    """
    Espera a que un elemento esté presente con reintentos automáticos
    """
    for attempt in range(max_retries):
        try:
            logger.info(f"Intento {attempt + 1}/{max_retries} buscando elemento: {value}")
            
            # Intentar encontrar el elemento
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            logger.info(f"Elemento encontrado en intento {attempt + 1}: {value}")
            return element
            
        except TimeoutException:
            logger.warning(f"Timeout en intento {attempt + 1} para elemento: {value}")
            
            if attempt < max_retries - 1:
                # Intentar cerrar elementos de bloqueo antes del siguiente intento
                close_blocking_elements(driver)
                
                # Refrescar la página si es el último intento antes del final
                if attempt == max_retries - 2:
                    logger.info("Refrescando página para último intento...")
                    driver.refresh()
                    wait_for_page_ready(driver)
                    
                time.sleep(2)
            else:
                logger.error(f"Elemento no encontrado después de {max_retries} intentos: {value}")
                raise

def wait_for_download(download_path, timeout=30):
    """
    Espera a que termine una descarga
    """
    logger.info("Esperando descarga...")
    time.sleep(2)
    
    seconds = 0
    while seconds < timeout:
        # Buscar archivos temporales de descarga (.crdownload, .tmp)
        downloading = False
        try:
            import os
            for filename in os.listdir(download_path):
                if filename.endswith(('.crdownload', '.tmp')):
                    downloading = True
                    break
        except Exception:
            pass
        
        if not downloading:
            logger.info("Descarga completada")
            return True
        
        time.sleep(1)
        seconds += 1
    
    logger.warning(f"Timeout esperando descarga ({timeout}s)")
    return False