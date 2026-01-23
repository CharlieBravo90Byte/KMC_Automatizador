"""
Bot de Transbank usando Playwright (solución moderna y estable)
Sin problemas de ChromeDriver - usa Chromium embebido
"""
import time
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from config.settings import (
    TRANSBANK_RUT, TRANSBANK_PASSWORD, LOGIN_URL, DOCUMENTOS_URL, HEADLESS
)
from bot.utils import logger, format_rut


class TransbankPlaywrightBot:
    def __init__(self, headless=None):
        self.headless = headless if headless is not None else HEADLESS
        self.playwright = None
        self.browser = None
        self.page = None
        self.logged_in = False
        
    def iniciar_navegador(self):
        """Inicia el navegador Playwright"""
        logger.info(f"🌐 Iniciando Chromium (headless={self.headless})...")
        
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        )
        
        # Crear contexto con viewport y user agent
        context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        )
        
        self.page = context.new_page()
        logger.info("✅ Navegador iniciado")
        
    def login(self, rut=None, password=None):
        """
        Realiza el login en el portal de Transbank
        FLUJO: RUT + Password → Ingresar → Modal empresas → Iniciar sesión en modal
        """
        if not self.page:
            self.iniciar_navegador()
            
        rut = rut or TRANSBANK_RUT
        password = password or TRANSBANK_PASSWORD
        
        logger.info("Iniciando proceso de login...")
        
        try:
            # Navegar a la página de login
            logger.info(f"📍 Navegando a {LOGIN_URL}")
            self.page.goto(LOGIN_URL, wait_until='domcontentloaded', timeout=60000)
            logger.info("✅ Página cargada")
            
            # PASO 1: Ingresar RUT
            logger.info("Ingresando RUT...")
            rut_input = self.page.locator('#_LoginWebPortlet_username')
            rut_input.wait_for(state='visible', timeout=15000)
            rut_input.fill(format_rut(rut))
            
            # PASO 2: Ingresar contraseña
            logger.info("Ingresando contraseña...")
            pwd_input = self.page.locator('#_LoginWebPortlet_contrasena')
            pwd_input.wait_for(state='visible', timeout=15000)
            pwd_input.fill(password)
            
            # PASO 3: Click en botón "Ingresar"
            logger.info("Click en botón 'Ingresar'...")
            
            # Esperar a que el botón sea visible y hacer scroll
            btn = self.page.locator('#_LoginWebPortlet_btnIngresar')
            btn.scroll_into_view_if_needed()
            btn.wait_for(state='visible', timeout=15000)
            btn.click()
            
            # PASO 4: Esperar modal de empresas
            logger.info("Esperando modal de empresas...")
            try:
                self.page.wait_for_selector(
                    '#_LoginWebPortlet_modal_org_select',
                    state='visible',
                    timeout=10000
                )
                logger.info("✅ Modal de empresas detectado")
                
                # Captura de pantalla del modal
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                screenshot_path = f'estado_modal_playwright_{timestamp}.png'
                self.page.screenshot(path=screenshot_path)
                logger.info(f"📸 Screenshot guardado: {screenshot_path}")
                
            except PlaywrightTimeout:
                logger.warning("⚠️ Modal no apareció en 10 segundos")
                return False
            
            # PASO 5: Click en botón "Iniciar sesión" del modal
            logger.info("Click en 'Iniciar sesión' del modal...")
            
            # Buscar el botón dentro del modal
            modal_button = self.page.locator(
                '#_LoginWebPortlet_modal_org_select button[type="submit"].button--primary'
            )
            
            if modal_button.count() > 0:
                modal_button.click()
                logger.info("✅ Click en 'Iniciar sesión' realizado")
            else:
                logger.error("❌ No se encontró el botón 'Iniciar sesión' en el modal")
                return False
            
            # PASO 6: Esperar que cargue el dashboard
            logger.info("Esperando carga del dashboard...")
            time.sleep(5)
            
            # Verificar que estamos en el portal (no en /login)
            current_url = self.page.url
            logger.info(f"📍 URL actual: {current_url}")
            
            if '/login' not in current_url and '/portal-3.0' in current_url:
                logger.info("✅ Login completado exitosamente")
                self.logged_in = True
                
                # Screenshot del dashboard
                screenshot_path = f'dashboard_playwright_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
                self.page.screenshot(path=screenshot_path)
                logger.info(f"📸 Dashboard capturado: {screenshot_path}")
                
                return True
            else:
                logger.error("❌ Login falló - No se redirigió al portal")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error en login: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def navegar_a_documentos(self):
        """Navega a la sección de Documentos Electrónicos"""
        if not self.logged_in:
            logger.error("❌ Debes hacer login primero")
            return False
        
        logger.info("📄 Navegando a Documentos Electrónicos...")
        
        try:
            # Navegar directamente a la URL
            self.page.goto(DOCUMENTOS_URL, wait_until='networkidle', timeout=30000)
            logger.info(f"📍 URL actual: {self.page.url}")
            
            # Esperar el iframe
            logger.info("🔍 Buscando iframe...")
            try:
                iframe_element = self.page.wait_for_selector(
                    'iframe#_cl_tbk_iframe_web_IframeCrossWebPortlet_portal30',
                    state='attached',
                    timeout=10000
                )
                logger.info("✅ Iframe encontrado")
                
                # Obtener el frame
                iframe = self.page.frame_locator('iframe#_cl_tbk_iframe_web_IframeCrossWebPortlet_portal30')
                logger.info("✅ Frame locator creado")
                
                # Esperar contenido del iframe
                time.sleep(3)
                
                # Screenshot
                screenshot_path = f'documentos_playwright_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
                self.page.screenshot(path=screenshot_path, full_page=True)
                logger.info(f"📸 Página de documentos capturada: {screenshot_path}")
                
                return True
                
            except PlaywrightTimeout:
                logger.error("❌ No se encontró el iframe en 10 segundos")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error al navegar a documentos: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def buscar_documentos(self, fecha_desde, fecha_hasta):
        """
        Busca documentos en el rango de fechas especificado
        Interactúa con el formulario dentro del iframe
        """
        logger.info(f"🔍 Buscando documentos desde {fecha_desde} hasta {fecha_hasta}...")
        
        try:
            # Acceder al iframe
            iframe = self.page.frame_locator('iframe#_cl_tbk_iframe_web_IframeCrossWebPortlet_portal30')
            
            # Esperar que el formulario esté visible
            logger.info("Esperando formulario de búsqueda...")
            
            # Buscar campos de fecha (ajustar selectores según el HTML real)
            # Estos selectores son tentativos - hay que verificar con el HTML real
            fecha_desde_input = iframe.locator('input[name*="fechaDesde"], input[id*="fechaDesde"]').first
            fecha_hasta_input = iframe.locator('input[name*="fechaHasta"], input[id*="fechaHasta"]').first
            
            # Llenar fechas
            logger.info(f"Ingresando fecha desde: {fecha_desde}")
            fecha_desde_input.fill(fecha_desde)
            
            logger.info(f"Ingresando fecha hasta: {fecha_hasta}")
            fecha_hasta_input.fill(fecha_hasta)
            
            # Buscar botón de búsqueda
            buscar_btn = iframe.locator('button:has-text("Buscar"), input[type="submit"][value*="Buscar"]').first
            buscar_btn.click()
            
            logger.info("⏳ Esperando resultados...")
            time.sleep(5)
            
            # Screenshot de resultados
            screenshot_path = f'resultados_playwright_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            self.page.screenshot(path=screenshot_path, full_page=True)
            logger.info(f"📸 Resultados capturados: {screenshot_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error al buscar documentos: {e}")
            logger.warning("⚠️ Los selectores pueden necesitar ajuste según el HTML real")
            import traceback
            traceback.print_exc()
            return False
    
    def seleccionar_documentos(self):
        """Selecciona todos los documentos encontrados"""
        logger.info("✅ Seleccionando todos los documentos...")
        
        try:
            iframe = self.page.frame_locator('iframe#_cl_tbk_iframe_web_IframeCrossWebPortlet_portal30')
            
            # Buscar checkbox "Seleccionar todos"
            select_all = iframe.locator('input[type="checkbox"][name*="selectAll"], input[type="checkbox"][id*="selectAll"]').first
            select_all.check()
            
            time.sleep(1)
            logger.info("✅ Documentos seleccionados")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error al seleccionar documentos: {e}")
            return False
    
    def descargar_masiva(self):
        """Inicia la descarga masiva de documentos"""
        logger.info("📥 Iniciando descarga masiva...")
        
        try:
            iframe = self.page.frame_locator('iframe#_cl_tbk_iframe_web_IframeCrossWebPortlet_portal30')
            
            # Buscar botón de descarga
            download_btn = iframe.locator('button:has-text("Descargar"), a:has-text("Descargar")').first
            
            # Configurar listener de descarga
            with self.page.expect_download() as download_info:
                download_btn.click()
            
            download = download_info.value
            logger.info(f"✅ Descarga iniciada: {download.suggested_filename}")
            
            # Guardar archivo
            download_path = f'downloads/{download.suggested_filename}'
            download.save_as(download_path)
            logger.info(f"💾 Archivo guardado en: {download_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en descarga: {e}")
            return False
    
    def close(self):
        """Cierra el navegador"""
        logger.info("Cerrando navegador...")
        if self.page:
            self.page.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        logger.info("✅ Navegador cerrado")
