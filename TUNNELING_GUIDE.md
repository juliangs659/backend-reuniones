# 🌐 Guía de Túneles para n8n Local - Exposición HTTPS

## 📋 Problema a resolver

Microsoft Graph API (Teams) requiere **URLs HTTPS públicas** para webhooks. Tu n8n está en `http://localhost:5678`, que:
- ❌ No es accesible desde Internet
- ❌ No tiene certificado SSL
- ❌ No puede recibir webhooks de Microsoft Teams

**Solución:** Usar un túnel que exponga tu n8n local con HTTPS público.

---

## 🎯 Opciones recomendadas

| Opción | Precio | Facilidad | Estabilidad | Recomendado |
|--------|--------|-----------|-------------|-------------|
| **Cloudflare Tunnel** | Gratis | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ **SÍ** |
| **ngrok** | Gratis/Pago | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⚠️ URL cambia |
| **LocalTunnel** | Gratis | ⭐⭐⭐⭐⭐ | ⭐⭐ | ❌ Inestable |
| **Tailscale Funnel** | Gratis | ⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Alternativa |

---

## 🚀 Opción 1: Cloudflare Tunnel (RECOMENDADA)

### ✅ Ventajas:
- ✅ **Gratis** permanentemente
- ✅ **URL fija** (no cambia)
- ✅ **HTTPS automático** con certificado de Cloudflare
- ✅ **Muy estable** (99.9% uptime)
- ✅ **Sin límites** de peticiones
- ✅ **DDoS protection** incluida
- ✅ **Dominio personalizado** (opcional)

### 📝 Requisitos:
- Cuenta gratuita en Cloudflare
- Un dominio (opcional, puedes usar subdominio de Cloudflare)

---

### 🔧 Instalación de Cloudflare Tunnel

#### 1. Instalar cloudflared

```bash
# En Ubuntu/Debian
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Verificar instalación
cloudflared --version
```

#### 2. Autenticarse con Cloudflare

```bash
# Esto abrirá tu navegador para autenticarte
cloudflared tunnel login
```

Se guardará un certificado en: `~/.cloudflared/cert.pem`

#### 3. Crear un túnel

```bash
# Crear túnel llamado "v1tr0-n8n"
cloudflared tunnel create v1tr0-n8n

# Esto genera:
# - Tunnel ID (ejemplo: a1b2c3d4-e5f6-7890-abcd-ef1234567890)
# - Archivo de credenciales en ~/.cloudflared/
```

**Guarda el Tunnel ID** que aparece!

#### 4. Configurar el túnel

```bash
# Crear archivo de configuración
mkdir -p ~/.cloudflared
nano ~/.cloudflared/config.yml
```

**Contenido del archivo `config.yml`:**

```yaml
tunnel: v1tr0-n8n
credentials-file: /home/julian/.cloudflared/<TUNNEL-ID>.json

ingress:
  # n8n webhook endpoint
  - hostname: n8n.tudominio.com
    service: http://localhost:5678
  
  # API backend (opcional, para exponer también la API)
  - hostname: api.tudominio.com
    service: http://localhost:8000
  
  # Catch-all rule (requerido)
  - service: http_status:404
```

**Si NO tienes dominio propio, usa subdominio de Cloudflare:**

```yaml
tunnel: v1tr0-n8n
credentials-file: /home/julian/.cloudflared/a1b2c3d4-e5f6-7890-abcd-ef1234567890.json

ingress:
  - hostname: v1tr0-n8n.your-cloudflare-tunnel-id.trycloudflare.com
    service: http://localhost:5678
  - service: http_status:404
```

#### 5. Configurar DNS en Cloudflare (si tienes dominio)

```bash
# Crear registro DNS que apunte al túnel
cloudflared tunnel route dns v1tr0-n8n n8n.tudominio.com
```

#### 6. Iniciar el túnel

```bash
# Modo prueba (ver logs)
cloudflared tunnel run v1tr0-n8n

# Modo background
cloudflared tunnel run --background v1tr0-n8n

# Ver status
cloudflared tunnel info v1tr0-n8n
```

#### 7. Como servicio systemd (para que inicie automáticamente)

