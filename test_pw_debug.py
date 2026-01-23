"""
Test de Playwright - paso a paso con screenshots
"""
from playwright.sync_api import sync_playwright
import time

print("=== PLAYWRIGHT - TEST DETALLADO ===\n")

try:
    with sync_playwright() as p:
        print("1. Lanzando navegador...")
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        
        print("2. Navegando a Transbank...")
        page.goto("https://privado.transbank.cl/group/portal-3.0/login", timeout=60000)
        print(f"   ✅ Página cargada: {page.title()}")
        
        page.screenshot(path="pw_01_pagina.png")
        print("   📸 Screenshot: pw_01_pagina.png")
        
        print("\n3. Buscando campo RUT...")
        rut_field = page.locator('#_LoginWebPortlet_username')
        if rut_field.count() > 0:
            print(f"   ✅ Campo RUT encontrado (visible: {rut_field.is_visible()})")
        else:
            print("   ❌ Campo RUT NO encontrado")
        
        print("\n4. Buscando botón Ingresar...")
        btn = page.locator('#_LoginWebPortlet_btnIngresar')
        if btn.count() > 0:
            print(f"   ✅ Botón encontrado (visible: {btn.is_visible()})")
            btn.scroll_into_view_if_needed()
            print(f"   Después del scroll (visible: {btn.is_visible()})")
        else:
            print("   ❌ Botón NO encontrado")
        
        page.screenshot(path="pw_02_elementos.png")
        print("   📸 Screenshot: pw_02_elementos.png")
        
        print("\n5. Cerrando en 5 segundos...")
        time.sleep(5)
        
        browser.close()
        print("✅ Test completado")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
