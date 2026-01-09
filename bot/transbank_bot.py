"""
Clase principal del bot de Transbank
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from config.settings import (
    LOGIN_URL, 
    DOCUMENTOS_URL,
    HEADLESS, 
    DOWNLOAD_PATH,
    WAIT_MEDIUM
)
from config.selectors import ProductoValues
from bot.login import TransbankLogin
from bot.documentos import DocumentosElectronicos
from bot.utils import logger, take_screenshot


class TransbankBot:
    def __init__(self, headless=HEADLESS):
        """
        Inicializa el bot de Transbank
        
        Args:
            headless: Si True, ejecuta sin interfaz gráfica
        """
        self.driver = None
        self.headless = headless
        self.login_module = None
        self.documentos_module = None
    
    def iniciar_navegador(self):
        """
        Configura e inicia el navegador Chrome
        """
        logger.info("Iniciando navegador Chrome...")
        
        try:
            # Configurar opciones de Chrome
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument('--headless')
            
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            # Configurar descargas
            prefs = {
                'download.default_directory': DOWNLOAD_PATH,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True
            }
            chrome_options.add_experimental_option('prefs', prefs)
            
            # Iniciar el driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Maximizar ventana
            self.driver.maximize_window()
            
            # Inicializar módulos
            self.login_module = TransbankLogin(self.driver)
            self.documentos_module = DocumentosElectronicos(self.driver)
            
            logger.info("✅ Navegador iniciado correctamente")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error iniciando navegador: {e}")
            return False
    
    def cerrar_navegador(self):
        """
        Cierra el navegador
        """
        if self.driver:
            logger.info("Cerrando navegador...")
            self.driver.quit()
            logger.info("✅ Navegador cerrado")
    
    def ir_a_login(self):
        """
        Navega a la página de login
        """
        logger.info(f"Navegando a: {LOGIN_URL}")
        self.driver.get(LOGIN_URL)
        time.sleep(WAIT_MEDIUM)
    
    def ejecutar_descarga_completa(self, rut, password, empresa, dia=None, mes=None, year=None, producto=ProductoValues.TODOS, max_docs=10):
        """
        Ejecuta el proceso completo de descarga de documentos
        
        Args:
            rut: RUT del usuario
            password: Contraseña
            empresa: Nombre de la empresa
            dia: Día del mes (opcional)
            mes: Mes (1-12)
            year: Año
            producto: Tipo de producto (usar ProductoValues)
            max_docs: Máximo de documentos a descargar (hasta 10)
        
        Returns:
            bool: True si todo fue exitoso
        """
        logger.info("="*60)
        logger.info("INICIANDO PROCESO DE DESCARGA DE DOCUMENTOS")
        logger.info("="*60)
        
        try:
            # 1. Iniciar navegador
            if not self.iniciar_navegador():
                return False
            
            # 2. Ir a login
            self.ir_a_login()
            
            # 3. Login
            if not self.login_module.login(rut, password):
                take_screenshot(self.driver, 'error_login.png')
                return False
            
            # 4. Seleccionar empresa
            if not self.login_module.seleccionar_empresa(empresa):
                take_screenshot(self.driver, 'error_empresa.png')
                return False
            
            # 5. Navegar a Documentos Electrónicos
            if not self.documentos_module.navegar_a_documentos():
                take_screenshot(self.driver, 'error_navegacion.png')
                return False
            
            # 6. Cambiar al iframe
            if not self.documentos_module.cambiar_a_iframe():
                take_screenshot(self.driver, 'error_iframe.png')
                return False
            
            # 7. Buscar documentos
            if not self.documentos_module.buscar_documentos(dia, mes, year, producto):
                take_screenshot(self.driver, 'sin_resultados.png')
                logger.warning("⚠️ No se encontraron documentos")
                return False
            
            # 8. Seleccionar documentos
            docs_seleccionados = self.documentos_module.seleccionar_documentos(max_docs)
            if docs_seleccionados == 0:
                logger.warning("⚠️ No se pudieron seleccionar documentos")
                return False
            
            # 9. Descargar
            if not self.documentos_module.descargar_masiva():
                take_screenshot(self.driver, 'error_descarga.png')
                return False
            
            logger.info("="*60)
            logger.info("✅ PROCESO COMPLETADO EXITOSAMENTE")
            logger.info("="*60)
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en proceso completo: {e}")
            take_screenshot(self.driver, 'error_general.png')
            return False
        
        finally:
            # Esperar un poco antes de cerrar
            time.sleep(3)
            self.cerrar_navegador()