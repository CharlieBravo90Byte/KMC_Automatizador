"""
Script de prueba simple para Playwright
"""
from playwright.sync_api import sync_playwright
import time

print("=== TEST PLAYWRIGHT ===")
print("Iniciando navegador...")

try:
    with sync_playwright() as p:
        print("✅ Playwright iniciado")
        
        browser = p.chromium.launch(headless=False)
        print("✅ Chromium lanzado")
        
        page = browser.new_page()
        print("✅ Página creada")
        
        print("Navegando a Transbank...")
        page.goto("https://privado.transbank.cl/group/portal-3.0/login", timeout=60000)
        print(f"✅ Página cargada: {page.title()}")
        
        time.sleep(5)
        
        print("Tomando screenshot...")
        page.screenshot(path="test_playwright.png")
        print("✅ Screenshot guardado")
        
        print("\nPresiona ENTER para cerrar...")
        input()
        
        browser.close()
        print("✅ Navegador cerrado")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
