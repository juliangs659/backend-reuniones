# ⚡ Inicio Rápido - V1tr0 Backend con IA

## 🚀 Levantar Todo con Docker

```bash
# 1. Configurar OpenAI (IMPORTANTE)
cp .env.example .env
nano .env  # Agregar tu OPENAI_API_KEY

# 2. Dar permisos a Docker (solo la primera vez)
sudo usermod -aG docker $USER
newgrp docker

# 3. Levantar todos los servicios
sudo docker compose up -d

# 4. Ver el progreso
docker compose logs -f api
```

## ✅ Verificar que todo funciona

```bash
# Estado de los servicios
docker compose ps

# Debe mostrar:
# ✅ v1tr0_api       - Puerto 8000
# ✅ v1tr0_mongodb   - Puerto 27017
# ✅ v1tr0_redis     - Puerto 6379
# ✅ v1tr0_mongo-express - Puerto 8081

# Probar la API
curl http://localhost:8000/health
# Respuesta: {"status":"healthy","database":"MongoDB"}

# Ver documentación
# http://localhost:8000/docs
```

## 📡 URLs Disponibles

- **API REST**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Mongo Express**: http://localhost:8081 (admin/admin123)

## 🧪 Probar Endpoints

```bash
# Crear transcripción
curl -X POST http://localhost:8000/api/v1/transcriptions/ \
  -H "Content-Type: application/json" \
  -d '{
    "transcription_text": "Reunión proyecto CRM. Necesitamos autenticación y dashboard.",
    "user_email": "test@example.com"
  }'

# Listar transcripciones
curl http://localhost:8000/api/v1/transcriptions/

# Ver todas las fases de un proyecto
curl http://localhost:8000/api/v1/project-phases/project/507f1f77bcf86cd799439011
```

📚 **Guía completa de testing:** [API_TESTING_GUIDE.md](API_TESTING_GUIDE.md)

## 🛑 Detener Todo

```bash
docker compose down
```

## 🔄 Actualizar y Reiniciar

```bash
# Si cambias código
docker compose build api
docker compose restart api

# Ver logs
docker compose logs -f api
```

## ⚡ Procesar con IA (requiere API key)

```bash
# 1. Crear transcripción
TRANS_ID=$(curl -s -X POST http://localhost:8000/api/v1/transcriptions/ \
  -H "Content-Type: application/json" \
  -d '{"transcription_text":"Reunión CRM...","user_email":"test@example.com"}' \
  | jq -r '._id')

# 2. Procesar con IA
curl -X POST "http://localhost:8000/api/v1/transcriptions/$TRANS_ID/process" \
  -H "Content-Type: application/json" \
  -d '{"project_context":"Sistema CRM corporativo"}'

# La IA extraerá automáticamente:
# ✅ Fases del proyecto
# ✅ Requerimientos (funcionales, técnicos, etc.)
# ✅ Decisiones técnicas
# ✅ Action items
```

## 💡 Tips

- La API se reconstruye automáticamente al hacer cambios
- MongoDB persiste los datos en un volumen Docker
- Redis se usa para cache (opcional)
- Sin OPENAI_API_KEY el sistema funciona pero sin procesamiento IA
- Para borrar todo: `docker compose down -v` (¡CUIDADO!)

## 🐛 Troubleshooting

**API no inicia:**
```bash
sudo docker logs v1tr0_api
# Si dice "OpenAI API key no configurada" es normal
# Solo afecta el endpoint /process
```

**MongoDB no conecta:**
```bash
docker compose restart mongodb
docker compose logs mongodb
```

**Limpiar y reiniciar:**
```bash
docker compose down
docker compose up -d --build
```

---

**¡Eso es todo! Simple, rápido y con IA. 🎉🤖**
