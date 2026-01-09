# 🤖 Transbank Bot - Automatizador de Documentos Electrónicos

Bot automatizado para descargar documentos electrónicos desde el portal privado de Transbank.

## 📋 Requisitos

- Python 3.8 o superior
- Google Chrome instalado
- Cuenta de Transbank con acceso al portal privado

## 🚀 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/CharlieBravo90Byte/KMC_Automatizador.git
cd KMC_Automatizador
```

2. Crear entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar credenciales:
```bash
# Copiar el archivo de ejemplo
copy .env.example .env

# Editar .env con tus credenciales reales
```

## 🎯 Uso

```bash
python main.py
```

## 📁 Estructura del Proyecto

```
KMC_Automatizador/
├── config/           # Configuración y selectores
├── bot/              # Módulos del bot
├── downloads/        # Archivos descargados
├── main.py           # Script principal
└── README.md         # Este archivo
```

## ⚙️ Configuración

Edita el archivo `.env` con tus credenciales:

```env
TRANSBANK_RUT=tu_rut_aqui
TRANSBANK_PASSWORD=tu_password_aqui
TRANSBANK_EMPRESA=nombre_de_tu_empresa
```

## 🔧 Funcionalidades

- ✅ Login automático
- ✅ Selección de empresa
- ✅ Navegación a Documentos Electrónicos
- ✅ Filtrado por fecha y producto
- ✅ Descarga masiva de documentos

## 📝 Licencia

MIT License