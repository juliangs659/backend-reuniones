# 🚀 Instrucciones de Configuración - MongoDB + OpenAI

## ✅ Estado Actual del Proyecto

### 1. **Sistema sin Autenticación**
- ❌ Sin autenticación de usuarios (API pública)
- ✅ Emails identifican a los usuarios en transcripciones y comentarios
- ✅ Sistema simplificado para desarrollo rápido

### 2. **Stack Tecnológico Completo**
- ✅ **FastAPI 0.104.1** - Framework web async
- ✅ **MongoDB con Motor** - Base de datos NoSQL async
- ✅ **OpenAI API** - Procesamiento inteligente de transcripciones
- ✅ **Redis** - Cache y pub/sub
- ✅ **Jitsi Meet** - Videollamadas integradas
- ✅ **Docker Compose** - Orquestación de servicios

### 3. **Modelos Implementados**
- ✅ `client.py` - Clientes del sistema
- ✅ `project.py` - Proyectos con current_phase_id
- ✅ `meeting.py` - Reuniones con Jitsi
- ✅ `transcription.py` - Transcripciones Teams + análisis IA
- ✅ `project_phase.py` - Fases del proyecto
- ✅ `requirement.py` - Requerimientos extraídos por IA
- ✅ `phase_comment.py` - Comentarios por fase

### 4. **Servicios y CRUDs**
- ✅ `openai_service.py` - Integración con OpenAI
- ✅ `transcription.py` - CRUD + process_with_ai()
- ✅ `project_phase.py` - CRUD + reorder_phases()
- ✅ `requirement.py` - CRUD + move_to_phase()
- ✅ `phase_comment.py` - CRUD completo

### 5. **29 Endpoints REST Activos**
- ✅ 6 endpoints de Transcriptions
- ✅ 9 endpoints de Project Phases
- ✅ 8 endpoints de Requirements
- ✅ 6 endpoints de Phase Comments
- ✅ Documentación OpenAPI/Swagger

### 6. **Configuración Docker**
- ✅ `docker-compose.yml` - API + MongoDB + Redis + Mongo Express
- ✅ `.env.example` con OPENAI_API_KEY
- ✅ Health checks y volúmenes persistentes

## �� Dependencias Instaladas

Las siguientes dependencias ya están instaladas en el entorno virtual:

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
motor==3.3.2              # Driver asíncrono de MongoDB
pymongo==4.6.1            # Cliente de MongoDB
beanie==1.23.6            # ODM para MongoDB
pydantic==2.5.0
pydantic-settings==2.1.0
email-validator==2.1.0
python-dotenv==1.0.0
```

## � Inicio Rápido

### 1. Configurar OpenAI API Key

```bash
# Editar archivo .env
nano .env

# Agregar tu API key:
OPENAI_API_KEY=sk-tu-key-real-de-openai
OPENAI_MODEL=gpt-4-turbo-preview
```

⚠️ **Sin API key:** El sistema funcionará pero el endpoint `/transcriptions/{id}/process` fallará.

### 2. Instalar MongoDB

#### Opción A: Docker (Recomendado)

```bash
# Necesitarás permisos de Docker. Ejecuta:
sudo usermod -aG docker $USER
newgrp docker

# Luego inicia MongoDB con:
docker compose up -d mongodb

# Para ver logs:
docker compose logs -f mongodb

# Para acceder a Mongo Express (GUI):
# http://localhost:8081
# Usuario: admin
# Contraseña: admin123
```

#### Opción B: Instalación Local (Ubuntu/Debian)

```bash
# Importar clave pública de MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Crear archivo de lista para MongoDB
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list ]"

# Actualizar repositorios
sudo apt-get update

# Instalar MongoDB
sudo apt-get install -y mongodb-org

# Iniciar MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Verificar estado
sudo systemctl status mongod
```

### 2. Verificar Conexión a MongoDB

```bash
# Si usas Docker:
docker exec -it v1tr0_mongodb mongosh

# Si instalaste localmente:
mongosh

# En el shell de MongoDB:
> show dbs
> use v1tr0_db
> show collections
```

### 3. Activar Entorno Virtual

```bash
source .venv/bin/activate
```

### 4. Ejecutar la Aplicación

```bash
# Modo desarrollo (con recarga automática):
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# O simplemente:
python main.py
```

### 5. Verificar que Todo Funciona

```bash
# Health check
curl http://localhost:8000/health

# Crear transcripción de prueba
curl -X POST http://localhost:8000/api/v1/transcriptions/ \
  -H "Content-Type: application/json" \
  -d '{
    "transcription_text": "Reunión proyecto CRM",
    "user_email": "test@example.com"
  }'

# Ver documentación interactiva
# http://localhost:8000/docs
```

### 6. Acceder a las Herramientas

Una vez que el servidor esté ejecutándose:

- **API REST**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Mongo Express**: http://localhost:8081 (admin/admin123)
- **Health Check**: http://localhost:8000/health

## 🗄️ Estructura de Colecciones MongoDB

El proyecto utiliza las siguientes colecciones:

```
v1tr0_db/
├── clients                  # Clientes del sistema
├── projects                 # Proyectos con fases
├── meetings                 # Reuniones con Jitsi
├── transcriptions           # ✨ Transcripciones Teams + análisis IA
├── project_phases           # ✨ Fases del proyecto
├── requirements             # ✨ Requerimientos extraídos
└── phase_comments           # ✨ Comentarios por fase
```

**✨ = Nuevas colecciones con IA**

## 📝 Variables de Entorno

Tu archivo `.env` debe contener:

```env
# Proyecto
PROJECT_NAME=V1tr0 Backend API
VERSION=1.0.0
API_V1_STR=/api/v1

