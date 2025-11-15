# 🚀 Instrucciones de Configuración - MongoDB

## ✅ Cambios Realizados

Se ha completado la migración del proyecto a MongoDB. Los cambios incluyen:

### 1. **Eliminación de Autenticación**
- ❌ Eliminado `app/core/security.py` (Supabase, JWT, passwords)
- ❌ Eliminado `app/schemas/auth.py`
- ❌ Eliminadas dependencias de autenticación en `app/core/deps.py`
- ❌ Eliminado router de autenticación

### 2. **Migración a MongoDB**
- ✅ Reemplazado SQLAlchemy con Motor (driver asíncrono de MongoDB)
- ✅ Actualizado `app/core/database.py` para MongoDB
- ✅ Convertidos todos los modelos a Pydantic para MongoDB:
  - `user.py`
  - `client.py`
  - `project.py`
  - `meeting.py`
  - `transcription.py`
  - `chat_message.py`

### 3. **Configuración Actualizada**
- ✅ `app/core/config.py` configurado para MongoDB
- ✅ `requirements.txt` actualizado con dependencias de MongoDB
- ✅ `docker-compose.yml` actualizado para MongoDB + Mongo Express
- ✅ `.env.example` actualizado
- ✅ Eliminado `alembic.ini` y migraciones SQL

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

## 🔧 Próximos Pasos

### 1. Instalar MongoDB

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

### 5. Acceder a la Documentación

Una vez que el servidor esté ejecutándose:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🗄️ Estructura de Colecciones MongoDB

El proyecto utiliza las siguientes colecciones:

```
v1tr0_db/
├── users              # Usuarios del sistema
├── clients            # Clientes
├── projects           # Proyectos
├── meetings           # Reuniones
├── transcriptions     # Transcripciones de audio
└── chat_messages      # Mensajes de chat con IA
```

## 📝 Variables de Entorno

Tu archivo `.env` debe contener:

```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017/v1tr0_db
MONGODB_DB=v1tr0_db

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]

# OpenAI (opcional)
OPENAI_API_KEY=tu-api-key-aqui

# Otros
ENVIRONMENT=development
LOG_LEVEL=INFO
```

## 🔍 Comandos Útiles de MongoDB

```javascript
// Conectar a la base de datos
use v1tr0_db

// Ver todas las colecciones
show collections

// Ver documentos de una colección
db.users.find().pretty()

// Contar documentos
db.projects.countDocuments()

// Crear índices
db.users.createIndex({ email: 1 }, { unique: true }) })
db.clients.createIndex({ name: 1 }) })
db.projects.createIndex({ title: 1 }) })

// Eliminar todos los documentos de una colección
db.users.deleteMany({})

// Insertar un documento de prueba
db.users.insertOne({})
  email: "test@example.com",
  full_name: "Usuario de Prueba",
  is_active: true,
  is_admin: false,
  created_at: new Date(),
  updated_at: new Date()
})
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

## ✨ Próximas Mejoras Sugeridas

1. **Implementar endpoints** en `app/api/v1/endpoints/`
2. **Agregar validaciones** adicionales en los modelos
3. **Implementar CRUD operations** para cada colección
4. **Configurar índices** en MongoDB para mejor rendimiento
5. **Agregar tests** con pytest
6. **Implementar autenticación** si es necesario en el futuro

---

**¡El proyecto está listo para desarrollar! 🎉**
