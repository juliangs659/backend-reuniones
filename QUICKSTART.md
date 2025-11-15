# ⚡ Inicio Rápido - V1tr0 Backend

## 🚀 Levantar Todo con Docker

```bash
# 1. Dar permisos a Docker (solo la primera vez)
sudo usermod -aG docker $USER
newgrp docker

# 2. Levantar todos los servicios
sudo docker compose up -d

# 3. Ver el progreso
docker compose logs -f
```

## ✅ Verificar que todo funciona

```bash
# Estado de los servicios
docker compose ps

# Probar la API
curl http://localhost:8000/health

# O abre en el navegador:
# http://localhost:8000/docs
```

## 📡 URLs Disponibles

- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **Mongo Express**: http://localhost:8081 (admin/admin123)

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

## 💡 Tips

- La API se reconstruye automáticamente al hacer cambios
- MongoDB persiste los datos en un volumen
- Para borrar todo: `docker compose down -v` (¡CUIDADO!)

---

**¡Eso es todo! Simple y rápido. 🎉**
