"""
Bot de Transbank usando Requests + BeautifulSoup (sin navegador)
Más rápido y sin problemas de ChromeDriver
"""
import requests
from bs4 import BeautifulSoup
import time
import os
from datetime import datetime
from config.settings import (
    TRANSBANK_RUT, TRANSBANK_PASSWORD, LOGIN_URL, BASE_URL, DOCUMENTOS_URL
)
from bot.utils import logger, format_rut


class TransbankRequestsBot:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-CL,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        self.logged_in = False
        self.empresa_id = None
        
    def login(self, rut=None, password=None):
        """
        Hace login usando POST requests (sin navegador)
        """
        rut = rut or TRANSBANK_RUT
        password = password or TRANSBANK_PASSWORD
        
        logger.info("🔍 PASO 1: Cargando página de login para obtener tokens...")
        
        try:
            # PASO 1: GET a la página de login para obtener cookies y tokens CSRF
            response = self.session.get(LOGIN_URL, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')
            logger.info(f"✅ Página cargada (Status: {response.status_code})")
            
            # Buscar el token p_auth (Liferay portal authentication)
            p_auth = None
            for input_tag in soup.find_all('input', {'name': 'p_auth'}):
                p_auth = input_tag.get('value')
                break
            
            if not p_auth:
                # Intentar extraer de URLs en la página
                for link in soup.find_all('a'):
                    href = link.get('href', '')
                    if 'p_auth=' in href:
                        p_auth = href.split('p_auth=')[1].split('&')[0]
                        break
            
            logger.info(f"🔑 Token p_auth: {p_auth[:20] if p_auth else 'NO ENCONTRADO'}...")
            
            # PASO 2: Preparar el POST del login
            logger.info("🔍 PASO 2: Enviando credenciales...")
            
            # Datos del formulario de login (Liferay portal)
            login_data = {
                '_LoginWebPortlet_formDate': str(int(time.time() * 1000)),
                '_LoginWebPortlet_username': format_rut(rut),
                '_LoginWebPortlet_contrasena': password,
                '_LoginWebPortlet_rememberMe': 'false',
            }
            
            if p_auth:
                login_data['p_auth'] = p_auth
            
            # URL del POST (puede ser la misma o una diferente)
            login_post_url = LOGIN_URL
            
            # Hacer el POST
            response = self.session.post(
                login_post_url,
                data=login_data,
                timeout=15,
                allow_redirects=True
            )
            
            logger.info(f"📥 Respuesta del login: Status {response.status_code}")
            logger.info(f"📍 URL final: {response.url}")
            logger.info(f"🍪 Cookies activas: {len(self.session.cookies)} cookies")
            for cookie in self.session.cookies:
                logger.info(f"  - {cookie.name}: {cookie.value[:20]}...")
            
            # PASO 3: Verificar si el login fue exitoso
            # Posibles indicadores de éxito:
            # - Redirección a /portal-3.0 (no /login)
            # - Presencia de modal de empresas
            # - Ausencia de mensajes de error
            
            soup_response = BeautifulSoup(response.text, 'lxml')
            
            # Buscar modal de empresas
            modal_empresas = soup_response.find('div', {'id': '_LoginWebPortlet_modal_org_select'})
            
            if modal_empresas:
                logger.info("✅ MODAL DE EMPRESAS DETECTADO - Login exitoso")
                self.logged_in = True
                
                # PASO 4: Seleccionar empresa (click en "Iniciar sesión" del modal)
                return self._seleccionar_empresa_modal(soup_response, response.url)
            
            # Verificar si ya estamos en el portal (sin modal)
            if '/portal-3.0' in response.url and '/login' not in response.url:
                logger.info("✅ LOGIN EXITOSO - Ya estamos en el portal")
                self.logged_in = True
                return True
            
            # Buscar mensajes de error
            error_msgs = soup_response.find_all(['div', 'span'], class_=lambda x: x and 'error' in x.lower() if x else False)
            if error_msgs:
                error_text = ' | '.join([msg.get_text(strip=True) for msg in error_msgs[:3]])
                logger.error(f"❌ Error de login: {error_text}")
                return False
            
            # Si no hay modal ni redirección clara, algo falló
            logger.warning("⚠️ Login ambiguo - No se detectó modal ni redirección clara")
            
            # Guardar HTML para debug
            debug_file = f"debug_login_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            logger.info(f"💾 HTML guardado en: {debug_file}")
            
            return False
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error de conexión: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error inesperado: {e}")
            return False
    
    def _seleccionar_empresa_modal(self, soup, current_url):
        """
        Simula el click en 'Iniciar sesión' del modal de empresas
        """
        logger.info("🔍 PASO 4: Procesando modal de empresas...")
        
        # Buscar formulario del modal
        modal = soup.find('div', {'id': '_LoginWebPortlet_modal_org_select'})
        if not modal:
            logger.error("❌ No se encontró el modal de empresas en el HTML")
            return False
        
        # Buscar el formulario dentro del modal
        form = modal.find('form')
        if not form:
            logger.error("❌ No se encontró formulario en el modal")
            return False
        
        # Extraer action del formulario
        form_action = form.get('action', '')
        if not form_action:
            form_action = current_url
        elif form_action.startswith('/'):
            form_action = BASE_URL + form_action
        
        logger.info(f"📍 Form action: {form_action}")
        
        # Extraer datos del formulario
        form_data = {}
        for input_tag in form.find_all('input'):
            name = input_tag.get('name')
            value = input_tag.get('value', '')
            if name:
                form_data[name] = value
        
        # Buscar empresa seleccionada por defecto (radio button checked)
        empresa_radios = modal.find_all('input', {'type': 'radio', 'name': '_LoginWebPortlet_org'})
        for radio in empresa_radios:
            if radio.get('checked'):
                form_data['_LoginWebPortlet_org'] = radio.get('value')
                logger.info(f"✅ Empresa por defecto: {radio.get('value')}")
                break
        
        # Si no hay empresa marcada, usar la primera
        if '_LoginWebPortlet_org' not in form_data and empresa_radios:
            form_data['_LoginWebPortlet_org'] = empresa_radios[0].get('value')
            logger.info(f"✅ Usando primera empresa: {empresa_radios[0].get('value')}")
        
        logger.info(f"📤 Enviando selección de empresa...")
        logger.info(f"📋 Datos del formulario: {list(form_data.keys())}")
        
        # Hacer el POST del formulario
        try:
            response = self.session.post(
                form_action,
                data=form_data,
                timeout=15,
                allow_redirects=True
            )
            
            logger.info(f"📥 Respuesta: Status {response.status_code}")
            logger.info(f"📍 URL final: {response.url}")
            
            # Verificar si estamos en el portal
            if '/portal-3.0' in response.url and '/login' not in response.url:
                logger.info("✅ ACCESO AL PORTAL COMPLETADO")
                self.logged_in = True
                return True
            
            # Guardar HTML para debug
            debug_file = f"debug_empresa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            logger.info(f"💾 HTML guardado en: {debug_file}")
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Error al seleccionar empresa: {e}")
            return False
    
    def navegar_a_documentos(self):
        """
        Navega a la sección de Documentos Electrónicos
        """
        if not self.logged_in:
            logger.error("❌ Debes hacer login primero")
            return False
        
        logger.info("📄 Navegando a Documentos Electrónicos...")
        logger.info(f"🍪 Cookies disponibles: {len(self.session.cookies)} cookies")
        
        try:
            response = self.session.get(DOCUMENTOS_URL, timeout=15, allow_redirects=True)
            logger.info(f"📥 Status: {response.status_code}")
            logger.info(f"📍 URL final: {response.url}")
            
            # Verificar si nos redirigió al login
            if '/login' in response.url:
                logger.error("❌ REDIRIGIDO AL LOGIN - La sesión no se mantuvo")
                logger.error("   Esto indica que Transbank requiere JavaScript para mantener la sesión")
                logger.error("   o usa tokens anti-CSRF más complejos")
                return False
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Buscar el iframe
            iframe = soup.find('iframe', {'id': '_cl_tbk_iframe_web_IframeCrossWebPortlet_portal30'})
            if iframe:
                iframe_src = iframe.get('src', '')
                if iframe_src:
                    if iframe_src.startswith('/'):
                        iframe_src = BASE_URL + iframe_src
                    
                    logger.info(f"🎯 Iframe encontrado: {iframe_src[:80]}...")
                    
                    # Cargar contenido del iframe
                    iframe_response = self.session.get(iframe_src, timeout=15)
                    logger.info(f"📥 Iframe cargado: Status {iframe_response.status_code}")
                    
                    # Guardar para debug
                    debug_file = f"debug_iframe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                    with open(debug_file, 'w', encoding='utf-8') as f:
                        f.write(iframe_response.text)
                    logger.info(f"💾 Contenido del iframe guardado en: {debug_file}")
                    
                    return True
            
            logger.warning("⚠️ No se encontró el iframe esperado")
            
            # Guardar para debug
            debug_file = f"debug_documentos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            logger.info(f"💾 HTML guardado en: {debug_file}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error al navegar a documentos: {e}")
            return False
    
    def buscar_documentos(self, fecha_desde, fecha_hasta):
        """
        Busca documentos en el rango de fechas especificado
        TODO: Implementar una vez que tengamos el HTML del iframe
        """
        logger.info(f"🔍 Buscando documentos desde {fecha_desde} hasta {fecha_hasta}...")
        logger.warning("⚠️ Función en desarrollo - analizar HTML del iframe primero")
        return True
    
    def close(self):
        """
        Cierra la sesión
        """
        logger.info("👋 Cerrando sesión...")
        self.session.close()
        self.logged_in = False