```bash
# Instalar como servicio
sudo cloudflared service install

# Iniciar servicio
sudo systemctl start cloudflared
sudo systemctl enable cloudflared

# Ver logs
sudo journalctl -u cloudflared -f
```

#### 8. Verificar funcionamiento

```bash
# Tu n8n ahora está disponible en:
# https://n8n.tudominio.com
# o
# https://v1tr0-n8n.your-cloudflare-tunnel-id.trycloudflare.com

# Probar
curl https://n8n.tudominio.com
```

---

## ⚡ Opción 2: ngrok (Más rápido pero URL temporal)

### ✅ Ventajas:
- ✅ **Muy fácil** de usar
- ✅ **Setup en 2 minutos**
- ✅ **Inspección de requests** en dashboard

### ❌ Desventajas:
- ❌ **URL cambia** cada vez que reinicias (en plan free)
- ❌ **Límites:** 40 req/min en plan free
- ❌ **Debe estar corriendo** constantemente

---

### 🔧 Instalación de ngrok

#### 1. Instalar ngrok

```bash
# Método 1: Snap (recomendado)
sudo snap install ngrok

# Método 2: Descarga directa
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xvzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/
```

#### 2. Crear cuenta en ngrok

- Ir a: https://dashboard.ngrok.com/signup
- Copiar tu authtoken

#### 3. Configurar authtoken

```bash
ngrok config add-authtoken TU_AUTH_TOKEN_AQUI
```

#### 4. Iniciar túnel para n8n

```bash
# Exponer puerto 5678 (n8n)
ngrok http 5678

# Con región específica (más rápido)
ngrok http 5678 --region=us

# Con subdominio personalizado (requiere plan pago)
ngrok http 5678 --subdomain=v1tr0-n8n
```

#### 5. Resultado

Verás algo como:

```
Session Status                online
Account                       tu-email@example.com
Version                       3.5.0
Region                        United States (us)
Latency                       45ms
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok.io -> http://localhost:5678
```

**Tu URL pública HTTPS:** `https://abc123.ngrok.io`

#### 6. Ver requests en dashboard

```
http://localhost:4040
```

#### 7. Configurar para que persista (opcional)

Crear archivo `ngrok.yml`:

```bash
nano ~/.config/ngrok/ngrok.yml
```

Contenido:

```yaml
version: 2
authtoken: TU_AUTH_TOKEN
tunnels:
  n8n:
    proto: http
    addr: 5678
    inspect: true
  api:
    proto: http
    addr: 8000
    inspect: true
```

Iniciar todos los túneles:

```bash
ngrok start --all
```

---

## 🔥 Opción 3: Tailscale Funnel (Alternativa moderna)

### ✅ Ventajas:
- ✅ **Gratis** para uso personal
- ✅ **URL fija** personalizada
- ✅ **Zero-trust security**
- ✅ **Muy estable**

### 🔧 Instalación

```bash
# Instalar Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Autenticarse
sudo tailscale up

# Habilitar Funnel
sudo tailscale funnel 5678

# Tu URL será:
# https://your-machine-name.your-tailnet.ts.net
```

---

## 🎯 Configuración en Microsoft Graph API

### 1. Obtener tu URL pública

**Con Cloudflare:**
```
https://n8n.tudominio.com/webhook/teams-transcription
```

**Con ngrok:**
```
https://abc123.ngrok.io/webhook/teams-transcription
```

### 2. Configurar en Azure AD

```bash
# En Azure Portal
# 1. Ir a: Azure Active Directory > App registrations
# 2. Seleccionar tu app
# 3. Ir a: Certificates & secrets > Client secrets
# 4. Crear nuevo secret
# 5. Ir a: API permissions
#    - Add permission: Microsoft Graph > Application permissions
#    - OnlineMeetings.Read.All
#    - Chat.Read.All
# 6. Grant admin consent
```

### 3. Configurar webhook en Microsoft Graph

