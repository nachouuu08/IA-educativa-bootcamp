# Log de Despliegue - IA Educativa Bootcamp

## Fecha: 2025-10-10

## Resumen
Se subió la carpeta `templates` a GitHub y se corrigieron problemas de compatibilidad para el despliegue en Render.com.

## Pasos Realizados

### 1. Subida Inicial de Templates
- Se agregó la carpeta `templates` al repositorio Git local.
- Commit: "Add templates"
- Intento de push a GitHub, pero falló inicialmente por conexión.

### 2. Problemas Detectados en Render
- Error: `jinja2.exceptions.TemplateNotFound: login.html`
- Causa: La carpeta estaba nombrada `Templates` (mayúscula), incompatible con Linux (case-sensitive).
- Error adicional: `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff`
- Causa: Archivos en UTF-16 con BOM, no UTF-8.

### 3. Correcciones Aplicadas
- **Renombrado de carpeta**: `Templates` → `templates` usando Git.
- **Conversión de codificación**:
  - De UTF-16 a UTF-8.
  - Eliminación de BOM (Byte Order Mark).
- **Cambio de line endings**: De CRLF (Windows) a LF (Unix).
- Configuración de Git: `core.autocrlf = false` para preservar LF.
- Commits:
  - "Fix encoding of HTML templates to UTF-8 without BOM"
  - "Fix line endings to LF for Unix compatibility"

### 4. Subida a GitHub
- Push falló por problemas de conexión a `github.com` puerto 443.
- Solución: Upload manual de archivos HTML corregidos a GitHub vía web interface.

### 5. Despliegue en Render
- Deploy manual para aplicar cambios.
- Verificación: Las plantillas ahora cargan correctamente sin errores.

## Archivos Afectados
- `templates/index.html`
- `templates/login.html`
- `templates/perfil.html`
- `templates/practico.html`
- `templates/register.html`
- `templates/visual.html`

## Configuraciones
- Git: `core.autocrlf = false`
- Codificación: UTF-8 sin BOM
- Line endings: LF

## Notas
- Render redeploya automáticamente al push, pero se usó manual deploy debido a fallos de conexión.
- Problemas de conexión a GitHub pueden deberse a firewall o red; usar VPN o upload manual como alternativa.

## Estado Final
✅ Templates subidos y funcionales en Render.com