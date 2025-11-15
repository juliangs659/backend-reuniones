# 📡 API Endpoints - Documentación Completa

## 🔗 Base URL

```
http://localhost:8000
```

## 📚 Tabla de Contenidos

- [Reuniones (Meetings)](#reuniones-meetings)
- [Proyectos (Projects)](#proyectos-projects) - Por implementar
- [Transcripciones (Transcriptions)](#transcripciones-transcriptions) - Por implementar
- [Clientes (Clients)](#clientes-clients) - Por implementar

---

## 📅 Reuniones (Meetings)

### Base Path: `/api/v1/meetings`

Este es el modelo core del sistema para gestionar reuniones virtuales con Jitsi y transcripciones con IA.

### 1. Crear Reunión

**POST** `/api/v1/meetings/`

**Request Body:**
```json
{
  "title": "Sprint Planning #5",
  "description": "Planificación del próximo sprint",
  "project_id": "507f1f77bcf86cd799439012",
  "scheduled_at": "2024-01-20T15:00:00Z",
  "duration_minutes": 60,
  "status": "scheduled",
  "meeting_type": "planning",
  "location": "Virtual - Jitsi",
  "jitsi_room_name": "v1tr0-planning-abc123",
  "jitsi_room_url": "https://meet.jit.si/v1tr0-planning-abc123",
  "host_id": "507f1f77bcf86cd799439015",
  "participant_ids": [
    "507f1f77bcf86cd799439016",
    "507f1f77bcf86cd799439017"
  ],
  "agenda": [
    "Revisión del sprint anterior",
    "Planificación de tareas",
    "Asignación de responsabilidades"
  ],
  "notes": "Traer el reporte de progreso actualizado",
  "action_items": []
}
```

**Response (201):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Sprint Planning #5",
  "description": "Planificación del próximo sprint",
  "project_id": "507f1f77bcf86cd799439012",
  "scheduled_at": "2024-01-20T15:00:00Z",
  "duration_minutes": 60,
  "status": "scheduled",
  "meeting_type": "planning",
  "location": "Virtual - Jitsi",
  "jitsi_room_name": "v1tr0-planning-abc123",
  "jitsi_room_url": "https://meet.jit.si/v1tr0-planning-abc123",
  "host_id": "507f1f77bcf86cd799439015",
  "participant_ids": [
    "507f1f77bcf86cd799439016",
    "507f1f77bcf86cd799439017"
  ],
  "agenda": [
    "Revisión del sprint anterior",
    "Planificación de tareas",
    "Asignación de responsabilidades"
  ],
  "notes": "Traer el reporte de progreso actualizado",
  "action_items": [],
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/meetings/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sprint Planning #5",
    "description": "Planificación del próximo sprint",
    "scheduled_at": "2024-01-20T15:00:00Z",
    "duration_minutes": 60,
    "jitsi_room_name": "v1tr0-planning-abc123"
  }'
```

---

### 2. Listar Reuniones

**GET** `/api/v1/meetings/`

**Query Parameters:**
- `skip` (opcional): Número de registros a saltar (default: 0)
- `limit` (opcional): Número máximo de registros (default: 10, max: 100)
- `project_id` (opcional): Filtrar por proyecto
- `status` (opcional): Filtrar por estado (scheduled, in_progress, completed, cancelled)

**Response (200):**
```json
{
  "items": [
    {
      "id": "507f1f77bcf86cd799439011",
      "title": "Sprint Planning #5",
      "scheduled_at": "2024-01-20T15:00:00Z",
      "status": "scheduled",
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 10,
  "pages": 1
}
```

**cURL:**
```bash
# Listar todas
curl "http://localhost:8000/api/v1/meetings/"

# Filtrar por proyecto
curl "http://localhost:8000/api/v1/meetings/?project_id=507f1f77bcf86cd799439012"

# Filtrar por estado
curl "http://localhost:8000/api/v1/meetings/?status=scheduled"

# Con paginación
curl "http://localhost:8000/api/v1/meetings/?skip=0&limit=20"
```

---

### 3. Obtener Reunión por ID

**GET** `/api/v1/meetings/{meeting_id}`

**Response (200):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Sprint Planning #5",
  "description": "Planificación del próximo sprint",
  "scheduled_at": "2024-01-20T15:00:00Z",
  "duration_minutes": 60,
  "status": "scheduled",
  "jitsi_room_url": "https://meet.jit.si/v1tr0-planning-abc123",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

**Response (404):**
```json
{
  "detail": "Reunión no encontrada"
}
```

**cURL:**
```bash
curl "http://localhost:8000/api/v1/meetings/507f1f77bcf86cd799439011"
```

---

### 4. Actualizar Reunión

**PUT** `/api/v1/meetings/{meeting_id}`

**Request Body (todos los campos son opcionales):**
```json
{
  "title": "Sprint Planning #5 - Actualizado",
  "scheduled_at": "2024-01-20T16:00:00Z",
  "duration_minutes": 90,
  "status": "in_progress",
  "notes": "Reunión iniciada. Se está grabando.",
  "action_items": [
    "Revisar el backlog actualizado",
    "Definir prioridades del sprint"
  ]
}
```

**Response (200):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Sprint Planning #5 - Actualizado",
  "scheduled_at": "2024-01-20T16:00:00Z",
  "duration_minutes": 90,
  "status": "in_progress",
  "notes": "Reunión iniciada. Se está grabando.",
  "action_items": [
    "Revisar el backlog actualizado",
    "Definir prioridades del sprint"
  ],
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-20T16:00:00Z"
}
```

**cURL:**
```bash
curl -X PUT "http://localhost:8000/api/v1/meetings/507f1f77bcf86cd799439011" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress",
    "notes": "Reunión iniciada"
  }'
```

---

### 5. Eliminar Reunión

**DELETE** `/api/v1/meetings/{meeting_id}`

**Response (200):**
```json
{
  "message": "Reunión eliminada exitosamente"
}
```

**Response (404):**
```json
{
  "detail": "Reunión no encontrada"
}
```

**cURL:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/meetings/507f1f77bcf86cd799439011"
```

---

### 6. Actualizar Estado de Reunión

**PATCH** `/api/v1/meetings/{meeting_id}/status`

**Query Parameters:**
- `status` (requerido): Nuevo estado - `scheduled`, `in_progress`, `completed`, `cancelled`

**Response (200):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Sprint Planning #5",
  "status": "completed",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-20T17:00:00Z"
}
```

**cURL:**
```bash
# Marcar como en progreso
curl -X PATCH "http://localhost:8000/api/v1/meetings/507f1f77bcf86cd799439011/status?status=in_progress"

# Marcar como completada
curl -X PATCH "http://localhost:8000/api/v1/meetings/507f1f77bcf86cd799439011/status?status=completed"

# Cancelar reunión
curl -X PATCH "http://localhost:8000/api/v1/meetings/507f1f77bcf86cd799439011/status?status=cancelled"
```

---

## Estados de Reunión

| Estado | Descripción |
|--------|-------------|
| `scheduled` | Reunión programada (pendiente) |
| `in_progress` | Reunión en curso |
| `completed` | Reunión finalizada |
| `cancelled` | Reunión cancelada |

---

## 📝 Notas Importantes

1. **Sin Autenticación**: Esta API actualmente no requiere autenticación. Todos los endpoints son públicos.

2. **IDs de MongoDB**: Los IDs son ObjectIds de MongoDB (24 caracteres hexadecimales).

3. **Fechas**: Todas las fechas están en formato ISO 8601 (UTC).

4. **Jitsi Integration**: Los campos `jitsi_room_name` y `jitsi_room_url` permiten integración con Jitsi Meet.

5. **CORS**: Configurado para permitir orígenes en `localhost:3000` y `localhost:3001`.

---

## 🚀 Inicio Rápido

```bash
# 1. Levantar servicios
sudo docker compose up -d

# 2. Verificar que la API está corriendo
curl http://localhost:8000/health

# 3. Ver documentación interactiva
# Abrir en navegador: http://localhost:8000/docs

# 4. Crear tu primera reunión
curl -X POST "http://localhost:8000/api/v1/meetings/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi Primera Reunión",
    "scheduled_at": "2024-01-25T10:00:00Z",
    "duration_minutes": 60
  }'
```

---

## � Soporte

Para más información, consulta:
- **Swagger UI**: http://localhost:8000/docs
- **Mongo Express**: http://localhost:8081
- **Código fuente**: `/app/api/v1/endpoints/meetings.py`

### Base Path: `/api/v1/users`

### 1. Crear Usuario

**POST** `/api/v1/users/`

**Request Body:**
```json
{
  "email": "juan.perez@example.com",
  "full_name": "Juan Pérez",
  "role": "user",
  "is_active": true,
  "phone": "+34612345678",
  "avatar_url": "https://example.com/avatar.jpg",
  "preferences": {
    "language": "es",
    "notifications": true
  }
}
```

**Response (201):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "juan.perez@example.com",
  "full_name": "Juan Pérez",
  "role": "user",
  "is_active": true,
  "phone": "+34612345678",
  "avatar_url": "https://example.com/avatar.jpg",
  "preferences": {
    "language": "es",
    "notifications": true
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan.perez@example.com",
    "full_name": "Juan Pérez",
    "role": "user",
    "is_active": true
  }'
```

---

### 2. Listar Usuarios

**GET** `/api/v1/users/`

**Query Parameters:**
- `skip` (opcional): Número de registros a saltar (default: 0)
- `limit` (opcional): Número máximo de registros (default: 10, max: 100)

**Response (200):**
```json
{
  "items": [
    {
      "id": "507f1f77bcf86cd799439011",
      "email": "juan.perez@example.com",
      "full_name": "Juan Pérez",
      "role": "user",
      "is_active": true,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": "507f1f77bcf86cd799439012",
      "email": "maria.garcia@example.com",
      "full_name": "María García",
      "role": "admin",
      "is_active": true,
      "created_at": "2024-01-15T11:00:00Z",
      "updated_at": "2024-01-15T11:00:00Z"
    }
  ],
  "total": 2,
  "page": 1,
  "size": 10,
  "pages": 1
}
```

**cURL:**
```bash
# Listar todos
curl "http://localhost:8000/api/v1/users/"

# Con paginación
curl "http://localhost:8000/api/v1/users/?skip=0&limit=20"
```

---

### 3. Obtener Usuario por ID

**GET** `/api/v1/users/{user_id}`

**Response (200):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "juan.perez@example.com",
  "full_name": "Juan Pérez",
  "role": "user",
  "is_active": true,
  "phone": "+34612345678",
  "avatar_url": "https://example.com/avatar.jpg",
  "preferences": {
    "language": "es",
    "notifications": true
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Response (404):**
```json
{
  "detail": "Usuario no encontrado"
}
```

**cURL:**
```bash
curl "http://localhost:8000/api/v1/users/507f1f77bcf86cd799439011"
```

---

### 4. Actualizar Usuario

**PUT** `/api/v1/users/{user_id}`

**Request Body (todos los campos son opcionales):**
```json
{
  "full_name": "Juan Carlos Pérez",
  "role": "admin",
  "phone": "+34612345679",
  "preferences": {
    "language": "en",
    "notifications": false
  }
}
```

**Response (200):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "juan.perez@example.com",
  "full_name": "Juan Carlos Pérez",
  "role": "admin",
  "is_active": true,
  "phone": "+34612345679",
  "preferences": {
    "language": "en",
    "notifications": false
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T12:00:00Z"
}
```

**cURL:**
```bash
curl -X PUT "http://localhost:8000/api/v1/users/507f1f77bcf86cd799439011" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Juan Carlos Pérez",
    "role": "admin"
  }'
```

---

### 5. Eliminar Usuario

**DELETE** `/api/v1/users/{user_id}`

**Response (200):**
```json
{
  "message": "Usuario eliminado exitosamente"
}
```

**Response (404):**
```json
{
  "detail": "Usuario no encontrado"
}
```

**cURL:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/users/507f1f77bcf86cd799439011"
```

---

## 🏢 Clientes (Clients)

### Base Path: `/api/v1/clients` (Por implementar)

### Estructura del Cliente:

```json
{
  "id": "507f1f77bcf86cd799439011",
  "name": "Acme Corporation",
  "email": "contact@acme.com",
  "phone": "+34912345678",
  "address": "Calle Principal 123",
  "city": "Madrid",
  "country": "España",
  "postal_code": "28001",
  "website": "https://acme.com",
  "industry": "Tecnología",
  "company_size": "50-200",
  "contact_person": "Ana Martínez",
  "contact_position": "CTO",
  "contact_email": "ana.martinez@acme.com",
  "contact_phone": "+34612345678",
  "notes": "Cliente premium con contrato anual",
  "is_active": true,
  "created_by": "507f1f77bcf86cd799439012",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

### Endpoints esperados:
- `POST /api/v1/clients/` - Crear cliente
- `GET /api/v1/clients/` - Listar clientes
- `GET /api/v1/clients/{client_id}` - Obtener cliente
- `PUT /api/v1/clients/{client_id}` - Actualizar cliente
- `DELETE /api/v1/clients/{client_id}` - Eliminar cliente

---

## 📊 Proyectos (Projects)

### Base Path: `/api/v1/projects` (Por implementar)

### Estructura del Proyecto:

```json
{
  "id": "507f1f77bcf86cd799439011",
  "name": "Desarrollo App Móvil",
  "description": "Aplicación móvil para gestión de inventarios",
  "client_id": "507f1f77bcf86cd799439012",
  "status": "in_progress",
  "priority": "high",
  "start_date": "2024-01-01T00:00:00Z",
  "end_date": "2024-06-30T00:00:00Z",
  "budget": 50000.00,
  "currency": "EUR",
  "progress": 45,
  "team_members": [
    "507f1f77bcf86cd799439013",
    "507f1f77bcf86cd799439014"
  ],
  "project_manager_id": "507f1f77bcf86cd799439015",
  "tags": ["mobile", "ios", "android", "inventory"],
  "requirements": [
    "Autenticación de usuarios",
    "Escaneo de códigos QR",
    "Sincronización offline"
  ],
  "deliverables": [
    "App iOS",
    "App Android",
    "Panel de administración web"
  ],
  "is_active": true,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

### Endpoints esperados:
- `POST /api/v1/projects/` - Crear proyecto
- `GET /api/v1/projects/` - Listar proyectos
- `GET /api/v1/projects/{project_id}` - Obtener proyecto
- `PUT /api/v1/projects/{project_id}` - Actualizar proyecto
- `DELETE /api/v1/projects/{project_id}` - Eliminar proyecto
- `GET /api/v1/projects/{project_id}/meetings` - Listar reuniones del proyecto
- `GET /api/v1/projects/{project_id}/transcriptions` - Listar transcripciones del proyecto

---

## 📅 Reuniones (Meetings)

### Base Path: `/api/v1/meetings` (Por implementar)

### Estructura de la Reunión:

```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Revisión Sprint #5",
  "description": "Revisión de progreso y planificación del siguiente sprint",
  "project_id": "507f1f77bcf86cd799439012",
  "scheduled_at": "2024-01-20T15:00:00Z",
  "duration_minutes": 60,
  "status": "scheduled",
  "meeting_type": "sprint_review",
  "location": "Sala de Conferencias A",
  "jitsi_room_name": "v1tr0-meeting-abc123",
  "jitsi_room_url": "https://meet.jit.si/v1tr0-meeting-abc123",
  "host_id": "507f1f77bcf86cd799439013",
  "participant_ids": [
    "507f1f77bcf86cd799439014",
    "507f1f77bcf86cd799439015",
    "507f1f77bcf86cd799439016"
  ],
  "agenda": [
    "Revisión de tareas completadas",
    "Demostración de funcionalidades",
    "Planificación próximo sprint"
  ],
  "notes": "Preparar demo del módulo de reportes",
  "action_items": [
    "Revisar feedback del cliente",
    "Actualizar documentación técnica"
  ],
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

### Endpoints esperados:
- `POST /api/v1/meetings/` - Crear reunión
- `GET /api/v1/meetings/` - Listar reuniones
- `GET /api/v1/meetings/{meeting_id}` - Obtener reunión
- `PUT /api/v1/meetings/{meeting_id}` - Actualizar reunión
- `DELETE /api/v1/meetings/{meeting_id}` - Eliminar reunión
- `GET /api/v1/meetings/{meeting_id}/transcriptions` - Listar transcripciones de la reunión

### Estados de reunión:
- `scheduled` - Programada
- `in_progress` - En curso
- `completed` - Completada
- `cancelled` - Cancelada

---

## 📝 Transcripciones (Transcriptions)

### Base Path: `/api/v1/transcriptions` (Por implementar)

### Estructura de la Transcripción:

```json
{
  "id": "507f1f77bcf86cd799439011",
  "meeting_id": "507f1f77bcf86cd799439012",
  "project_id": "507f1f77bcf86cd799439013",
  "title": "Transcripción - Revisión Sprint #5",
  "text": "Participante 1: Buenos días a todos...\nParticipante 2: Hola, gracias por...",
  "language": "es",
  "duration_seconds": 3600,
  "word_count": 2500,
  "status": "completed",
  "model_used": "whisper-1",
  "confidence_score": 0.95,
  "ai_summary": "Se revisó el progreso del sprint #5. Se completaron 15 de 18 tareas. Se identificaron 3 bloqueadores que requieren atención inmediata.",
  "ai_insights": [
    "El equipo está por encima del 80% de cumplimiento",
    "Se requiere más tiempo para el módulo de reportes",
    "El cliente solicitó cambios en la interfaz de usuario"
  ],
  "speakers": [
    {
      "id": "speaker_1",
      "name": "Juan Pérez",
      "segments": 15
    },
    {
      "id": "speaker_2",
      "name": "María García",
      "segments": 12
    }
  ],
  "segments": [
    {
      "start_time": 0.0,
      "end_time": 5.2,
      "speaker": "speaker_1",
      "text": "Buenos días a todos, comenzamos la reunión.",
      "confidence": 0.96
    }
  ],
  "created_at": "2024-01-20T16:00:00Z",
  "updated_at": "2024-01-20T16:00:00Z"
}
```

### Endpoints esperados:
- `POST /api/v1/transcriptions/` - Crear transcripción
- `POST /api/v1/transcriptions/process` - Procesar con IA
- `GET /api/v1/transcriptions/` - Listar transcripciones
- `GET /api/v1/transcriptions/{transcription_id}` - Obtener transcripción
- `PUT /api/v1/transcriptions/{transcription_id}` - Actualizar transcripción
- `DELETE /api/v1/transcriptions/{transcription_id}` - Eliminar transcripción
- `GET /api/v1/transcriptions/{transcription_id}/summary` - Obtener resumen IA
- `GET /api/v1/transcriptions/{transcription_id}/export` - Exportar (PDF, TXT, DOCX)

### Estados de transcripción:
- `pending` - Pendiente
- `processing` - Procesando
- `completed` - Completada
- `failed` - Fallida

---

## 💬 Mensajes de Chat (Chat Messages)

### Base Path: `/api/v1/chat-messages` (Por implementar)

### Estructura del Mensaje:

```json
{
  "id": "507f1f77bcf86cd799439011",
  "meeting_id": "507f1f77bcf86cd799439012",
  "user_id": "507f1f77bcf86cd799439013",
  "message": "¿Podemos revisar el presupuesto actualizado?",
  "message_type": "text",
  "reply_to": null,
  "attachments": [
    {
      "filename": "presupuesto_v2.pdf",
      "url": "https://storage.example.com/files/presupuesto_v2.pdf",
      "size": 245678,
      "mime_type": "application/pdf"
    }
  ],
  "reactions": [
    {
      "user_id": "507f1f77bcf86cd799439014",
      "emoji": "👍",
      "created_at": "2024-01-20T15:30:00Z"
    }
  ],
  "is_edited": false,
  "is_deleted": false,
  "created_at": "2024-01-20T15:25:00Z",
  "updated_at": "2024-01-20T15:25:00Z"
}
```

### Endpoints esperados:
- `POST /api/v1/chat-messages/` - Enviar mensaje
- `GET /api/v1/chat-messages/` - Listar mensajes
- `GET /api/v1/chat-messages/{message_id}` - Obtener mensaje
- `PUT /api/v1/chat-messages/{message_id}` - Editar mensaje
- `DELETE /api/v1/chat-messages/{message_id}` - Eliminar mensaje
- `POST /api/v1/chat-messages/{message_id}/reactions` - Agregar reacción
- `GET /api/v1/meetings/{meeting_id}/messages` - Mensajes de una reunión

### Tipos de mensaje:
- `text` - Texto simple
- `file` - Archivo adjunto
- `image` - Imagen
- `system` - Mensaje del sistema

---

## 🔧 Utilidades y Endpoints Comunes

### Health Check

**GET** `/health`

**Response (200):**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:00:00Z",
  "version": "1.0.0"
}
```

**cURL:**
```bash
curl "http://localhost:8000/health"
```

---

### Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📋 Códigos de Estado HTTP

| Código | Significado | Descripción |
|--------|-------------|-------------|
| 200 | OK | Petición exitosa |
| 201 | Created | Recurso creado exitosamente |
| 204 | No Content | Petición exitosa sin contenido de respuesta |
| 400 | Bad Request | Datos de entrada inválidos |
| 404 | Not Found | Recurso no encontrado |
| 409 | Conflict | Conflicto (ej: email duplicado) |
| 422 | Unprocessable Entity | Error de validación |
| 500 | Internal Server Error | Error del servidor |

---

## 🧪 Ejemplos de Testing

### Usando cURL

```bash
# 1. Crear un usuario
USER_ID=$(curl -s -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","full_name":"Test User","role":"user","is_active":true}' \
  | jq -r '.id')

# 2. Obtener el usuario creado
curl "http://localhost:8000/api/v1/users/$USER_ID"

# 3. Actualizar el usuario
curl -X PUT "http://localhost:8000/api/v1/users/$USER_ID" \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Test User Updated"}'

# 4. Eliminar el usuario
curl -X DELETE "http://localhost:8000/api/v1/users/$USER_ID"
```

### Usando Python (requests)

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Crear usuario
response = requests.post(
    f"{BASE_URL}/users/",
    json={
        "email": "test@example.com",
        "full_name": "Test User",
        "role": "user",
        "is_active": True
    }
)
user = response.json()
user_id = user["id"]

# Obtener usuario
response = requests.get(f"{BASE_URL}/users/{user_id}")
print(response.json())

# Actualizar usuario
response = requests.put(
    f"{BASE_URL}/users/{user_id}",
    json={"full_name": "Test User Updated"}
)
print(response.json())

# Listar usuarios
response = requests.get(f"{BASE_URL}/users/", params={"skip": 0, "limit": 10})
print(response.json())

# Eliminar usuario
response = requests.delete(f"{BASE_URL}/users/{user_id}")
print(response.json())
```

### Usando JavaScript (fetch)

```javascript
const BASE_URL = "http://localhost:8000/api/v1";

// Crear usuario
const createUser = async () => {
  const response = await fetch(`${BASE_URL}/users/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: "test@example.com",
      full_name: "Test User",
      role: "user",
      is_active: true,
    }),
  });
  const user = await response.json();
  return user.id;
};

// Obtener usuario
const getUser = async (userId) => {
  const response = await fetch(`${BASE_URL}/users/${userId}`);
  const user = await response.json();
  console.log(user);
};

// Actualizar usuario
const updateUser = async (userId) => {
  const response = await fetch(`${BASE_URL}/users/${userId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      full_name: "Test User Updated",
    }),
  });
  const user = await response.json();
  console.log(user);
};

// Eliminar usuario
const deleteUser = async (userId) => {
  const response = await fetch(`${BASE_URL}/users/${userId}`, {
    method: "DELETE",
  });
  const result = await response.json();
  console.log(result);
};

// Uso
(async () => {
  const userId = await createUser();
  await getUser(userId);
  await updateUser(userId);
  await deleteUser(userId);
})();
```

---

## 📌 Notas Importantes

1. **Sin Autenticación**: Esta API actualmente no requiere autenticación. Todos los endpoints son públicos.

2. **Paginación**: Los endpoints de listado soportan paginación con `skip` y `limit`.

3. **Validación**: Todos los datos son validados usando Pydantic schemas.

4. **IDs de MongoDB**: Los IDs son ObjectIds de MongoDB (24 caracteres hexadecimales).

5. **Fechas**: Todas las fechas están en formato ISO 8601 (UTC).

6. **CORS**: Configurado para permitir orígenes en `localhost:3000` y `localhost:3001`.

---

## 🚀 Inicio Rápido

```bash
# 1. Levantar servicios
sudo docker compose up -d

# 2. Verificar que la API está corriendo
curl http://localhost:8000/health

# 3. Ver documentación interactiva
# Abrir en navegador: http://localhost:8000/docs

# 4. Crear tu primer usuario
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "mi.email@example.com",
    "full_name": "Mi Nombre",
    "role": "user",
    "is_active": true
  }'
```

---

## 📞 Soporte

Para más información, consulta:
- **Swagger UI**: http://localhost:8000/docs
- **Mongo Express**: http://localhost:8081
- **Código fuente**: `/app/api/v1/endpoints/`
