"""
Módulo de Documentos Electrónicos para Transbank
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from config.selectors import DashboardSelectors, DocumentosSelectors, ProductoValues
from bot.utils import logger, wait_and_find, wait_and_click, wait_for_download
from config.settings import WAIT_MEDIUM, DOWNLOAD_PATH


class DocumentosElectronicos:
    def __init__(self, driver):
        self.driver = driver
    
    def navegar_a_documentos(self):
        """
        Navega desde el dashboard a Documentos Electrónicos
        """
        logger.info("Navegando a 'Documentos Electrónicos'...")
        
        try:
            # SOLUCIÓN DIRECTA: Navegar a la URL conocida sin buscar
            # La URL de documentos electrónicos sigue un patrón conocido
            base_url = self.driver.current_url
            
            # Si estamos en el dashboard (portal-3.0), agregar la ruta de documentos
            if "portal-3.0" in base_url:
                # Construir URL directa
                doc_url = base_url.split("/portal")[0] + "/group/portal-3.0/documentos-electronicos"
                logger.info(f"Navegando directamente a: {doc_url}")
                self.driver.get(doc_url)
                time.sleep(5)
                logger.info(f"📍 URL actual: {self.driver.current_url}")
                logger.info("✅ Navegación exitosa - DEBERÍAS VER LA PÁGINA DE DOCUMENTOS")
                return True
            else:
                logger.error(f"❌ URL inesperada: {base_url}")
                return False
            
        except Exception as e:
            logger.error(f"❌ Error navegando: {e}")
            return False
    
    def cambiar_a_iframe(self):
        """
        Cambia el contexto al iframe de documentos electrónicos
        """
        logger.info("Cambiando contexto al iframe...")
        
        try:
            # Buscar TODOS los iframes
            all_iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            logger.info(f"🔍 Total de iframes encontrados: {len(all_iframes)}")
            
            # Listar información de todos los iframes
            for i, frame in enumerate(all_iframes):
                try:
                    frame_id = frame.get_attribute("id") or "sin ID"
                    frame_name = frame.get_attribute("name") or "sin name"
                    frame_src = frame.get_attribute("src") or "sin src"
                    logger.info(f"   IFRAME #{i+1}: ID={frame_id}, NAME={frame_name}")
                except Exception as e:
                    logger.info(f"   IFRAME #{i+1}: Error obteniendo datos - {e}")
            
            # Intentar con el ID conocido
            logger.info(f"Buscando iframe con ID: {DocumentosSelectors.IFRAME_ID}")
            iframe = None
            try:
                iframe = self.driver.find_element(By.ID, DocumentosSelectors.IFRAME_ID)
                logger.info("✅ Iframe encontrado con ID conocido")
            except:
                logger.warning("⚠️ No se encontró iframe con ID conocido")
                
                # Intentar con el primer iframe disponible
                if all_iframes:
                    logger.info("Intentando con el primer iframe disponible...")
                    iframe = all_iframes[0]
                else:
                    logger.error("❌ No hay iframes disponibles")
                    return False
            
            # Cambiar al contexto del iframe
            self.driver.switch_to.frame(iframe)
            logger.info("✅ Contexto cambiado al iframe")
            
            logger.info("Esperando que cargue contenido del iframe...")
            time.sleep(3)  # Pausa para ver el iframe
            
            logger.info("✅ Iframe cargado - DEBERÍAS VER EL FORMULARIO DE BÚSQUEDA")
            return True
            logger.info("📸 Captura: iframe_2_dentro.png")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error cambiando a iframe: {e}")
            return False
    
    def buscar_documentos(self, dia=None, mes=None, year=None, producto=ProductoValues.TODOS):
        """
        Realiza búsqueda de documentos con filtros
        
        Args:
            dia: Día del mes (1-31) o None para todo el mes
            mes: Mes (1-12) o None para usar el actual
            year: Año (ej: 2026) o None para usar el actual
            producto: Código del producto (usar ProductoValues)
        """
        logger.info("Aplicando filtros de búsqueda...")
        
        try:
            # Filtro de día (opcional)
            if dia:
                dia_input = wait_and_find(self.driver, By.ID, DocumentosSelectors.DIA_INPUT)
                dia_input.clear()
                dia_input.send_keys(str(dia))
                logger.info(f"Día: {dia}")
            
            # Filtro de mes
            if mes:
                mes_select = Select(wait_and_find(self.driver, By.ID, DocumentosSelectors.MES_SELECT))
                mes_select.select_by_value(str(mes))
                logger.info(f"Mes: {mes}")
            
            # Filtro de año
            if year:
                year_select = Select(wait_and_find(self.driver, By.ID, DocumentosSelectors.YEAR_SELECT))
                year_select.select_by_value(str(year))
                logger.info(f"Año: {year}")
            
            # Filtro de producto
            producto_select = Select(wait_and_find(
                self.driver, 
                By.CSS_SELECTOR, 
                DocumentosSelectors.PRODUCTO_SELECT
            ))
            producto_select.select_by_value(producto)
            logger.info(f"Producto: {producto}")
            
            # Click en botón Buscar
            buscar_btn = wait_and_find(self.driver, By.ID, DocumentosSelectors.BUSCAR_BUTTON)
            buscar_btn.click()
            logger.info("Click en 'Buscar'")
            
            # Esperar a que cargue la tabla
            time.sleep(WAIT_MEDIUM)
            
            # Verificar si hay resultados
            try:
                empty_msg = self.driver.find_element(By.CSS_SELECTOR, DocumentosSelectors.TABLA_EMPTY)
                if empty_msg.is_displayed():
                    logger.warning("⚠️ No hay documentos para los filtros aplicados")
                    return False
            except:
                logger.info("✅ Documentos encontrados")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en búsqueda: {e}")
            return False
    
    def seleccionar_documentos(self, max_documentos=10):
        """
        Selecciona checkboxes de documentos (máximo 10)
        """
        logger.info(f"Seleccionando hasta {max_documentos} documentos...")
        
        try:
            # Encontrar todos los checkboxes en la tabla
            checkboxes = self.driver.find_elements(
                By.CSS_SELECTOR, 
                f'#{DocumentosSelectors.TABLA_DOCUMENTOS} {DocumentosSelectors.CHECKBOXES}'
            )
            
            if not checkboxes:
                logger.warning("No se encontraron checkboxes")
                return 0
            
            # Seleccionar hasta max_documentos
            seleccionados = 0
            for checkbox in checkboxes[:max_documentos]:
                if not checkbox.is_selected():
                    checkbox.click()
                    seleccionados += 1
                    time.sleep(0.5)
            
            logger.info(f"✅ {seleccionados} documentos seleccionados")
            return seleccionados
            
        except Exception as e:
            logger.error(f"❌ Error seleccionando documentos: {e}")
            return 0
    
    def descargar_masiva(self):
        """
        Realiza descarga masiva de documentos seleccionados
        """
        logger.info("Iniciando descarga masiva...")
        
        try:
            # Click en botón Descarga Masiva
            descarga_btn = wait_and_find(
                self.driver, 
                By.CSS_SELECTOR, 
                DocumentosSelectors.DESCARGA_MASIVA_BUTTON
            )
            descarga_btn.click()
            logger.info("Click en 'Descarga Masiva'")
            
            # Esperar a que se complete la descarga
            if wait_for_download(DOWNLOAD_PATH):
                logger.info("✅ Descarga completada exitosamente")
                return True
            else:
                logger.warning("⚠️ Timeout esperando descarga")
                return False
            
        except Exception as e:
            logger.error(f"❌ Error en descarga masiva: {e}")
            return False
    
    def volver_al_contexto_principal(self):
        """
        Vuelve al contexto principal (fuera del iframe)
        """
        self.driver.switch_to.default_content()
        logger.info("Contexto vuelto a la página principal")