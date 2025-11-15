# 🚀 V1tr0 Backend API - MongoDB

API REST para gestión de proyectos, reuniones y transcripciones con procesamiento de IA.

## ✨ Características

- ✅ **FastAPI** - Framework moderno y de alto rendimiento
- ✅ **MongoDB** - Base de datos NoSQL escalable
- ✅ **Redis** - Cache y sesiones
- ✅ **OpenAI** - Procesamiento y resúmenes de transcripciones
- ✅ **Docker** - Contenedorización completa
- ✅ **Sin autenticación** - Arquitectura simplificada

## 🎯 Funcionalidades

### Gestión de Proyectos
- Crear y administrar proyectos
- Asignar clientes a proyectos
- Seguimiento de progreso y estados

### Reuniones
- Programar reuniones con Jitsi Meet
- Vincular reuniones a proyectos
- Gestión de participantes

### Transcripciones
- Almacenar transcripciones de reuniones
- **Procesamiento con IA** para generar resúmenes
- Análisis y extracción de insights
- Multi-idioma

### Chat con IA
- Interacción con IA sobre proyectos y transcripciones
- Consultas contextuales
- Generación de contenido

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker y Docker Compose instalados
- Nada más! 🎉

### Levantar toda la aplicación

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd backend_v1tr0

# 2. (Opcional) Configurar variables de entorno
cp .env.example .env
# Edita .env y agrega tu OPENAI_API_KEY si lo necesitas

# 3. Levantar todos los servicios con Docker
sudo docker compose up -d

# 4. Ver logs (opcional)
docker compose logs -f api
```

**¡Eso es todo> /home/julian/Documents/back-v1tr0/backend_v1tr0/.dockerignore << 'EOF'
# Git
.git
.gitignore

# Python
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info
dist
build
.venv
venv
env

# IDEs
.vscode
.idea
*.swp
*.swo
*~

# Testing
.pytest_cache
.coverage
htmlcov

# Documentation
*.md
docs/
mkdocs.yml

# Docker
Dockerfile
docker-compose.yml
.dockerignore

# Environment
.env
.env.local
.env.*.local

# Logs
*.log
logs/

# Otros
*.zip
*.tar.gz
.DS_Store
EOF* 🎊

## 📡 Acceso a los Servicios

Una vez levantados los contenedores:

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **API REST** | http://localhost:8000 | Backend principal |
| **Swagger UI** | http://localhost:8000/docs | Documentación interactiva |
| **ReDoc** | http://localhost:8000/redoc | Documentación alternativa |
| **Mongo Express** | http://localhost:8081 | GUI para MongoDB |
| **MongoDB** | mongodb://localhost:27017 | Base de datos |
| **Redis** | redis://localhost:6379 | Cache |

### Credenciales Mongo Express

- **Usuario**: `admin`
- **Contraseña**: `admin123`

## 📊 Estructura de la Base de Datos

### Colecciones MongoDB

```
v1tr0_db/
├── users              # Usuarios del sistema
├── clients            # Clientes
├── projects           # Proyectos
├── meetings           # Reuniones
├── transcriptions     # Transcripciones con resúmenes de IA
└── chat_messages      # Conversaciones con IA
```

## 🔧 Comandos Útiles

### Docker Compose

```bash
# Iniciar todos los servicios
sudo docker compose up -d

# Ver logs de todos los servicios
docker compose logs -f

# Ver logs solo de la API
docker compose logs -f api

# Detener todos los servicios
docker compose down

# Detener y eliminar volúmenes (CUIDADO: borra los datos)
docker compose down -v

# Reconstruir la imagen de la API
docker compose build api

# Reiniciar la API
docker compose restart api

# Ver estado de los servicios
docker compose ps
```

### MongoDB

```bash
# Conectarse a MongoDB
docker exec -it v1tr0_mongodb mongosh

# Comandos dentro de MongoDB:
> use v1tr0_db
> show collections
> db.users.find().pretty()
> db.transcriptions.countDocuments()
```

## 🛠️ Desarrollo Local (sin Docker)

Si prefieres desarrollar sin Docker:

```bash
# 1. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Iniciar MongoDB y Redis localmente
# (Ver sección de instalación local)

# 4. Ejecutar la aplicación
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🗄️ Modelos de Datos

### Transcription (Ejemplo)

```json
{}
  "_id": "ObjectId",
  "text": "Contenido de la transcripción...",
  "language": "es",
  "status": "completed",
  "ai_summary": "Resumen generado por IA...",
  "ai_insights": "Insights extraídos...",
  "model_used": "gpt-4",
  "meeting_id": "ObjectId",
  "project_id": "ObjectId",
  "created_by_id": "ObjectId",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

## 🤖 Integración con OpenAI

Para usar las funcionalidades de IA:

1. Obtén una API Key de [OpenAI](https://platform.openai.com/)
2. Agrégala al archivo `.env`:
   ```env
   OPENAI_API_KEY=sk-tu-api-key-aqui
   ```
3. Reinicia los contenedores:
   ```bash
   docker compose restart api
   ```

## 🔐 Variables de Entorno

Principales variables configurables en `.env`:

```env
# MongoDB
MONGODB_URL=mongodb://mongodb:27017/v1tr0_db
MONGODB_DB=v1tr0_db

# OpenAI
OPENAI_API_KEY=sk-your-key

# Redis
REDIS_URL=redis://redis:6379

# Configuración
ENVIRONMENT=production
LOG_LEVEL=INFO
```

## 📝 API Endpoints (Ejemplos)

### Health Check

```bash
curl http://localhost:8000/health
```

### Crear Usuario

```bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{}'
    "email": "user@example.com",
    "full_name": "Usuario Test"
  }'
```

*Nota: Los endpoints específicos se implementarán según necesidades*

## 🧪 Testing

```bash
# Ejecutar tests
docker compose exec api pytest

# Con cobertura
docker compose exec api pytest --cov=app tests/
```

## 📦 Estructura del Proyecto

```
backend_v1tr0/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── api.py           # Router principal
│   │       └── endpoints/       # Endpoints (a implementar)
│   ├── core/
│   │   ├── config.py            # Configuración
│   │   ├── database.py          # Conexión MongoDB
│   │   └── deps.py              # Dependencias
│   ├── models/                  # Modelos Pydantic
│   └── schemas/                 # Schemas de validación
├── main.py                      # Entry point
├── requirements.txt             # Dependencias Python
├── Dockerfile                   # Imagen Docker
├── docker-compose.yml           # Orquestación
└── .env                         # Variables de entorno
```

## 🐛 Solución de Problemas

### Error: "Cannot connect to the Docker daemon"

```bash
sudo systemctl start docker
sudo usermod -aG docker $USER
newgrp docker
```

### La API no responde

```bash
# Ver logs
docker compose logs api

# Verificar estado
docker compose ps

# Reiniciar
docker compose restart api
```

### MongoDB no inicia

```bash
# Verificar logs
docker compose logs mongodb

# Limpiar volúmenes y reiniciar
docker compose down -v
docker compose up -d
```

## 🚦 Estado del Proyecto

- ✅ Configuración base completada
- ✅ Modelos de datos definidos
- ✅ Docker compose configurado
- 🔨 Endpoints en desarrollo
- 🔨 Tests en desarrollo

## 📄 Licencia

MIT License

---

**Desarrollado con ❤️ usando FastAPI, MongoDB y Docker**
