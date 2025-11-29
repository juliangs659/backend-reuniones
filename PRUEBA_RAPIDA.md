# 🚀 Prueba Rápida del CRUD de Usuarios

## 1. Levantar los servicios

```bash
sudo docker compose up -d
```

## 2. Verificar que todo está corriendo

```bash
sudo docker compose ps
```

Deberías ver 4 servicios activos:
- `mongodb` (puerto 27017)
- `redis` (puerto 6379)
- `api` (puerto 8000)
- `mongo-express` (puerto 8081)

## 3. Abrir la documentación interactiva

Abre tu navegador en: **http://localhost:8000/docs**

## 4. Probar los endpoints

### ✅ Crear un usuario (POST)

**Endpoint:** `POST /api/v1/users/`

**Body:**
```json
{
  "email": "juan@example.com",
  "full_name": "Juan Pérez",
  "role": "user",
  "is_active": true
}
```

### ✅ Listar usuarios (GET)

**Endpoint:** `GET /api/v1/users/`

Query params opcionales:
- `skip`: 0 (por defecto)
- `limit`: 10 (por defecto)

### ✅ Obtener un usuario específico (GET)

**Endpoint:** `GET /api/v1/users/{user_id}`

Usa el `id` que te devolvió el POST anterior.

### ✅ Actualizar un usuario (PUT)

**Endpoint:** `PUT /api/v1/users/{user_id}`

**Body:**
```json
{
  "full_name": "Juan Carlos Pérez",
  "role": "admin"
}
```

### ✅ Eliminar un usuario (DELETE)

**Endpoint:** `DELETE /api/v1/users/{user_id}`

## 5. Ver la base de datos

Abre **Mongo Express** en: **http://localhost:8081**

- Verás la base de datos `v1tr0_db`
- Dentro encontrarás la colección `users`
- Puedes ver todos los documentos creados

## 6. Probar con cURL (alternativa)

### Crear usuario:
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "maria@example.com",
    "full_name": "María García",
    "role": "user",
    "is_active": true
  }'
```

### Listar usuarios:
```bash
curl "http://localhost:8000/api/v1/users/"
```

### Obtener usuario por ID:
```bash
curl "http://localhost:8000/api/v1/users/{REEMPLAZA_CON_ID}"
```

### Actualizar usuario:
```bash
curl -X PUT "http://localhost:8000/api/v1/users/{REEMPLAZA_CON_ID}" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "María Fernanda García"
  }'
```

### Eliminar usuario:
```bash
curl -X DELETE "http://localhost:8000/api/v1/users/{REEMPLAZA_CON_ID}"
```

## 7. Ver logs

```bash
# Ver logs de la API
sudo docker compose logs -f api

# Ver logs de MongoDB
sudo docker compose logs -f mongodb
```

## 8. Detener los servicios

```bash
sudo docker compose down
```

## 9. Detener y limpiar todo

```bash
sudo docker compose down -v
```

Esto eliminará también los volúmenes (datos de MongoDB).

---

## 📝 Estructura del CRUD creado

```
app/
├── crud/
│   ├── __init__.py
│   └── user.py          # Lógica CRUD para usuarios
├── api/
│   └── v1/
│       ├── endpoints/
│       │   ├── __init__.py
│       │   └── users.py # Endpoints REST para usuarios
│       └── api.py       # Router principal (incluye /users)
└── schemas/
    └── user.py          # Schemas Pydantic (UserCreate, UserUpdate, UserResponse)
```

## 🎯 Endpoints disponibles

- `POST /api/v1/users/` - Crear usuario
- `GET /api/v1/users/` - Listar usuarios (con paginación)
- `GET /api/v1/users/{user_id}` - Obtener usuario por ID
- `PUT /api/v1/users/{user_id}` - Actualizar usuario
- `DELETE /api/v1/users/{user_id}` - Eliminar usuario

Todos los endpoints están documentados automáticamente en `/docs` (Swagger UI).
