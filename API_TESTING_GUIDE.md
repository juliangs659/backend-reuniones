# 📚 Guía Completa de Testing - API V1tr0 Backend

## 🚀 Configuración Inicial

### Verificar que la API está corriendo
```bash
curl http://localhost:8000/health
# Respuesta esperada: {"status":"healthy","database":"MongoDB"}
```

### Acceder a la documentación interactiva
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📝 1. TRANSCRIPTIONS - Endpoints de Transcripciones

### 1.1 Crear Transcripción
**Endpoint:** `POST /api/v1/transcriptions/`

**JSON de prueba:**
```json
{
  "transcription_text": "Reunión del proyecto CRM. El cliente requiere un sistema para gestionar contactos, ventas y reportes. Se necesita implementar autenticación con OAuth2, sistema de roles, dashboard analítico con gráficas, exportación a Excel y PDF. Prioridad alta en seguridad y backup automático de datos.",
  "user_email": "julian@example.com",
  "language": "es",
  "source": "teams"
}
```

**Comando curl:**
```bash
curl -X POST http://localhost:8000/api/v1/transcriptions/ \
  -H "Content-Type: application/json" \
  -d '{
    "transcription_text": "Reunión del proyecto CRM. El cliente requiere un sistema para gestionar contactos, ventas y reportes.",
    "user_email": "julian@example.com",
    "language": "es",
    "source": "teams"
  }'
```

**Respuesta esperada:**
```json
{
  "_id": "691906b484f907825330feca",
  "transcription_text": "Reunión del proyecto CRM...",
  "user_email": "julian@example.com",
  "meeting_id": null,
  "project_id": null,
  "language": "es",
  "source": "teams",
  "status": "pending",
  "processed_at": null,
  "error_message": null,
  "ai_analysis": null,
  "ai_model_used": null,
  "created_at": "2025-11-15T23:03:16.066000",
  "updated_at": "2025-11-15T23:03:16.066000"
}
```

---

### 1.2 Listar Transcripciones
**Endpoint:** `GET /api/v1/transcriptions/`

**Con filtros:**
```bash
# Todas las transcripciones
curl http://localhost:8000/api/v1/transcriptions/

# Filtrar por usuario
curl "http://localhost:8000/api/v1/transcriptions/?user_email=julian@example.com"

# Filtrar por status
curl "http://localhost:8000/api/v1/transcriptions/?status=pending"

# Filtrar por proyecto
curl "http://localhost:8000/api/v1/transcriptions/?project_id=507f1f77bcf86cd799439011"

# Skip y Limit para paginación
curl "http://localhost:8000/api/v1/transcriptions/?skip=0&limit=10"
```

---

### 1.3 Obtener Transcripción por ID
**Endpoint:** `GET /api/v1/transcriptions/{transcription_id}`

```bash
curl http://localhost:8000/api/v1/transcriptions/691906b484f907825330feca
```

---

### 1.4 Actualizar Transcripción
**Endpoint:** `PUT /api/v1/transcriptions/{transcription_id}`

**JSON de prueba:**
```json
{
  "transcription_text": "ACTUALIZADO: Reunión CRM con nuevos requerimientos de seguridad y compliance GDPR",
  "status": "pending"
}
```

**Comando curl:**
```bash
curl -X PUT http://localhost:8000/api/v1/transcriptions/691906b484f907825330feca \
  -H "Content-Type: application/json" \
  -d '{
    "transcription_text": "ACTUALIZADO: Reunión CRM con nuevos requerimientos",
    "status": "pending"
  }'
```

---

### 1.5 Procesar Transcripción con IA
**Endpoint:** `POST /api/v1/transcriptions/{transcription_id}/process`

**JSON de prueba:**
```json
{
  "project_context": "Sistema CRM corporativo para empresa de 500+ empleados. Stack: FastAPI, MongoDB, React. Presupuesto: $50,000 USD. Timeline: 6 meses."
}
```

**Comando curl:**
```bash
curl -X POST http://localhost:8000/api/v1/transcriptions/691906b484f907825330feca/process \
  -H "Content-Type: application/json" \
  -d '{
    "project_context": "Sistema CRM corporativo. Stack: FastAPI, MongoDB, React."
  }'
```

**Nota:** ⚠️ Requiere `OPENAI_API_KEY` configurada en `.env`