```bash
# Endpoint de Graph API
POST https://graph.microsoft.com/v1.0/subscriptions

# Body:
{
  "changeType": "created,updated",
  "notificationUrl": "https://n8n.tudominio.com/webhook/teams-transcription",
  "resource": "communications/onlineMeetings",
  "expirationDateTime": "2025-12-31T00:00:00Z",
  "clientState": "secretClientValue"
}

# Headers:
Authorization: Bearer {access_token}
Content-Type: application/json
```

### 4. Validar webhook en n8n

Microsoft enviará una validación inicial:

```json
{
  "validationToken": "abc123..."
}
```

Tu workflow de n8n debe responder:

```javascript
// En n8n Function node
return [{
  json: {
    validationToken: $input.first().json.validationToken
  }
}];
```

---

## 🛠️ Integración con docker-compose

### Agregar Cloudflare Tunnel a Docker

```yaml
# En docker-compose.yml
services:
  # ... servicios existentes ...

  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: v1tr0_cloudflared
    command: tunnel --no-autoupdate run --token ${CLOUDFLARE_TUNNEL_TOKEN}
    environment:
      - TUNNEL_TOKEN=${CLOUDFLARE_TUNNEL_TOKEN}
    networks:
      - v1tr0_network
    restart: unless-stopped
    depends_on:
      - n8n
      - api
```

En tu `.env`:

```bash
# Cloudflare Tunnel
CLOUDFLARE_TUNNEL_TOKEN=eyJhIjoiYWJjMTIzLi4u  # Token del túnel
```

---

## 📊 Comparativa detallada

### Cloudflare Tunnel

```
Precio: Gratis
URL: Fija (https://n8n.tudominio.com)
HTTPS: Automático
Setup: 10 minutos
Estabilidad: ⭐⭐⭐⭐⭐
Límites: Sin límites
Ventajas:
  ✅ Producción-ready
  ✅ DDoS protection
  ✅ URL personalizada
  ✅ Gratis para siempre
Desventajas:
  ❌ Requiere dominio (opcional)
  ❌ Setup inicial más complejo

Recomendado para: Producción y desarrollo estable
```

### ngrok

```
Precio: Gratis (con límites)
URL: Cambia cada reinicio (ej: https://abc123.ngrok.io)
HTTPS: Automático
Setup: 2 minutos
Estabilidad: ⭐⭐⭐
Límites: 40 req/min, 1 proceso
Ventajas:
  ✅ Muy fácil de usar
  ✅ Dashboard de inspección
  ✅ Setup instantáneo
Desventajas:
  ❌ URL temporal (plan free)
  ❌ Límites de requests
  ❌ Debe estar corriendo manualmente

Recomendado para: Testing rápido y desarrollo
```

### Tailscale Funnel

```
Precio: Gratis (uso personal)
URL: Fija (https://machine.tailnet.ts.net)
HTTPS: Automático
Setup: 5 minutos
Estabilidad: ⭐⭐⭐⭐
Límites: Razonables para uso personal
Ventajas:
  ✅ Zero-trust security
  ✅ URL fija
  ✅ Fácil de usar
Desventajas:
  ❌ Dominio no personalizable

Recomendado para: Equipos y desarrollo colaborativo
```

---

## 🎯 Recomendación según caso de uso

### Para Desarrollo / Testing:
```bash
👉 Usar: ngrok
Razón: Setup instantáneo, fácil de reiniciar

# Iniciar
ngrok http 5678

# URL temporal: https://abc123.ngrok.io
```

### Para Producción / Staging:
```bash
👉 Usar: Cloudflare Tunnel
Razón: Gratis, estable, URL fija, sin límites

# Iniciar una vez
cloudflared tunnel run v1tr0-n8n

# URL fija: https://n8n.tudominio.com
```

### Para Equipos distribuidos:
```bash
👉 Usar: Tailscale Funnel
Razón: Zero-trust, control de acceso

# Iniciar
tailscale funnel 5678

# URL: https://machine.tailnet.ts.net
```

---

## 📝 Checklist de configuración

### ✅ Cloudflare Tunnel (Producción)