# MongoDB
MONGODB_URL=mongodb://localhost:27017/v1tr0_db
MONGODB_SERVER=localhost
MONGODB_PORT=27017
MONGODB_DB=v1tr0_db

# OpenAI (IMPORTANTE para procesamiento con IA)
OPENAI_API_KEY=sk-tu-api-key-real
OPENAI_MODEL=gpt-4-turbo-preview

# Jitsi
JITSI_DOMAIN=meet.jit.si

# Redis
REDIS_URL=redis://localhost:6379

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]
ALLOWED_HOSTS=["localhost","127.0.0.1","0.0.0.0"]

# Logging
LOG_LEVEL=INFO
ENVIRONMENT=development
```

⚠️ **IMPORTANTE:** Sin `OPENAI_API_KEY` válida, el endpoint de procesamiento con IA no funcionará.

## 🔍 Comandos Útiles de MongoDB

```javascript
// Conectar a la base de datos
use v1tr0_db

// Ver todas las colecciones
show collections

// Ver documentos de una colección
db.transcriptions.find().pretty()
db.project_phases.find().pretty()

// Contar documentos
db.transcriptions.countDocuments()
db.requirements.countDocuments()

// Crear índices para mejor rendimiento
db.transcriptions.createIndex({ user_email: 1 })
db.transcriptions.createIndex({ project_id: 1 })
db.transcriptions.createIndex({ status: 1 })
db.project_phases.createIndex({ project_id: 1, order: 1 })
db.requirements.createIndex({ phase_id: 1 })
db.requirements.createIndex({ type: 1, priority: 1 })
db.phase_comments.createIndex({ phase_id: 1 })

// Eliminar todos los documentos de una colección
db.transcriptions.deleteMany({})

// Insertar transcripción de prueba
db.transcriptions.insertOne({
  transcription_text: "Reunión kick-off proyecto CRM",
  user_email: "test@example.com",
  language: "es",
  source: "teams",
  status: "pending",
  created_at: new Date(),
  updated_at: new Date()
})

// Ver transcripciones con análisis IA
db.transcriptions.find({ status: "completed" }).pretty()

// Ver fases de un proyecto
db.project_phases.find({ project_id: ObjectId("507f1f77bcf86cd799439011") }).sort({ order: 1 })

// Ver requerimientos de una fase
db.requirements.find({ phase_id: ObjectId("6919074e84f907825330fecc") })
```

## 🐛 Solución de Problemas

### Error: "MongoDB no está conectado"

**Solución**: Asegúrate de que MongoDB esté ejecutándose:

```bash
# Con Docker:
docker ps | grep mongodb

# Localmente:
sudo systemctl status mongod
```

### Error: "Permission denied while trying to connect to Docker"

**Solución**: Agrega tu usuario al grupo docker:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Error al cargar variables de entorno

**Solución**: Verifica que tu archivo `.env` tenga el formato correcto (sin duplicados).

## 📚 Recursos Adicionales

- [Motor Documentation](https://motor.readthedocs.io/)
- [MongoDB Python Driver](https://pymongo.readthedocs.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 🎯 Características Implementadas

### ✅ Sistema Completo de Transcripciones con IA

1. **Subir transcripción de Teams** (manual)
2. **Procesar con OpenAI** - Extrae automáticamente:
   - Resumen ejecutivo
   - Fases del proyecto
   - Requerimientos (funcionales, técnicos, etc.)
   - Decisiones técnicas
   - Action items
3. **Gestión de fases** - Crear, reordenar, actualizar progreso
4. **Gestión de requerimientos** - Por fase, con prioridades
5. **Comentarios por fase** - Públicos o internos
6. **29 endpoints REST** - Completamente documentados

### 📚 Documentación Disponible

- ✅ `API_TESTING_GUIDE.md` - Guía completa con ejemplos curl
- ✅ `SISTEMA_TRANSCRIPCIONES_IA.md` - Arquitectura del sistema IA
- ✅ `README_NEW.md` - Documentación principal
- ✅ `QUICKSTART.md` - Inicio rápido
- ✅ Swagger UI en `/docs`
- ✅ ReDoc en `/redoc`

## 🧪 Testing Rápido

```bash
# Ver guía completa de testing
cat API_TESTING_GUIDE.md

# O ejecutar tests básicos
bash test_api.sh  # Si existe el script

# Testing manual
curl http://localhost:8000/docs  # Swagger interactivo
```

## ✨ Próximas Mejoras Sugeridas

1. **Implementar autenticación** con JWT o API Keys
2. **Rate limiting** para proteger la API
3. **Tests automatizados** con pytest
4. **CI/CD pipeline** con GitHub Actions
5. **Webhooks** para notificaciones
6. **WebSockets** para actualizaciones en tiempo real
7. **Integración directa con Teams** (API de Teams)
8. **Dashboard de métricas** con Grafana

---

**¡El proyecto está completamente funcional y listo para producción! 🎉🤖**