**Respuesta esperada (con API key configurada):**
```json
{
  "_id": "691906b484f907825330feca",
  "status": "completed",
  "processed_at": "2025-11-15T23:10:00.000000",
  "ai_analysis": {
    "summary": "Reunión para definir sistema CRM...",
    "phases": [
      {
        "name": "Análisis y Diseño",
        "description": "Definición de arquitectura...",
        "estimated_duration": "4 semanas"
      }
    ],
    "requirements": [
      {
        "title": "Sistema de autenticación OAuth2",
        "type": "functional",
        "priority": "high"
      }
    ],
    "technical_decisions": ["FastAPI backend", "MongoDB database"],
    "action_items": ["Crear diagrama de arquitectura"]
  },
  "ai_model_used": "gpt-4-turbo-preview"
}
```

---

### 1.6 Eliminar Transcripción
**Endpoint:** `DELETE /api/v1/transcriptions/{transcription_id}`

```bash
curl -X DELETE http://localhost:8000/api/v1/transcriptions/691906b484f907825330feca
```

**Respuesta:**
```json
{
  "message": "Transcripción eliminada exitosamente"
}
```

---

## 🎯 2. PROJECT PHASES - Endpoints de Fases del Proyecto

### 2.1 Crear Fase
**Endpoint:** `POST /api/v1/project-phases/`

**JSON de prueba:**
```json
{
  "project_id": "507f1f77bcf86cd799439011",
  "name": "Análisis de Requerimientos",
  "description": "Fase inicial del proyecto donde se definen todos los requerimientos funcionales y no funcionales",
  "order": 1,
  "status": "pending",
  "start_date": "2025-11-20T00:00:00",
  "end_date": "2025-12-15T00:00:00"
}
```

**Comando curl:**
```bash
curl -X POST http://localhost:8000/api/v1/project-phases/ \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "507f1f77bcf86cd799439011",
    "name": "Análisis de Requerimientos",
    "description": "Fase inicial del proyecto",
    "order": 1
  }'
```

**Otros ejemplos de fases:**

```json
{
  "project_id": "507f1f77bcf86cd799439011",
  "name": "Diseño de Arquitectura",
  "description": "Diseño del sistema, base de datos y APIs",
  "order": 2
}
```

```json
{
  "project_id": "507f1f77bcf86cd799439011",
  "name": "Desarrollo",
  "description": "Implementación del backend y frontend",
  "order": 3
}
```

```json
{
  "project_id": "507f1f77bcf86cd799439011",
  "name": "Testing y QA",
  "description": "Pruebas unitarias, integración y end-to-end",
  "order": 4
}
```

```json
{
  "project_id": "507f1f77bcf86cd799439011",
  "name": "Deployment",
  "description": "Despliegue a producción y configuración",
  "order": 5
}
```

---

### 2.2 Listar Todas las Fases
**Endpoint:** `GET /api/v1/project-phases/`

```bash
curl http://localhost:8000/api/v1/project-phases/
```

---

### 2.3 Listar Fases por Proyecto
**Endpoint:** `GET /api/v1/project-phases/project/{project_id}`

```bash
curl http://localhost:8000/api/v1/project-phases/project/507f1f77bcf86cd799439011
```

**Respuesta esperada:**
```json
[
  {
    "_id": "6919074e84f907825330fecc",
    "project_id": "507f1f77bcf86cd799439011",
    "name": "Análisis de Requerimientos",
    "order": 1,
    "status": "in_progress",
    "completion_percentage": 75,
    "created_at": "2025-11-15T23:00:00.000000"
  },
  {
    "_id": "6919075984f907825330fecd",
    "name": "Diseño",
    "order": 2,
    "status": "pending",
    "completion_percentage": 0
  }
]
```

---

### 2.4 Obtener Fase por ID
**Endpoint:** `GET /api/v1/project-phases/{phase_id}`

```bash
curl http://localhost:8000/api/v1/project-phases/6919074e84f907825330fecc
```

---

### 2.5 Actualizar Fase
**Endpoint:** `PUT /api/v1/project-phases/{phase_id}`

**JSON de prueba:**
```json
{
  "name": "Análisis y Documentación Completa",
  "description": "ACTUALIZADO: Fase extendida para incluir documentación técnica completa",
  "status": "in_progress"
}
```

```bash
curl -X PUT http://localhost:8000/api/v1/project-phases/6919074e84f907825330fecc \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Análisis y Documentación Completa",
    "description": "Fase extendida"
  }'
```

---

### 2.6 Actualizar Status de Fase
**Endpoint:** `PATCH /api/v1/project-phases/{phase_id}/status`

**Valores válidos:** `pending`, `in_progress`, `completed`, `blocked`

```bash
# Iniciar fase
curl -X PATCH "http://localhost:8000/api/v1/project-phases/6919074e84f907825330fecc/status?status=in_progress"

# Completar fase
curl -X PATCH "http://localhost:8000/api/v1/project-phases/6919074e84f907825330fecc/status?status=completed"

# Bloquear fase
curl -X PATCH "http://localhost:8000/api/v1/project-phases/6919074e84f907825330fecc/status?status=blocked"
```