- [ ] Crear cuenta en Cloudflare
- [ ] Instalar cloudflared
- [ ] Autenticarse: `cloudflared tunnel login`
- [ ] Crear túnel: `cloudflared tunnel create v1tr0-n8n`
- [ ] Configurar `~/.cloudflared/config.yml`
- [ ] Configurar DNS (si tienes dominio)
- [ ] Iniciar túnel: `cloudflared tunnel run v1tr0-n8n`
- [ ] Instalar como servicio systemd
- [ ] Probar acceso: `curl https://n8n.tudominio.com`
- [ ] Configurar webhook en Microsoft Graph
- [ ] Validar webhook en n8n
- [ ] Crear workflow de prueba
- [ ] Verificar logs: `sudo journalctl -u cloudflared -f`

### ✅ ngrok (Testing rápido)

- [ ] Crear cuenta en ngrok.com
- [ ] Instalar ngrok
- [ ] Configurar authtoken
- [ ] Iniciar túnel: `ngrok http 5678`
- [ ] Copiar URL HTTPS (ej: https://abc123.ngrok.io)
- [ ] Configurar en Microsoft Graph (recordar que cambiará)
- [ ] Crear workflow en n8n
- [ ] Probar webhook
- [ ] Ver requests en http://localhost:4040

---

## 🐛 Troubleshooting

### Problema: Cloudflared no inicia

```bash
# Verificar logs
sudo journalctl -u cloudflared -f

# Verificar configuración
cloudflared tunnel info v1tr0-n8n

# Re-instalar servicio
sudo cloudflared service uninstall
sudo cloudflared service install

# Reiniciar
sudo systemctl restart cloudflared
```

### Problema: ngrok dice "authtoken not found"

```bash
# Re-configurar token
ngrok config add-authtoken TU_TOKEN

# Verificar config
cat ~/.config/ngrok/ngrok.yml
```

### Problema: Microsoft Graph no valida webhook

```bash
# Verificar que n8n responde correctamente
curl https://n8n.tudominio.com/webhook/test

# En n8n, crear workflow:
Webhook Trigger
  ↓
Function: return [{json: {validationToken: $input.first().json.validationToken}}]
  ↓
Respond to Webhook
```

### Problema: "ERR_TOO_MANY_REDIRECTS"

```bash
# En Cloudflare Dashboard:
# 1. Ir a SSL/TLS
# 2. Cambiar a "Full" (no "Full strict")
# 3. O configurar Origin Certificate
```

---

## 📚 Scripts útiles

### Script para iniciar túnel automáticamente

```bash
# ~/start-tunnel.sh
#!/bin/bash

echo "🚀 Iniciando túnel Cloudflare..."

# Verificar si cloudflared está instalado
if ! command -v cloudflared &> /dev/null; then
    echo "❌ cloudflared no está instalado"
    exit 1
fi

# Iniciar túnel
cloudflared tunnel run v1tr0-n8n &

# Esperar 5 segundos
sleep 5

# Verificar status
if cloudflared tunnel info v1tr0-n8n &> /dev/null; then
    echo "✅ Túnel iniciado correctamente"
    echo "📡 URL: https://n8n.tudominio.com"
else
    echo "❌ Error iniciando túnel"
    exit 1
fi
```

### Script para verificar túnel

```bash
# ~/check-tunnel.sh
#!/bin/bash

URL="https://n8n.tudominio.com"

echo "🔍 Verificando túnel..."
if curl -s -o /dev/null -w "%{http_code}" $URL | grep -q "200\|302"; then
    echo "✅ Túnel activo y funcionando"
else
    echo "❌ Túnel no responde"
fi
```

---

## 🎉 Resultado final

Después de configurar, tendrás:

```
🌐 URL pública HTTPS para n8n:
   https://n8n.tudominio.com

🔗 Webhook URL para Microsoft Graph:
   https://n8n.tudominio.com/webhook/teams-transcription

🎯 Workflows n8n accesibles desde:
   - Microsoft Teams
   - Slack
   - Cualquier servicio externo

🔒 Seguridad:
   - HTTPS automático
   - DDoS protection (Cloudflare)
   - Certificado SSL válido
   - Basic Auth en n8n (admin/admin123)
```

---

**¡Tu n8n local ahora es público y seguro! 🚀**
