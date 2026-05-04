
### `docs/arquitectura.md`
```markdown
# Arquitectura del Sistema

## Diagrama de Componentes

[Incluir el diagrama Mermaid de la Fase 1]

## Decisiones Técnicas

### Concurrencia Optimista
- Campo `version` en tablas mutables
- UPDATE con verificación WHERE version = X
- HTTP 409 Conflict si falla

### Roles y Permisos
- JWT con claims de rol
- Dependencias FastAPI para verificación

### Integración IA
- Fallback a triaje manual (YELLOW) si LLM falla
- Prompts médicos con reglas Manchester