**Nota:** ✨ Al cambiar a `in_progress` se auto-setea `actual_start_date`. Al cambiar a `completed` se auto-setea `actual_end_date` y `completion_percentage=100`.

---

### 2.7 Actualizar Porcentaje de Completitud
**Endpoint:** `PATCH /api/v1/project-phases/{phase_id}/completion`

```bash
# Actualizar a 25%
curl -X PATCH "http://localhost:8000/api/v1/project-phases/6919074e84f907825330fecc/completion?completion=25"

# Actualizar a 50%
curl -X PATCH "http://localhost:8000/api/v1/project-phases/6919074e84f907825330fecc/completion?completion=50"

# Actualizar a 75%
curl -X PATCH "http://localhost:8000/api/v1/project-phases/6919074e84f907825330fecc/completion?completion=75"

# Completar al 100%
curl -X PATCH "http://localhost:8000/api/v1/project-phases/6919074e84f907825330fecc/completion?completion=100"
```

**Parámetro:** `completion` (entero de 0 a 100)

---

### 2.8 Reordenar Fases
**Endpoint:** `POST /api/v1/project-phases/reorder?project_id={project_id}`

**JSON de prueba:**
```json
{
  "phase_orders": [
    {
      "phase_id": "6919075a84f907825330fece",
      "order": 1
    },
    {
      "phase_id": "6919075984f907825330fecd",
      "order": 2
    },
    {
      "phase_id": "6919074e84f907825330fecc",
      "order": 3
    }
  ]
}
```

**Comando curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/project-phases/reorder?project_id=507f1f77bcf86cd799439011" \
  -H "Content-Type: application/json" \
  -d '{
    "phase_orders": [
      {"phase_id": "6919075a84f907825330fece", "order": 1},
      {"phase_id": "6919075984f907825330fecd", "order": 2},
      {"phase_id": "6919074e84f907825330fecc", "order": 3}
    ]
  }'
```

**Respuesta:**
```json
{
  "message": "Fases reordenadas exitosamente"
}
```

---

### 2.9 Eliminar Fase
**Endpoint:** `DELETE /api/v1/project-phases/{phase_id}`

```bash
curl -X DELETE http://localhost:8000/api/v1/project-phases/6919074e84f907825330fecc
```

**Respuesta:**
```json
{
  "message": "Fase eliminada exitosamente"
}
```

---

## ✅ 3. REQUIREMENTS - Endpoints de Requerimientos

### 3.1 Crear Requerimiento
**Endpoint:** `POST /api/v1/requirements/`

**JSON de prueba:**
```json
{
  "project_id": "507f1f77bcf86cd799439011",
  "phase_id": "6919074e84f907825330fecc",
  "title": "Sistema de autenticación de usuarios",
  "description": "Implementar autenticación con JWT, OAuth2 (Google, GitHub), refresh tokens, roles y permisos. Debe incluir 2FA opcional.",
  "type": "functional",
  "priority": "critical",
  "status": "pending",
  "extracted_by_ai": false
}
```

**Comando curl:**
```bash
curl -X POST http://localhost:8000/api/v1/requirements/ \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "507f1f77bcf86cd799439011",
    "phase_id": "6919074e84f907825330fecc",
    "title": "Sistema de autenticación",
    "description": "JWT + OAuth2",
    "type": "functional",
    "priority": "high"
  }'
```

**Más ejemplos de requerimientos:**

**Requerimiento Funcional:**
```json
{
  "project_id": "507f1f77bcf86cd799439011",
  "phase_id": "6919074e84f907825330fecc",
  "title": "Dashboard de Reportes Analíticos",
  "description": "Dashboard con gráficas interactivas, filtros por fecha, exportación a PDF/Excel",
  "type": "functional",
  "priority": "high"
}
```

**Requerimiento No Funcional:**
```json
{
  "project_id": "507f1f77bcf86cd799439011",
  "phase_id": "6919074e84f907825330fecc",
  "title": "Performance - Tiempo de Respuesta",
  "description": "El sistema debe responder en menos de 200ms para el 95% de las peticiones",
  "type": "non_functional",
  "priority": "medium"
}
```

**Requerimiento Técnico:**
```json
{
  "project_id": "507f1f77bcf86cd799439011",
  "phase_id": "6919075984f907825330fecd",
  "title": "API REST con FastAPI",
  "description": "Endpoints CRUD, documentación OpenAPI, validación con Pydantic, async/await",
  "type": "technical",
  "priority": "critical"
}
```

**Requerimiento de Negocio:**
```json
{
  "project_id": "507f1f77bcf86cd799439011",
  "phase_id": "6919074e84f907825330fecc",
  "title": "Compliance GDPR",
  "description": "Sistema debe cumplir con regulaciones GDPR para protección de datos",
  "type": "business",
  "priority": "critical"
}
```

**Tipos válidos:** `functional`, `non_functional`, `technical`, `business`  
**Prioridades válidas:** `low`, `medium`, `high`, `critical`  
**Status válidos:** `pending`, `in_progress`, `completed`, `blocked`

---

### 3.2 Listar Requerimientos
**Endpoint:** `GET /api/v1/requirements/`

```bash
# Todos los requerimientos
curl http://localhost:8000/api/v1/requirements/

