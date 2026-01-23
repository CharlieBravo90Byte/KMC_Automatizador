"""
Selectores CSS e IDs de elementos HTML del portal de Transbank
"""

# ============================================
# LOGIN PAGE
# ============================================
class LoginSelectors:
    RUT_INPUT = '_LoginWebPortlet_username'
    PASSWORD_INPUT = '_LoginWebPortlet_contrasena'
    LOGIN_BUTTON = '#_LoginWebPortlet_btnIngresar'
    ERROR_MESSAGE = '#_LoginWebPortlet_wrongUserOrPass'
    # Elementos de bloqueo comunes
    POPUP_MODAL = '.modal, #modal, [role="dialog"]'
    CLOSE_BUTTON = '.close, .btn-close, [aria-label="close"], [aria-label="Close"]'
    LOADING_OVERLAY = '.loading, .overlay, .spinner'
    COOKIE_BANNER = '[class*="cookie"], [id*="cookie"], [class*="gdpr"]'

# ============================================
# MODAL DE SELECCIÓN DE EMPRESA
# ============================================
class EmpresaSelectors:
    MODAL = '#_LoginWebPortlet_modalOrgSelector'
    DROPDOWN_UL = '_LoginWebPortlet_organizacionListado'
    EMPRESA_ITEM = 'li'  # Dentro del ul con id organizacionListado
    INICIAR_SESION_BUTTON = 'button.btn-primary'

# ============================================
# DASHBOARD
# ============================================
class DashboardSelectors:
    MENU_LATERAL = 'nav'
    DOCUMENTOS_LINK = 'a[href*="documentos-electronicos"]'
    
    # Selector de empresa en dashboard
    EMPRESA_ACTUAL = '.change_sessions'
    EMPRESA_NOMBRE_DISPLAY = 'span[nombredisplay]'
    EMPRESA_DROPDOWN_BUTTON = 'button.org-tbk'
    EMPRESA_LISTA = 'ul.list-org'
    EMPRESA_ITEM = 'li[data-org-rut]'

# ============================================
# DOCUMENTOS ELECTRÓNICOS (IFRAME)
# ============================================
class DocumentosSelectors:
    # Iframe principal
    IFRAME_ID = '_cl_tbk_iframe_web_IframeCrossWebPortlet_portal30'
    
    # Filtros de búsqueda
    DIA_INPUT = 'inputDia'
    MES_SELECT = 'selectMes'
    YEAR_SELECT = 'selectYear'
    PRODUCTO_SELECT = 'select.selector-dinamico'
    
    # Botones
    BUSCAR_BUTTON = 'consultar'
    DESCARGA_MASIVA_BUTTON = 'button.descarga-masiva'
    
    # Tabla de resultados
    TABLA_DOCUMENTOS = 'tablaDocumentos'
    TABLA_FILAS = '#tablaDocumentos tbody tr'
    TABLA_EMPTY = '.dataTables_empty'
    CHECKBOXES = 'input[type="checkbox"]'
    
    # Mensajes
    ERROR_MESSAGE = '.alerta.roja'
    ALERTA_MESSAGE = '.alerta.amarilla'
    LOADING = '.dataTables_processing'

# ============================================
# VALORES DE PRODUCTOS
# ============================================
class ProductoValues:
    TODOS = '-1'
    DETALLE_TRANSACCIONES = '67'
    DETALLE_SALDOS = '66'
    INFORME_SALDOS = '65'