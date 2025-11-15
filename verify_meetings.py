#!/usr/bin/env python3
from main import app
from app.api.v1.endpoints.meetings import router

routes = [r for r in app.routes if hasattr(r, 'path') and '/meetings' in r.path]

print('✅ API cargada correctamente')
print(f'✅ {len(routes)} rutas de meetings registradas:')
for r in routes:
    methods = ', '.join(r.methods) if hasattr(r, 'methods') else 'N/A'
    print(f'   {methods:20s} {r.path}')