# Filtrar por proyecto
curl "http://localhost:8000/api/v1/requirements/?project_id=507f1f77bcf86cd799439011"

# Filtrar por fase
curl "http://localhost:8000/api/v1/requirements/?phase_id=6919074e84f907825330fecc"

# Filtrar por tipo
curl "http://localhost:8000/api/v1/requirements/?type=functional"

# Filtrar por prioridad
curl "http://localhost:8000/api/v1/requirements/?priority=critical"

# Filtrar por status
curl "http://localhost:8000/api/v1/requirements/?status=in_progress"

# Solo los extraídos por IA
curl "http://localhost:8000/api/v1/requirements/?extracted_by_ai=true"

# Combinación de filtros
curl "http://localhost:8000/api/v1/requirements/?project_id=507f1f77bcf86cd799439011&type=functional&priority=high"
```

---

### 3.3 Listar Requerimientos por Fase
**Endpoint:** `GET /api/v1/requirements/phase/{phase_id}`

```bash
curl http://localhost:8000/api/v1/requirements/phase/6919074e84f907825330fecc
```

**Respuesta esperada:**
```json
[
  {
    "_id": "69190b2cea577a1f0752a72e",
    "project_id": "507f1f77bcf86cd799439011",
    "phase_id": "6919074e84f907825330fecc",
    "title": "Sistema de autenticación",
    "description": "JWT + OAuth2",
    "type": "functional",
    "priority": "high",
    "status": "in_progress",
    "extracted_by_ai": false,
    "user_edited": false
  }
]
```

---

### 3.4 Obtener Requerimiento por ID
**Endpoint:** `GET /api/v1/requirements/{requirement_id}`

```bash
curl http://localhost:8000/api/v1/requirements/69190b2cea577a1f0752a72e
```

---

### 3.5 Actualizar Requerimiento
**Endpoint:** `PUT /api/v1/requirements/{requirement_id}`

**JSON de prueba:**
```json
{
  "title": "Sistema de autenticación completo",
  "description": "ACTUALIZADO: JWT + OAuth2 (Google, GitHub, Microsoft) + 2FA + Password reset + Email verification",
  "priority": "critical",
  "user_edited": true
}
```

```bash
curl -X PUT http://localhost:8000/api/v1/requirements/69190b2cea577a1f0752a72e \
  -H "Content-Type: application/json" \
  -d '{
    "description": "ACTUALIZADO: Sistema completo de autenticación",
    "priority": "critical"
  }'
```

---

### 3.6 Actualizar Status de Requerimiento
**Endpoint:** `PATCH /api/v1/requirements/{requirement_id}/status`

```bash
# Iniciar desarrollo
curl -X PATCH "http://localhost:8000/api/v1/requirements/69190b2cea577a1f0752a72e/status?status=in_progress"

# Completar
curl -X PATCH "http://localhost:8000/api/v1/requirements/69190b2cea577a1f0752a72e/status?status=completed"

# Bloquear
curl -X PATCH "http://localhost:8000/api/v1/requirements/69190b2cea577a1f0752a72e/status?status=blocked"
```

---

### 3.7 Mover Requerimiento a Otra Fase
**Endpoint:** `PATCH /api/v1/requirements/{requirement_id}/move`

```bash
# Mover requerimiento de "Análisis" a "Desarrollo"
curl -X PATCH "http://localhost:8000/api/v1/requirements/69190b2cea577a1f0752a72e/move?new_phase_id=6919075a84f907825330fece"
```

**Respuesta:**
```json
{
  "_id": "69190b2cea577a1f0752a72e",
  "title": "Sistema de autenticación",
  "phase_id": "6919075a84f907825330fece",
  "updated_at": "2025-11-15T23:30:00.000000"
}
```

---

### 3.8 Eliminar Requerimiento
**Endpoint:** `DELETE /api/v1/requirements/{requirement_id}`

```bash
curl -X DELETE http://localhost:8000/api/v1/requirements/69190b2cea577a1f0752a72e
```

**Respuesta:**
```json
{
  "message": "Requerimiento eliminado exitosamente"
}
```

---

## 💬 4. PHASE COMMENTS - Endpoints de Comentarios

### 4.1 Crear Comentario
**Endpoint:** `POST /api/v1/phase-comments/`

**JSON de prueba:**
```json
{
  "phase_id": "6919074e84f907825330fecc",
  "project_id": "507f1f77bcf86cd799439011",
  "user_email": "julian@example.com",
  "comment": "Esta fase va muy bien, pero necesitamos más tiempo para completar las pruebas de integración. Sugiero extender la fecha de entrega 1 semana.",
  "is_internal": false
}
```

**Comando curl:**
```bash
curl -X POST http://localhost:8000/api/v1/phase-comments/ \
  -H "Content-Type: application/json" \
  -d '{
    "phase_id": "6919074e84f907825330fecc",
    "project_id": "507f1f77bcf86cd799439011",
    "user_email": "julian@example.com",
    "comment": "Esta fase va muy bien",
    "is_internal": false
  }'
