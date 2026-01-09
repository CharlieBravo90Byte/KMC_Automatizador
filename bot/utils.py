"""
Funciones auxiliares para el bot
"""
import time
import logging
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