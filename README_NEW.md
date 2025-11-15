# V1tr0 Backend API - MongoDB

Backend API para V1tr0 Dashboard construido con FastAPI y MongoDB.

## 🚀 Características

- ✅ **FastAPI** - Framework moderno y rápido
- ✅ **MongoDB** - Base de datos NoSQL con Motor (async driver)
- ✅ **Sin autenticación** - Arquitectura simplificada
- ✅ **Modelos Pydantic** - Validación de datos robusta
- ✅ **OpenAPI/Swagger** - Documentación automática
- ✅ **CORS configurado** - Para desarrollo con frontend

## 📋 Requisitos previos

- Python 3.10 o superior
- MongoDB 5.0 o superior
- pip (gestor de paquetes de Python)

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd backend_v1tr0
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# En Linux/Mac
source venv/bin/activate

# En Windows
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` y configura las variables necesarias:

```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017/v1tr0_db
MONGODB_DB=v1tr0_db

# OpenAI (opcional, para funciones de IA)
OPENAI_API_KEY=tu-api-key-aqui
```

### 5. Instalar y configurar MongoDB

#### En Ubuntu/Debian:

```bash
# Importar clave pública de MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Crear archivo de lista para MongoDB
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

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

#### Con Docker:

```bash
# Ejecutar MongoDB en Docker
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_DATABASE=v1tr0_db \
  -v mongodb_data:/data/db \
  mongo:7.0
```

#### Verificar conexión:

```bash
# Conectar a MongoDB
mongosh

# O con Docker
docker exec -it mongodb mongosh

# En el shell de MongoDB:
show dbs
use v1tr0_db
```

## 🚀 Ejecución

### Modo desarrollo (con recarga automática)

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

O simplemente:

```bash
python main.py
```

### Modo producción

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 Documentación de la API

Una vez que el servidor esté ejecutándose, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## 🏗️ Estructura del proyecto

```
backend_v1tr0/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── api.py              # Router principal
│   │       └── endpoints/          # Endpoints de la API (a implementar)
│   ├── core/
│   │   ├── config.py               # Configuración
│   │   ├── database.py             # Conexión a MongoDB
│   │   └── deps.py                 # Dependencias
│   ├── models/
│   │   ├── base.py                 # Modelo base para MongoDB
│   │   ├── user.py                 # Modelo de usuario
│   │   ├── client.py               # Modelo de cliente
│   │   ├── project.py              # Modelo de proyecto
│   │   ├── meeting.py              # Modelo de reunión
│   │   ├── transcription.py        # Modelo de transcripción
│   │   └── chat_message.py         # Modelo de mensaje de chat
│   └── schemas/
│       └── ...                     # Esquemas Pydantic
├── main.py                         # Punto de entrada
├── requirements.txt                # Dependencias
├── .env.example                    # Ejemplo de variables de entorno
├── docker-compose.yml              # Configuración de Docker
└── README.md                       # Este archivo
```

## 🔌 Endpoints principales

### Health Check

```bash
# Verificar estado de la API
curl http://localhost:8000/health

# Endpoint raíz
curl http://localhost:8000/
```

## 🗄️ Colecciones de MongoDB

El proyecto utiliza las siguientes colecciones:

- `users` - Usuarios del sistema
- `clients` - Clientes
- `projects` - Proyectos
- `meetings` - Reuniones
- `transcriptions` - Transcripciones de audio
- `chat_messages` - Mensajes de chat con IA

## 🔍 Operaciones con MongoDB

### Conectar a MongoDB:

```bash
mongosh mongodb://localhost:27017/v1tr0_db
```

### Comandos útiles:

```javascript
// Ver todas las colecciones
show collections

// Ver documentos de una colección
db.users.find().pretty()

// Contar documentos
db.projects.countDocuments()

// Crear índices (si es necesario)
db.users.createIndex({ email: 1 }, { unique: true })
db.clients.createIndex({ name: 1 })

// Eliminar todos los documentos de una colección
db.users.deleteMany({})
```

## 🐳 Docker

### Ejecutar con Docker Compose:

```bash
# Iniciar todos los servicios
sudo docker compose up -d

# Ver logs
sudo docker compose logs -f

# Detener servicios
sudo docker compose down
```

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=app tests/
```

## 📦 Dependencias principales

- **FastAPI** - Framework web
- **Motor** - Driver asíncrono de MongoDB
- **Pydantic** - Validación de datos
- **Uvicorn** - Servidor ASGI
- **pymongo** - Cliente de MongoDB
- **Beanie** - ODM para MongoDB (opcional)

## 🔐 Seguridad

⚠️ **Nota importante**: Este proyecto NO incluye autenticación. Si necesitas proteger tus endpoints, considera implementar:

- JWT tokens
- OAuth2
- API Keys
- Rate limiting

## 🛠️ Desarrollo

### Formatear código:

```bash
black app/
isort app/
```

### Linting:

```bash
flake8 app/
mypy app/
```

## 📝 Variables de entorno

| Variable | Descripción | Por defecto |
|----------|-------------|-------------|
| `MONGODB_URL` | URL de conexión a MongoDB | `mongodb://localhost:27017/v1tr0_db` |
| `MONGODB_DB` | Nombre de la base de datos | `v1tr0_db` |
| `OPENAI_API_KEY` | API Key de OpenAI | - |
| `BACKEND_CORS_ORIGINS` | Orígenes permitidos para CORS | `http://localhost:3000` |

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

## 📞 Soporte

Si tienes problemas o preguntas, por favor abre un issue en el repositorio.

---

**¡Desarrollado con ❤️ usando FastAPI y MongoDB!**