```

**Comentario Interno (solo para el equipo):**
```json
{
  "phase_id": "6919074e84f907825330fecc",
  "project_id": "507f1f77bcf86cd799439011",
  "user_email": "dev@example.com",
  "comment": "INTERNO: El cliente aún no ha aprobado el presupuesto adicional. No avanzar con features premium hasta confirmación.",
  "is_internal": true
}
```

**Más ejemplos:**

```json
{
  "phase_id": "6919074e84f907825330fecc",
  "project_id": "507f1f77bcf86cd799439011",
  "user_email": "pm@example.com",
  "comment": "Fase completada exitosamente. Cliente muy satisfecho con los resultados.",
  "is_internal": false
}
```

```json
{
  "phase_id": "6919075984f907825330fecd",
  "project_id": "507f1f77bcf86cd799439011",
  "user_email": "client@empresa.com",
  "comment": "¿Podríamos agregar un módulo de reportes personalizados en esta fase?",
  "is_internal": false
}
```

---

### 4.2 Listar Comentarios
**Endpoint:** `GET /api/v1/phase-comments/`

```bash
# Todos los comentarios
curl http://localhost:8000/api/v1/phase-comments/

# Solo comentarios públicos
curl "http://localhost:8000/api/v1/phase-comments/?is_internal=false"

# Solo comentarios internos
curl "http://localhost:8000/api/v1/phase-comments/?is_internal=true"

# Filtrar por proyecto
curl "http://localhost:8000/api/v1/phase-comments/?project_id=507f1f77bcf86cd799439011"

# Filtrar por usuario
curl "http://localhost:8000/api/v1/phase-comments/?user_email=julian@example.com"
```

---

### 4.3 Listar Comentarios por Fase
**Endpoint:** `GET /api/v1/phase-comments/phase/{phase_id}`

```bash
curl http://localhost:8000/api/v1/phase-comments/phase/6919074e84f907825330fecc
```

**Respuesta esperada:**
```json
[
  {
    "_id": "69190bc0ea577a1f0752a730",
    "phase_id": "6919074e84f907825330fecc",
    "project_id": "507f1f77bcf86cd799439011",
    "user_email": "julian@example.com",
    "comment": "Esta fase va muy bien",
    "is_internal": false,
    "created_at": "2025-11-15T23:20:00.000000",
    "updated_at": "2025-11-15T23:20:00.000000"
  },
  {
    "_id": "69190bddea577a1f0752a731",
    "user_email": "dev@example.com",
    "comment": "INTERNO: El cliente no ha aprobado...",
    "is_internal": true
  }
]
```

---

### 4.4 Obtener Comentario por ID
**Endpoint:** `GET /api/v1/phase-comments/{comment_id}`

```bash
curl http://localhost:8000/api/v1/phase-comments/69190bc0ea577a1f0752a730
```

---

### 4.5 Actualizar Comentario
**Endpoint:** `PUT /api/v1/phase-comments/{comment_id}`

**JSON de prueba:**
```json
{
  "comment": "ACTUALIZADO: Esta fase está completada al 90%, solo queda pendiente la documentación técnica y el video tutorial."
}
```

```bash
curl -X PUT http://localhost:8000/api/v1/phase-comments/69190bc0ea577a1f0752a730 \
  -H "Content-Type: application/json" \
  -d '{
    "comment": "ACTUALIZADO: Fase completada al 90%"
  }'
