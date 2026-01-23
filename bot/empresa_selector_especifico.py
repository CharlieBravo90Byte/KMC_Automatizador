"""
SELECTOR DE EMPRESA CON MANEJO DE 2 ESCENARIOS:
1. Modal de selección aparece (múltiples empresas)
2. Redirección directa al dashboard (una sola empresa)
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def seleccionar_empresa_especifica(driver, timeout=30):
    """
    Maneja la selección de empresa o verifica que ya estemos en el dashboard correcto
    """
    print("\n" + "="*70)
    print("🏢 GESTIÓN DE SELECCIÓN DE EMPRESA")
    print("="*70)
    
    try:
        # ESCENARIO 1: Buscar el modal de selección
        print("\n[1/2] 🔍 Verificando si aparece modal de selección...")
        
        # Esperar tiempo razonable
        time.sleep(6)
        
        # Guardar captura del estado actual
        try:
            driver.save_screenshot("seleccion_1_estado_inicial.png")
            print("   📸 seleccion_1_estado_inicial.png")
        except:
            pass
        
        url_actual = driver.current_url
        print(f"   📍 URL actual: {url_actual}")
        
        # Intentar encontrar el modal
        modal_encontrado = False
        try:
            modal = driver.find_element(By.ID, "_LoginWebPortlet_modal__org_select")
            modal_encontrado = modal.is_displayed()
            print(f"   {'✅' if modal_encontrado else '⚠️'} Modal encontrado (visible: {modal_encontrado})")
        except:
            print("   ⚠️ Modal no encontrado")
        
        # CASO A: SI HAY MODAL - Seleccionar empresa
        if modal_encontrado:
            print("\n   📋 CASO A: Modal detectado - Procediendo a seleccionar empresa")
            return seleccionar_en_modal(driver)
        
        # CASO B: NO HAY MODAL - Verificar si ya estamos en dashboard
        else:
            print("\n   📋 CASO B: Sin modal - Verificando dashboard")
            return verificar_dashboard_directo(driver, url_actual)
            
    except Exception as e:
        print(f"\n❌ ERROR GENERAL: {e}")
        try:
            driver.save_screenshot("seleccion_error_general.png")
        except:
            pass
        return False


def seleccionar_en_modal(driver):
    """
    Selecciona INVERSIONES COLCHILE LIMITADA cuando el modal está presente
    """
    print("\n   🎯 Seleccionando empresa en modal...")
    
    try:
        # Buscar lista de empresas
        ul_empresas = driver.find_element(By.ID, "_LoginWebPortlet_organizacionListado")
        empresas = ul_empresas.find_elements(By.TAG_NAME, "a")
        
        print(f"   📊 Empresas disponibles: {len(empresas)}")
        
        empresa_objetivo = None
        for i, empresa in enumerate(empresas):
            texto = empresa.text.strip()
            seleccionada = 'selected' in (empresa.get_attribute('class') or '')
            
            print(f"      [{i+1}] {texto} {'✓' if seleccionada else ''}")
            
            if "INVERSIONES COLCHILE" in texto.upper():
                empresa_objetivo = empresa
                print(f"          🎯 ¡OBJETIVO!")
        
        if not empresa_objetivo:
            print("   ❌ INVERSIONES COLCHILE no encontrada")
            return False
        
        # Click en la empresa
        try:
            driver.execute_script("arguments[0].click();", empresa_objetivo)
            print("   ✅ Click ejecutado")
            time.sleep(3)
        except Exception as e:
            print(f"   ❌ Error en click: {e}")
            return False
        
        # Buscar y hacer click en botón de confirmación
        botones = driver.find_elements(By.CSS_SELECTOR, "button, input[type='submit']")
        for boton in botones:
            try:
                texto = (boton.text or boton.get_attribute('value') or '').strip().lower()
                if boton.is_displayed() and any(p in texto for p in ['iniciar', 'continuar', 'aceptar']):
                    driver.execute_script("arguments[0].click();", boton)
                    print(f"   ✅ Botón '{boton.text}' clickeado")
                    time.sleep(5)
                    break
            except:
                continue
        
        driver.save_screenshot("seleccion_2_empresa_seleccionada.png")
        return True
        
    except Exception as e:
        print(f"   ❌ Error en selección de modal: {e}")
        return False


def verificar_dashboard_directo(driver, url_actual):
    """
    Verifica si fuimos redirigidos directamente al dashboard
    Esto pasa cuando el usuario tiene solo UNA empresa
    """
    print("\n   🔍 Verificando acceso directo al dashboard...")
    
    try:
        # Esperar a que cargue el dashboard
        time.sleep(5)
        
        # Verificar si estamos en el dashboard
        if "inicio" in url_actual or "dashboard" in url_actual or "portal-3.0" in url_actual:
            print("   ✅ Redirigido al dashboard")
            
            # Buscar indicador de empresa actual
            selectores_empresa = [
                ".change_sessions",
                "[class*='empresa']",
                "[class*='organization']",
                "[class*='comercio']",
                "span.empresa",
                "div.empresa-actual"
            ]
            
            empresa_actual = None
            for selector in selectores_empresa:
                try:
                    elem = driver.find_element(By.CSS_SELECTOR, selector)
                    if elem.is_displayed():
                        empresa_actual = elem.text.strip()
                        print(f"   📋 Empresa actual detectada: {empresa_actual}")
                        break
                except:
                    continue
            
            # Verificar si es la empresa correcta
            if empresa_actual and "INVERSIONES COLCHILE" in empresa_actual.upper():
                print("   ✅ ¡CORRECTO! Ya estás en INVERSIONES COLCHILE LIMITADA")
                driver.save_screenshot("seleccion_2_dashboard_correcto.png")
                return True
            
            elif empresa_actual:
                print(f"   ⚠️ Empresa actual: {empresa_actual}")
                print("   ⚠️ NO es INVERSIONES COLCHILE LIMITADA")
                
                # Buscar si hay algún selector de empresa en el dashboard
                try:
                    selector = driver.find_element(By.CSS_SELECTOR, ".change_sessions, [onclick*='cambiar'], [onclick*='empresa']")
                    print("   🔄 Selector de empresa encontrado en dashboard")
                    print("   💡 Puedes intentar hacer click manual o configurar para cambiar empresa")
                    driver.save_screenshot("seleccion_2_empresa_incorrecta.png")
                    return False
                except:
                    print("   ❌ No se encontró forma de cambiar empresa")
                    driver.save_screenshot("seleccion_2_sin_selector.png")
                    return False
            
            else:
                print("   ⚠️ No se pudo determinar la empresa actual")
                print("   ℹ️ Puede que el usuario tenga solo una empresa y ya esté en ella")
                print("   🚀 Continuando con el proceso...")
                driver.save_screenshot("seleccion_2_dashboard_sin_indicador.png")
                return True  # Asumir éxito si no hay error obvio
        
        else:
            print(f"   ❌ URL inesperada: {url_actual}")
            driver.save_screenshot("seleccion_2_url_inesperada.png")
            return False
            
    except Exception as e:
        print(f"   ❌ Error verificando dashboard: {e}")
        driver.save_screenshot("seleccion_2_error_dashboard.png")
        return False
