"""
Clase principal del bot de Transbank
"""
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import geckodriver_autoinstaller

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
        Configura e inicia el navegador Firefox
        """
        logger.info("Iniciando navegador Firefox...")
        
        try:
            # Instalar geckodriver automáticamente
            logger.info("Verificando GeckoDriver...")
            geckodriver_autoinstaller.install()
            
            # Configuración de Firefox
            firefox_options = Options()
            
            if self.headless:
                firefox_options.add_argument('--headless')
                logger.info("Modo headless activado")
            
            # Configurar descargas
            firefox_options.set_preference('browser.download.folderList', 2)
            firefox_options.set_preference('browser.download.dir', DOWNLOAD_PATH)
            firefox_options.set_preference('browser.download.useDownloadDir', True)
            firefox_options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip,application/pdf,application/excel')
            
            # Deshabilitar notificaciones
            firefox_options.set_preference('dom.webnotifications.enabled', False)
            
            # Iniciar Firefox con timeouts extendidos
            logger.info("Lanzando Firefox...")
            
            # Service con timeout extendido
            service = Service(log_path='geckodriver.log')
            
            self.driver = webdriver.Firefox(options=firefox_options, service=service)
            
            # Configurar timeouts MUY largos para evitar desconexiones
            self.driver.set_page_load_timeout(120)  # 2 minutos
            self.driver.implicitly_wait(30)  # 30 segundos
            
            self.driver.maximize_window()
            logger.info("Timeouts configurados: page_load=120s, implicit_wait=30s")
            
            # Inicializar módulos
            self.login_module = TransbankLogin(self.driver)
            self.documentos_module = DocumentosElectronicos(self.driver)
            
            logger.info("✅ Navegador Firefox iniciado correctamente")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error iniciando navegador: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def cerrar_navegador(self):
        """
        Cierra el navegador de forma segura
        """
        if self.driver:
            logger.info("Cerrando navegador...")
            try:
                self.driver.quit()
                logger.info("✅ Navegador cerrado")
            except Exception as e:
                logger.warning(f"⚠️ Error al cerrar navegador (probablemente ya estaba cerrado): {e}")
                # Ignorar errores de cierre porque ChromeDriver a veces crashea
    
    def ir_a_login(self):
        """
        Navega a la página de login
        """
        from bot.utils import wait_for_page_ready
        
        logger.info(f"Navegando a: {LOGIN_URL}")
        self.driver.get(LOGIN_URL)
        
        # Esperar a que la página cargue completamente
        wait_for_page_ready(self.driver, 30)
        logger.info("Página de login cargada completamente")
    
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
            
            # 3. Login (entrada automática con primera empresa)
            if not self.login_module.login(rut, password):
                take_screenshot(self.driver, 'error_login.png')
                return False
            
            # ============================================
            # LOGIN COMPLETADO - DETENIENDO PARA PRUEBAS
            # ============================================
            logger.info("✅ Login completado exitosamente")
            logger.info("=" * 60)
            
            # PAUSA PARA OBSERVAR DASHBOARD Y QUE CARGUE COMPLETAMENTE
            logger.info("⏸️  PAUSA: Observa el navegador - deberías ver el DASHBOARD")
            logger.info("Esperando que el dashboard cargue completamente...")
            time.sleep(8)  # Pausa más larga para que cargue todo
            
            # SALTAR cambio de empresa (usar la que viene por defecto del modal)
            logger.info("📌 Usando empresa por defecto del login")
            
            # 5. Navegar a Documentos Electrónicos
            logger.info("=" * 60)
            logger.info("NAVEGANDO A DOCUMENTOS ELECTRÓNICOS")
            logger.info("=" * 60)
            if not self.documentos_module.navegar_a_documentos():
                take_screenshot(self.driver, 'error_navegacion.png')
                logger.error("❌ Error al navegar a documentos")
                return False
            
            logger.info("✅ Navegación a documentos exitosa")
            
            # 6. Cambiar al iframe
            logger.info("Cambiando al iframe de documentos...")
            if not self.documentos_module.cambiar_a_iframe():
                take_screenshot(self.driver, 'error_iframe.png')
                logger.error("❌ Error al cambiar al iframe")
                return False
            
            logger.info("✅ Iframe cargado correctamente")
            
            # PAUSA PARA OBSERVAR
            logger.info("=" * 60)
            logger.info("⏸️  PAUSA: Observa el navegador - deberías ver el formulario")
            logger.info("=" * 60)
            time.sleep(5)  # Pausa para que veas el formulario
            
            # 7. Buscar documentos
            logger.info("=" * 60)
            logger.info(f"BUSCANDO DOCUMENTOS: {dia}/{mes}/{year} - Producto: {producto}")
            logger.info("=" * 60)
            if not self.documentos_module.buscar_documentos(dia, mes, year, producto):
                take_screenshot(self.driver, 'sin_resultados.png')
                logger.warning("⚠️ No se encontraron documentos")
                return False
            
            logger.info("✅ Búsqueda completada")
            
            # 8. Seleccionar documentos
            logger.info(f"Seleccionando hasta {max_docs} documentos...")
            docs_seleccionados = self.documentos_module.seleccionar_documentos(max_docs)
            if docs_seleccionados == 0:
                logger.warning("⚠️ No se pudieron seleccionar documentos")
                return False
            
            logger.info(f"✅ {docs_seleccionados} documentos seleccionados")
            
            # 9. Descargar
            logger.info("=" * 60)
            logger.info("INICIANDO DESCARGA MASIVA")
            logger.info("=" * 60)
            if not self.documentos_module.descargar_masiva():
                take_screenshot(self.driver, 'error_descarga.png')
                logger.error("❌ Error en la descarga")
                return False
            
            logger.info("✅ Descarga completada")
            
            logger.info("="*60)
            logger.info("✅ PROCESO COMPLETADO EXITOSAMENTE")
            logger.info("="*60)
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en proceso completo: {e}")
            take_screenshot(self.driver, 'error_general.png')
            return False
        
        finally:
            # Espera mínima antes de cerrar
            time.sleep(1)
            self.cerrar_navegador()