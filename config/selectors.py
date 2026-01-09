"""
Selectores CSS e IDs de elementos HTML del portal de Transbank
"""

# ============================================
# LOGIN PAGE
# ============================================
class LoginSelectors:
    RUT_INPUT = 'rutPersona'
    PASSWORD_INPUT = 'password'
    LOGIN_BUTTON = 'button.btn-primary'
    ERROR_MESSAGE = '.form-validator-stack'

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
    EMPRESA_ACTUAL = '.change_sessions'

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