```

---

### 4.6 Eliminar Comentario
**Endpoint:** `DELETE /api/v1/phase-comments/{comment_id}`

```bash
curl -X DELETE http://localhost:8000/api/v1/phase-comments/69190bc0ea577a1f0752a730
```

**Respuesta:**
```json
{
  "message": "Comentario eliminado exitosamente"
}
```

---

## 🔄 5. FLUJO COMPLETO DE TRABAJO

### Escenario: Crear proyecto completo desde una transcripción

```bash
# 1. Crear transcripción de reunión
TRANSCRIPTION_ID=$(curl -s -X POST http://localhost:8000/api/v1/transcriptions/ \
  -H "Content-Type: application/json" \
  -d '{
    "transcription_text": "Reunión kick-off proyecto CRM. El cliente necesita: 1) Sistema de login con Google/GitHub. 2) Dashboard con métricas de ventas. 3) Módulo de contactos con búsqueda avanzada. 4) Exportar reportes a Excel. 5) API REST documentada. 6) Deploy en AWS con CI/CD. Timeline: 4 meses. Presupuesto: $40k USD.",
    "user_email": "pm@example.com",
    "language": "es",
    "source": "teams"
  }' | jq -r '._id')

echo "Transcripción creada: $TRANSCRIPTION_ID"

# 2. Procesar con IA (requiere API key)
curl -X POST "http://localhost:8000/api/v1/transcriptions/$TRANSCRIPTION_ID/process" \
  -H "Content-Type: application/json" \
  -d '{
    "project_context": "CRM empresarial. Stack: FastAPI, React, MongoDB, AWS. Equipo: 3 devs."
  }'

# 3. Crear fases del proyecto
PHASE1=$(curl -s -X POST http://localhost:8000/api/v1/project-phases/ \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "507f1f77bcf86cd799439011",
    "name": "Análisis y Diseño",
    "description": "Definir arquitectura y diseñar base de datos",
    "order": 1
  }' | jq -r '._id')

PHASE2=$(curl -s -X POST http://localhost:8000/api/v1/project-phases/ \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "507f1f77bcf86cd799439011",
    "name": "Desarrollo Backend",
    "description": "Implementar API REST con FastAPI",
    "order": 2
  }' | jq -r '._id')

PHASE3=$(curl -s -X POST http://localhost:8000/api/v1/project-phases/ \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "507f1f77bcf86cd799439011",
    "name": "Desarrollo Frontend",
    "description": "Implementar UI con React",
    "order": 3
  }' | jq -r '._id')

echo "Fases creadas: $PHASE1, $PHASE2, $PHASE3"

# 4. Crear requerimientos para la fase 1
curl -X POST http://localhost:8000/api/v1/requirements/ \
  -H "Content-Type: application/json" \
  -d "{
    \"project_id\": \"507f1f77bcf86cd799439011\",
    \"phase_id\": \"$PHASE1\",
    \"title\": \"Diagrama de arquitectura del sistema\",
    \"description\": \"Crear diagrama completo con: backend, frontend, base de datos, cache, CDN\",
    \"type\": \"technical\",
    \"priority\": \"high\"
  }"

curl -X POST http://localhost:8000/api/v1/requirements/ \
  -H "Content-Type: application/json" \
  -d "{
    \"project_id\": \"507f1f77bcf86cd799439011\",
    \"phase_id\": \"$PHASE1\",
    \"title\": \"Modelo de datos MongoDB\",
    \"description\": \"Definir colecciones: users, contacts, companies, deals, activities\",
    \"type\": \"technical\",
    \"priority\": \"critical\"
  }"

# 5. Iniciar la primera fase
curl -X PATCH "http://localhost:8000/api/v1/project-phases/$PHASE1/status?status=in_progress"

# 6. Actualizar progreso
curl -X PATCH "http://localhost:8000/api/v1/project-phases/$PHASE1/completion?completion=30"

# 7. Agregar comentario del cliente
curl -X POST http://localhost:8000/api/v1/phase-comments/ \
  -H "Content-Type: application/json" \
  -d "{
    \"phase_id\": \"$PHASE1\",
    \"project_id\": \"507f1f77bcf86cd799439011\",
    \"user_email\": \"cliente@empresa.com\",
    \"comment\": \"Excelente avance! Me gustaría revisar el diagrama antes de continuar.\",
    \"is_internal\": false
  }"

# 8. Ver el estado de todo el proyecto
echo "\n=== FASES DEL PROYECTO ==="
curl -s "http://localhost:8000/api/v1/project-phases/project/507f1f77bcf86cd799439011" | jq '.[] | {name: .name, status: .status, completion: .completion_percentage}'

echo "\n=== REQUERIMIENTOS FASE 1 ==="
curl -s "http://localhost:8000/api/v1/requirements/phase/$PHASE1" | jq '.[] | {title: .title, priority: .priority}'

