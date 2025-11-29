# 🚀 Guía de Integración n8n con V1tr0 Backend

## 📋 Índice
1. [¿Qué es n8n?](#qué-es-n8n)
2. [¿Por qué n8n para este proyecto?](#por-qué-n8n)
3. [Configuración inicial](#configuración-inicial)
4. [Workflows recomendados](#workflows-recomendados)
5. [Ejemplos de automatización](#ejemplos)
6. [Integraciones clave](#integraciones)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 ¿Qué es n8n?

**n8n** es una herramienta de automatización de workflows de código abierto que permite:
- Conectar diferentes servicios y APIs
- Automatizar procesos sin código
- Crear flujos visuales con drag & drop
- Ejecutar lógica compleja con JavaScript
- Self-hosted (control total de datos)

**Interfaz visual:** http://localhost:5678 (después de iniciar)

---

## ✅ ¿Por qué n8n para este proyecto?

### Casos de uso perfectos:

1. **🤖 Procesamiento automático de transcripciones**
   - Webhook recibe nueva transcripción
   - Llama automáticamente a `/transcriptions/{id}/process`
   - Envía notificación cuando termina

2. **📧 Notificaciones inteligentes**
   - Email cuando se crea un nuevo requerimiento
   - Slack/Teams cuando cambia el status de una fase
   - Discord cuando hay comentarios internos importantes

3. **🔄 Sincronización con Microsoft Teams**
   - Captura transcripciones de reuniones
   - Crea automáticamente el meeting en la API
   - Procesa con IA y notifica resultados

4. **📊 Reportes automatizados**
   - Genera reporte semanal de progreso
   - Envía dashboard por email
   - Exporta métricas a Google Sheets

5. **⚡ Webhooks personalizados**
   - Integra con sistemas externos
   - Trigger eventos en otras plataformas
   - Flujos de trabajo complejos

---

## 🔧 Configuración inicial

### 1. Iniciar n8n

```bash
# Levantar todos los servicios (incluyendo n8n)
docker-compose up -d

# Verificar que n8n está corriendo
docker ps | grep n8n

# Ver logs de n8n
docker logs -f v1tr0_n8n
```

### 2. Acceder a la interfaz

```
URL: http://localhost:5678
Usuario: admin
Contraseña: admin123
```

### 3. Configurar credenciales

En n8n, ve a **Settings > Credentials** y agrega:

#### a) HTTP Request (para tu API)
```
Name: V1tr0 Backend API
URL: http://api:8000
Authentication: None (por ahora)
```

#### b) OpenAI (si quieres usar directamente)
```
Name: OpenAI GPT-4o-mini
API Key: tu-openai-api-key
Organization ID: (opcional)
```

#### c) Email (para notificaciones)
```
Name: Gmail/SMTP
SMTP Host: smtp.gmail.com
Port: 587
User: tu-email@gmail.com
Password: tu-app-password
```

#### d) Slack/Teams (opcional)
```
Name: Slack Workspace
Webhook URL: tu-webhook-url
```

---

## 🎨 Workflows recomendados

### **Workflow 1: Procesamiento automático de transcripciones**

```
Trigger: Webhook
↓
1. Recibe datos de transcripción
↓
2. HTTP Request: POST /api/v1/transcriptions
   Body: {
     "meeting_id": "{{$json.meeting_id}}",
     "content": "{{$json.content}}",
     "speaker": "{{$json.speaker}}"
   }
↓
3. Esperar 2 segundos
↓
4. HTTP Request: POST /api/v1/transcriptions/{{$json.id}}/process
↓
5. IF: status === "completed"
   ├─ TRUE → Send Email: "Transcripción procesada exitosamente"
   └─ FALSE → Send Email: "Error en procesamiento"
```

**Webhook URL:** `http://localhost:5678/webhook/process-transcription`

---

### **Workflow 2: Notificación de nuevos requerimientos**

```
Trigger: Webhook (desde tu API)
↓
1. Recibe nuevo requerimiento
↓
2. IF: priority === "high"
   ├─ TRUE → Send Slack: "🚨 Nuevo requerimiento ALTA prioridad"
   └─ FALSE → Send Email: "📝 Nuevo requerimiento registrado"
↓
3. HTTP Request: GET /api/v1/requirements/{{$json.id}}
↓
4. Create Google Sheet Row (opcional)
   - ID, Title, Type, Priority, Created At
```

---

### **Workflow 3: Reporte semanal de progreso**

```
Trigger: Cron (Lunes 9:00 AM)
↓
1. HTTP Request: GET /api/v1/projects
↓
2. Loop over projects
   ├─ HTTP Request: GET /api/v1/project-phases?project_id={{$json.id}}
   ├─ Calculate: completion_percentage promedio
   └─ Store in variable
↓
3. Generate HTML Report
↓
4. Send Email con el reporte
```

---

### **Workflow 4: Sincronización con Microsoft Teams**

```
Trigger: Teams Meeting Ended (webhook)
↓
1. HTTP Request: GET Teams Transcription API
↓
2. HTTP Request: POST /api/v1/clients (if needed)
↓
3. HTTP Request: POST /api/v1/projects (if needed)
↓
4. HTTP Request: POST /api/v1/meetings
   Body: {
     "project_id": "{{$json.project_id}}",
     "title": "{{$json.meeting_title}}",
     "date": "{{$json.meeting_date}}"
   }
↓
5. HTTP Request: POST /api/v1/transcriptions
   Body: {
     "meeting_id": "{{$json.meeting_id}}",
     "content": "{{$json.transcription}}",
     "speaker": "Microsoft Teams"
   }
↓
6. HTTP Request: POST /api/v1/transcriptions/{{$json.id}}/process
↓
7. Send Teams Message: "✅ Reunión procesada y documentada"
```

---

## 💡 Ejemplos prácticos

### Ejemplo 1: Crear cliente y proyecto desde formulario

**Trigger:** Webhook Form Submission

```javascript
// Node 1: Webhook (POST)
// URL: http://localhost:5678/webhook/create-client-project

// Node 2: Create Client
// HTTP Request POST to: http://api:8000/api/v1/clients
{
  "name": "{{$json.body.client_name}}",
  "email": "{{$json.body.client_email}}",
  "phone": "{{$json.body.client_phone}}"
}

// Node 3: Create Project
// HTTP Request POST to: http://api:8000/api/v1/projects
{
  "client_id": "{{$node['Create Client'].json.id}}",
  "name": "{{$json.body.project_name}}",
  "description": "{{$json.body.project_description}}"
}

// Node 4: Send Confirmation Email
To: {{$json.body.client_email}}
Subject: "Proyecto {{$json.body.project_name}} creado exitosamente"
Body: "Tu proyecto ha sido registrado con ID: {{$node['Create Project'].json.id}}"
```

---

### Ejemplo 2: Monitor de cambios en fases

**Trigger:** Webhook (llamado desde tu API cuando cambia status)

```javascript
// Node 1: Webhook
// POST http://localhost:5678/webhook/phase-status-changed

// Node 2: Get Phase Details
// HTTP Request GET: http://api:8000/api/v1/project-phases/{{$json.phase_id}}

// Node 3: Conditional Logic
// IF status === "completed"

// Node 4a: Send Celebration Email
To: project_team@company.com
Subject: "🎉 Fase {{$json.name}} completada!"
Body: "La fase ha sido completada con {{$json.completion_percentage}}% de progreso"

// Node 4b: Update External System
// HTTP Request POST: https://your-external-system.com/api/phase-completed
{
  "phase_name": "{{$json.name}}",
  "project_id": "{{$json.project_id}}",
  "completed_at": "{{$json.updated_at}}"
}
```

---

### Ejemplo 3: Procesamiento batch de transcripciones

**Trigger:** Cron (cada hora)

```javascript
// Node 1: Schedule Trigger
// Cron: 0 * * * * (cada hora)

// Node 2: Get Pending Transcriptions
// HTTP Request GET: http://api:8000/api/v1/transcriptions?status=pending

// Node 3: Loop Over Results
// Split In Batches: 5 items

// Node 4: Process Each Transcription
// HTTP Request POST: http://api:8000/api/v1/transcriptions/{{$json.id}}/process

// Node 5: Wait 30 seconds between batches
// Delay: 30000ms

// Node 6: Send Summary Email
To: admin@company.com
Subject: "Batch Processing Complete"
Body: "Procesadas {{$json.total}} transcripciones"
```

---

## 🔌 Integraciones clave

### 1. **Microsoft Teams** (Alta prioridad)

```yaml
Nodos necesarios:
- Microsoft Teams Trigger (Meeting Ended)
- Microsoft Graph API (Get Transcription)
- HTTP Request (to V1tr0 API)
- Microsoft Teams (Send Message)

Configuración:
1. Registrar app en Azure AD
2. Permisos: OnlineMeetings.Read, Chat.ReadWrite
3. Obtener Client ID y Secret
4. Configurar webhook en Teams
```

### 2. **Slack** (notificaciones)

```yaml
Nodos:
- Slack (Send Message)
- Slack (Send File)

Configuración:
1. Crear Slack App
2. Agregar Bot Token Scopes: chat:write, files:write
3. Instalar en workspace
4. Copiar Bot Token
```

### 3. **Google Sheets** (reportes)

```yaml
Nodos:
- Google Sheets (Append Row)
- Google Sheets (Update Row)
- Google Sheets (Get Values)

Uso:
- Dashboard de requerimientos
- Log de transcripciones
- Métricas de proyectos
```

### 4. **Email** (notificaciones universales)

```yaml
Proveedor recomendado: SendGrid o Gmail

Gmail setup:
1. Activar 2FA en cuenta
2. Generar App Password
3. Usar en n8n con SMTP
```

### 5. **Discord** (opcional, equipos dev)

```yaml
Nodos:
- Discord (Send Message)
- Discord Webhook

Uso:
- Notificaciones para desarrolladores
- Logs de errores
- Alertas de sistema
```

---

## 🎯 Webhooks en tu API

Para integrar n8n con tu API, agrega webhooks:

### Opción 1: Agregar en cada endpoint (manual)

```python
# En app/api/v1/endpoints/transcriptions.py
import httpx

async def notify_n8n(event: str, data: dict):
    """Notifica a n8n sobre eventos"""
    n8n_webhook = "http://n8n:5678/webhook/v1tr0-events"
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                n8n_webhook,
                json={"event": event, "data": data},
                timeout=5.0
            )
    except Exception as e:
        print(f"Error notificando n8n: {e}")

# Después de crear transcripción
@router.post("/transcriptions/{transcription_id}/process")
async def process_transcription(...):
    # ... lógica existente ...
    
    # Notificar a n8n
    await notify_n8n("transcription.processed", {
        "id": str(transcription_id),
        "status": result.get("status"),
        "phases_found": len(result.get("phases", []))
    })
```

### Opción 2: Sistema de eventos (recomendado)

```python
# app/core/events.py
from typing import Dict, Any, List, Callable
import httpx

class EventBus:
    def __init__(self):
        self.webhooks: List[str] = []
    
    def register_webhook(self, url: str):
        self.webhooks.append(url)
    
    async def emit(self, event: str, data: Dict[str, Any]):
        for webhook_url in self.webhooks:
            try:
                async with httpx.AsyncClient() as client:
                    await client.post(
                        webhook_url,
                        json={"event": event, "data": data},
                        timeout=5.0
                    )
            except Exception as e:
                print(f"Webhook error: {e}")

# Singleton
event_bus = EventBus()

# En config.py agregar
N8N_WEBHOOK_URL: str = "http://n8n:5678/webhook/v1tr0-events"

# En startup
event_bus.register_webhook(settings.N8N_WEBHOOK_URL)

# Usar en cualquier endpoint
await event_bus.emit("transcription.created", {"id": str(new_transcription.id)})
```

---

## 📊 Monitoreo y logs

### Ver ejecuciones en n8n

```
1. Acceder a: http://localhost:5678/executions
2. Ver workflows ejecutados
3. Revisar datos de entrada/salida
4. Debug de errores
```

### Logs de Docker

```bash
# Ver logs de n8n
docker logs -f v1tr0_n8n

# Ver últimas 100 líneas
docker logs --tail 100 v1tr0_n8n

# Buscar errores
docker logs v1tr0_n8n | grep ERROR
```

---

## 🐛 Troubleshooting

### Problema: n8n no puede conectar con API

**Solución:**
```bash
# Verificar que están en la misma red
docker network inspect backend_v1tr0_v1tr0_network

# Usar nombre del servicio (no localhost)
URL: http://api:8000/api/v1/...
```

### Problema: Webhook no recibe datos

**Solución:**
```bash
# Verificar que n8n está escuchando
curl http://localhost:5678/webhook/test

# Verificar firewall
sudo ufw status

# Test desde dentro del container
docker exec -it v1tr0_api curl http://n8n:5678/webhook/test
```

### Problema: Credenciales no funcionan

**Solución:**
1. Re-crear credencial en n8n
2. Verificar que el servicio externo está activo
3. Revisar API keys y tokens
4. Verificar permisos/scopes

---

## 🚀 Workflows pre-construidos

Puedes importar workflows desde:

1. **n8n Template Library:** https://n8n.io/workflows
2. **GitHub Community:** https://github.com/topics/n8n-workflows
3. **Crear tus propios y exportar como JSON**

---

## 📝 Configuración recomendada

### Variables de entorno en .env

```bash
# n8n Configuration
N8N_WEBHOOK_URL=http://n8n:5678/webhook/v1tr0-events
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=admin123
N8N_ENCRYPTION_KEY=your-random-32-char-key-here
N8N_HOST=0.0.0.0
N8N_PORT=5678
```

### Seguridad

```yaml
Para producción:
1. Cambiar credenciales por defecto
2. Usar HTTPS (con reverse proxy)
3. Configurar autenticación OAuth2
4. Limitar IPs permitidas
5. Rotar encryption key periódicamente
```

---

## 🎯 Próximos pasos

1. **Iniciar n8n:**
   ```bash
   docker-compose up -d n8n
   ```

2. **Acceder a interfaz:**
   ```
   http://localhost:5678
   ```

3. **Crear primer workflow:**
   - Webhook Trigger
   - HTTP Request a tu API
   - Email notification

4. **Explorar integraciones:**
   - Microsoft Teams
   - Slack
   - Google Sheets

5. **Automatizar procesos:**
   - Procesamiento de transcripciones
   - Notificaciones
   - Reportes

---

## 📚 Recursos adicionales

- **Documentación oficial:** https://docs.n8n.io
- **Community Forum:** https://community.n8n.io
- **Video Tutorials:** https://www.youtube.com/@n8n-io
- **Template Library:** https://n8n.io/workflows

---

## ✅ Checklist de implementación

- [ ] Iniciar servicio n8n con docker-compose
- [ ] Acceder a interfaz (localhost:5678)
- [ ] Configurar credenciales (API, Email, etc.)
- [ ] Crear workflow de prueba
- [ ] Configurar webhook en API
- [ ] Probar procesamiento automático
- [ ] Configurar notificaciones
- [ ] Integrar con Microsoft Teams
- [ ] Crear reportes automatizados
- [ ] Documentar workflows personalizados

---

**¡n8n está listo para automatizar tu proyecto! 🚀**
