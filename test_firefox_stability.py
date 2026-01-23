"""
Test mínimo para verificar estabilidad del driver
"""
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import geckodriver_autoinstaller
import time

print("=== TEST DE ESTABILIDAD DE GECKODRIVER ===\n")

try:
    print("1. Instalando GeckoDriver...")
    geckodriver_autoinstaller.install()
    print("   ✅ GeckoDriver instalado\n")
    
    print("2. Configurando Firefox...")
    options = Options()
    service = Service(log_path='geckodriver_test.log')
    print("   ✅ Opciones configuradas\n")
    
    print("3. Lanzando Firefox...")
    driver = webdriver.Firefox(options=options, service=service)
    print("   ✅ Firefox lanzado\n")
    
    print("4. Configurando timeouts...")
    driver.set_page_load_timeout(120)
    driver.implicitly_wait(30)
    print("   ✅ Timeouts configurados\n")
    
    print("5. Esperando 10 segundos SIN hacer nada...")
    for i in range(10, 0, -1):
        print(f"   {i}...", end=" ", flush=True)
        time.sleep(1)
    print("\n   ✅ 10 segundos completados - driver sigue vivo\n")
    
    print("6. Navegando a Google (página simple)...")
    driver.get("https://www.google.com")
    print(f"   ✅ Título: {driver.title}\n")
    
    print("7. Esperando otros 10 segundos...")
    for i in range(10, 0, -1):
        print(f"   {i}...", end=" ", flush=True)
        time.sleep(1)
    print("\n   ✅ 10 segundos más - driver sigue vivo\n")
    
    print("8. Obteniendo URL actual...")
    url = driver.current_url
    print(f"   ✅ URL: {url}\n")
    
    print("9. Tomando screenshot...")
    driver.save_screenshot("test_firefox_estabilidad.png")
    print("   ✅ Screenshot guardado\n")
    
    print("✅ TEST COMPLETADO - GeckoDriver es ESTABLE en tu sistema")
    print("\nPresiona ENTER para cerrar Firefox...")
    input()
    
    driver.quit()
    print("✅ Firefox cerrado correctamente")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    print("\nPresiona ENTER para salir...")
    input()
