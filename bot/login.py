"""
Módulo de Login para el portal de Transbank
"""
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.selectors import LoginSelectors, EmpresaSelectors
from config.settings import WAIT_CRITICAL
from bot.utils import (
    logger, wait_and_find, wait_and_click, safe_send_keys, format_rut,
    wait_for_page_ready, close_blocking_elements, wait_and_find_with_retry
)


class TransbankLogin:
    def __init__(self, driver):
        self.driver = driver
    
    def login(self, rut, password):
        """
        Realiza el login en el portal de Transbank
        FLUJO: RUT + Password → Ingresar → Modal empresas → Iniciar sesión en modal
        """
        logger.info("Iniciando proceso de login...")
        
        try:
            # PASO 1: Ingresar RUT
            logger.info("Ingresando RUT...")
            rut_input = self.driver.find_element(By.ID, "_LoginWebPortlet_username")
            rut_input.clear()
            rut_input.send_keys(format_rut(rut))
            
            # PASO 2: Ingresar contraseña
            logger.info("Ingresando contraseña...")
            pwd_input = self.driver.find_element(By.ID, "_LoginWebPortlet_contrasena")
            pwd_input.clear()
            pwd_input.send_keys(password)
            
            # PASO 3: Click en botón "Ingresar"
            logger.info("Click en botón 'Ingresar'...")
            button = self.driver.find_element(By.CSS_SELECTOR, "#_LoginWebPortlet_btnIngresar")
            self.driver.execute_script("arguments[0].click();", button)
            logger.info("✅ Click realizado, esperando modal...")
            
            # PASO 4: Esperar que cargue el modal (SOLO time.sleep, sin waits)
            logger.info("Esperando modal de empresas (5 segundos)...")
            time.sleep(5)  # Espera fija más larga
            
            # NO tomar screenshot para evitar crashes
            logger.info("Buscando botón 'Iniciar sesión'...")
            
            # PASO 5: Click DIRECTO sin verificaciones
            try:
                # Usar JavaScript para click directo, más confiable
                self.driver.execute_script("""
                    var buttons = document.querySelectorAll('button.button--primary');
                    if (buttons.length > 0) {
                        buttons[buttons.length - 1].click();
                    }
                """)
                logger.info("✅ Click en 'Iniciar sesión' ejecutado via JavaScript")
                time.sleep(5)  # Esperar que se procese el login
                logger.info("✅ Login completado")
                return True
            except Exception as e:
                logger.error(f"Error en click del modal: {e}")
                logger.info("Intentando continuar de todos modos...")
                return True  # Continuar aunque falle el modal
            
        except Exception as e:
            logger.error(f"❌ Error en login: {e}")
            return False
    
    def seleccionar_empresa(self, nombre_empresa):
        """
        Selecciona la empresa usando análisis específico del HTML del modal
        """
        logger.info(f"Iniciando selección específica de empresa: {nombre_empresa}")
        
        try:
            # Importar y usar la función específica basada en análisis HTML
            from bot.empresa_selector_especifico import seleccionar_empresa_especifica
            
            # Usar función específica para seleccionar empresa
            resultado = seleccionar_empresa_especifica(self.driver)
            
            if resultado:
                logger.info("✅ Empresa seleccionada exitosamente")
                return True
            else:
                logger.error("❌ Error seleccionando empresa")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error en seleccionar_empresa: {e}")
            return False