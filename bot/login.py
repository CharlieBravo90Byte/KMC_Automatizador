"""
Módulo de Login para el portal de Transbank
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.selectors import LoginSelectors, EmpresaSelectors
from bot.utils import logger, wait_and_find, wait_and_click, safe_send_keys, format_rut


class TransbankLogin:
    def __init__(self, driver):
        self.driver = driver
    
    def login(self, rut, password):
        """
        Realiza el login en el portal de Transbank
        """
        logger.info("Iniciando proceso de login...")
        
        try:
            # Encontrar campo RUT
            rut_input = wait_and_find(self.driver, By.ID, LoginSelectors.RUT_INPUT)
            logger.info("Campo RUT encontrado")
            
            # Ingresar RUT
            formatted_rut = format_rut(rut)
            safe_send_keys(rut_input, formatted_rut)
            logger.info(f"RUT ingresado: {formatted_rut}")
            
            # Encontrar campo contraseña
            password_input = wait_and_find(self.driver, By.ID, LoginSelectors.PASSWORD_INPUT)
            logger.info("Campo contraseña encontrado")
            
            # Ingresar contraseña
            safe_send_keys(password_input, password)
            logger.info("Contraseña ingresada")
            
            # Click en botón login
            wait_and_click(self.driver, By.CSS_SELECTOR, LoginSelectors.LOGIN_BUTTON)
            logger.info("Click en botón 'Iniciar sesión'")
            
            # Esperar a que cargue la siguiente página
            time.sleep(3)
            
            # Verificar si hay error
            try:
                error = self.driver.find_element(By.CSS_SELECTOR, LoginSelectors.ERROR_MESSAGE)
                if error.is_displayed():
                    logger.error(f"Error en login: {error.text}")
                    return False
            except:
                pass
            
            logger.info("✅ Login exitoso")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en login: {e}")
            return False
    
    def seleccionar_empresa(self, nombre_empresa):
        """
        Selecciona la empresa del dropdown modal
        """
        logger.info(f"Buscando empresa: {nombre_empresa}")
        
        try:
            # Esperar a que aparezca el modal
            wait_and_find(self.driver, By.CSS_SELECTOR, EmpresaSelectors.MODAL, timeout=10)
            logger.info("Modal de selección de empresa detectado")
            
            # Esperar un poco para que cargue la lista
            time.sleep(2)
            
            # Encontrar el <ul> de empresas
            ul_empresas = wait_and_find(self.driver, By.ID, EmpresaSelectors.DROPDOWN_UL)
            logger.info("Lista de empresas encontrada")
            
            # Obtener todos los <li>
            empresas = ul_empresas.find_elements(By.TAG_NAME, EmpresaSelectors.EMPRESA_ITEM)
            logger.info(f"Total de empresas encontradas: {len(empresas)}")
            
            # Buscar la empresa deseada
            empresa_encontrada = False
            for empresa in empresas:
                texto_empresa = empresa.text.strip()
                logger.info(f"Evaluando empresa: {texto_empresa}")
                
                if nombre_empresa.upper() in texto_empresa.upper():
                    logger.info(f"✅ Empresa encontrada: {texto_empresa}")
                    empresa.click()
                    empresa_encontrada = True
                    time.sleep(1)
                    break
            
            if not empresa_encontrada:
                logger.error(f"❌ Empresa '{nombre_empresa}' no encontrada en la lista")
                return False
            
            # Click en botón "Iniciar Sesión"
            wait_and_click(self.driver, By.CSS_SELECTOR, EmpresaSelectors.INICIAR_SESION_BUTTON)
            logger.info("Click en 'Iniciar Sesión'")
            
            # Esperar a que cargue el dashboard
            time.sleep(5)
            
            logger.info("✅ Empresa seleccionada exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error seleccionando empresa: {e}")
            return False