echo "\n=== COMENTARIOS FASE 1 ==="
curl -s "http://localhost:8000/api/v1/phase-comments/phase/$PHASE1" | jq '.[] | {user: .user_email, comment: .comment}'
```

---

## 📊 6. EJEMPLOS DE CONSULTAS AVANZADAS

### Obtener estadísticas del proyecto
```bash
PROJECT_ID="507f1f77bcf86cd799439011"

# Total de fases
echo "Total fases:"
curl -s "http://localhost:8000/api/v1/project-phases/project/$PROJECT_ID" | jq 'length'

# Fases completadas
echo "Fases completadas:"
curl -s "http://localhost:8000/api/v1/project-phases/project/$PROJECT_ID" | jq '[.[] | select(.status == "completed")] | length'

# Progreso promedio
echo "Progreso promedio:"
curl -s "http://localhost:8000/api/v1/project-phases/project/$PROJECT_ID" | jq '[.[].completion_percentage] | add / length'

# Requerimientos críticos pendientes
echo "Requerimientos críticos pendientes:"
curl -s "http://localhost:8000/api/v1/requirements/?project_id=$PROJECT_ID&priority=critical&status=pending" | jq 'length'

# Comentarios recientes
echo "Últimos 5 comentarios:"
curl -s "http://localhost:8000/api/v1/phase-comments/?project_id=$PROJECT_ID" | jq '.[:5] | .[] | {user: .user_email, comment: .comment, date: .created_at}'
```

---

## 🧪 7. SCRIPTS DE TESTING AUTOMATIZADO

### Script Bash para testing completo

Guarda este script como `test_api.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost:8000/api/v1"
PROJECT_ID="507f1f77bcf86cd799439011"

echo "🚀 Iniciando tests de API V1tr0..."

# Test 1: Crear transcripción
echo "\n✅ Test 1: Crear transcripción"
TRANS_ID=$(curl -s -X POST "$BASE_URL/transcriptions/" \
  -H "Content-Type: application/json" \
  -d '{
    "transcription_text": "Test: Reunión proyecto CRM",
    "user_email": "test@example.com"
  }' | jq -r '._id')
echo "Transcripción creada: $TRANS_ID"

# Test 2: Listar transcripciones
echo "\n✅ Test 2: Listar transcripciones"
TRANS_COUNT=$(curl -s "$BASE_URL/transcriptions/" | jq 'length')
echo "Total transcripciones: $TRANS_COUNT"

# Test 3: Crear fase
echo "\n✅ Test 3: Crear fase"
PHASE_ID=$(curl -s -X POST "$BASE_URL/project-phases/" \
  -H "Content-Type: application/json" \
  -d "{
    \"project_id\": \"$PROJECT_ID\",
    \"name\": \"Test Phase\",
    \"order\": 999
  }" | jq -r '._id')
echo "Fase creada: $PHASE_ID"

# Test 4: Actualizar status
echo "\n✅ Test 4: Actualizar status de fase"
curl -s -X PATCH "$BASE_URL/project-phases/$PHASE_ID/status?status=in_progress" | jq '.status'

# Test 5: Crear requerimiento
echo "\n✅ Test 5: Crear requerimiento"
REQ_ID=$(curl -s -X POST "$BASE_URL/requirements/" \
  -H "Content-Type: application/json" \
  -d "{
    \"project_id\": \"$PROJECT_ID\",
    \"phase_id\": \"$PHASE_ID\",
    \"title\": \"Test Requirement\",
    \"type\": \"functional\",
    \"priority\": \"low\"
  }" | jq -r '._id')
echo "Requerimiento creado: $REQ_ID"

# Test 6: Crear comentario
echo "\n✅ Test 6: Crear comentario"
COMM_ID=$(curl -s -X POST "$BASE_URL/phase-comments/" \
  -H "Content-Type: application/json" \
  -d "{
    \"phase_id\": \"$PHASE_ID\",
    \"project_id\": \"$PROJECT_ID\",
    \"user_email\": \"test@example.com\",
    \"comment\": \"Test comment\",
    \"is_internal\": false
  }" | jq -r '._id')
echo "Comentario creado: $COMM_ID"

# Cleanup: Eliminar datos de prueba
echo "\n🧹 Limpiando datos de prueba..."
curl -s -X DELETE "$BASE_URL/transcriptions/$TRANS_ID" > /dev/null
curl -s -X DELETE "$BASE_URL/requirements/$REQ_ID" > /dev/null
curl -s -X DELETE "$BASE_URL/phase-comments/$COMM_ID" > /dev/null
curl -s -X DELETE "$BASE_URL/project-phases/$PHASE_ID" > /dev/null

echo "\n✨ Tests completados exitosamente!"
```

Ejecutar:
```bash
chmod +x test_api.sh
./test_api.sh
```

---

## 🔧 8. TROUBLESHOOTING

### Error: "OpenAI API key no configurada"
**Solución:**
```bash
# Editar .env
nano .env

# Agregar tu API key real
OPENAI_API_KEY=sk-tu-key-real-de-openai

# Reiniciar
sudo docker compose restart api
```

### Error: "Field required"
**Causa:** Falta un campo obligatorio en el JSON  
**Solución:** Verificar que todos los campos marcados como requeridos estén presentes

### Error: "Invalid ObjectId"
**Causa:** El ID proporcionado no es un ObjectId válido de MongoDB  
**Solución:** Verificar que el ID tenga 24 caracteres hexadecimales

### Error: "Not Found (404)"
**Causa:** El recurso no existe en la base de datos  
**Solución:** Verificar que el ID sea correcto usando GET para listar recursos

---

## 📝 9. NOTAS IMPORTANTES

### Tipos de Datos

**Requerimientos - type:**
- `functional`: Funcionalidad del sistema
- `non_functional`: Performance, seguridad, usabilidad
- `technical`: Decisiones técnicas, stack, arquitectura
- `business`: Reglas de negocio, compliance

**Requerimientos - priority:**
- `low`: Baja prioridad, nice-to-have
- `medium`: Prioridad media
- `high`: Alta prioridad, importante
- `critical`: Crítico, bloqueante

**Fases y Requerimientos - status:**
- `pending`: Pendiente de iniciar
- `in_progress`: En progreso
- `completed`: Completado
- `blocked`: Bloqueado por algún impedimento

### Campos Auto-generados
- `_id`: Generado automáticamente por MongoDB
- `created_at`: Timestamp de creación
- `updated_at`: Timestamp de última actualización
- `actual_start_date`: Se setea automáticamente al cambiar status a `in_progress`
- `actual_end_date`: Se setea automáticamente al cambiar status a `completed`

### Validaciones
- Email: Debe ser formato válido `user@domain.com`
- ObjectId: 24 caracteres hexadecimales
- Completion: 0-100 (entero)
- Order: Entero positivo

---

## 🎯 10. ENDPOINTS SUMMARY

| Recurso | Método | Endpoint | Descripción |
|---------|--------|----------|-------------|
| **Transcriptions** |
| | POST | `/transcriptions/` | Crear transcripción |
| | GET | `/transcriptions/` | Listar (con filtros) |
| | GET | `/transcriptions/{id}` | Obtener por ID |
| | PUT | `/transcriptions/{id}` | Actualizar |
| | DELETE | `/transcriptions/{id}` | Eliminar |
| | POST | `/transcriptions/{id}/process` | Procesar con IA |
| **Project Phases** |
| | POST | `/project-phases/` | Crear fase |
| | GET | `/project-phases/` | Listar todas |
| | GET | `/project-phases/project/{project_id}` | Listar por proyecto |
| | GET | `/project-phases/{id}` | Obtener por ID |
| | PUT | `/project-phases/{id}` | Actualizar |
| | DELETE | `/project-phases/{id}` | Eliminar |
| | PATCH | `/project-phases/{id}/status` | Actualizar status |
| | PATCH | `/project-phases/{id}/completion` | Actualizar % |
| | POST | `/project-phases/reorder` | Reordenar fases |
| **Requirements** |
| | POST | `/requirements/` | Crear requerimiento |
| | GET | `/requirements/` | Listar (con filtros) |
| | GET | `/requirements/phase/{phase_id}` | Listar por fase |
| | GET | `/requirements/{id}` | Obtener por ID |
| | PUT | `/requirements/{id}` | Actualizar |
| | DELETE | `/requirements/{id}` | Eliminar |
| | PATCH | `/requirements/{id}/status` | Actualizar status |
| | PATCH | `/requirements/{id}/move` | Mover a fase |
| **Phase Comments** |
| | POST | `/phase-comments/` | Crear comentario |
| | GET | `/phase-comments/` | Listar (con filtros) |
| | GET | `/phase-comments/phase/{phase_id}` | Listar por fase |
| | GET | `/phase-comments/{id}` | Obtener por ID |
| | PUT | `/phase-comments/{id}` | Actualizar |
| | DELETE | `/phase-comments/{id}` | Eliminar |

**Total:** 29 endpoints REST ✅

---

## 📚 Recursos Adicionales

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc  
- **OpenAPI JSON:** http://localhost:8000/api/v1/openapi.json
- **Health Check:** http://localhost:8000/health

---

**Creado:** 2025-11-15  
**Versión API:** v1  
**Backend:** FastAPI + MongoDB + Redis  
**Puerto:** 8000
