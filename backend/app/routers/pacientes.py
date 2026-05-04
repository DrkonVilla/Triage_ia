from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from typing import Optional, List

from app.database import get_db
from app.dependencies import EnfermeraDep, CurrentUser
from app.models.paciente import Paciente
from app.models.contacto_emergencia import ContactoEmergencia
from app.schemas.paciente import (
    PacienteCreate, PacienteUpdate, PacienteResponse,
    ContactoEmergenciaCreate, ContactoEmergenciaResponse
)
from app.services.audit_service import audit_log

router = APIRouter(prefix="/api/v1/pacientes", tags=["Pacientes"])

@router.get("/", response_model=List[PacienteResponse])
async def list_pacientes(
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = None,
    search: Optional[str] = Query(None, min_length=2),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0)
):
    """Lista pacientes con búsqueda opcional"""
    query = (
        select(Paciente)
        .options(selectinload(Paciente.contactos_emergencia))
        .where(Paciente.activo == True)
    )
    
    if search:
        query = query.where(
            or_(
                Paciente.dni.ilike(f"%{search}%"),
                Paciente.nombres.ilike(f"%{search}%"),
                Paciente.apellidos.ilike(f"%{search}%")
            )
        )
    
    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    pacientes = result.scalars().all()
    
    return [PacienteResponse.model_validate(p) for p in pacientes]

@router.get("/{paciente_id}", response_model=PacienteResponse)
async def get_paciente(
    paciente_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = None
):
    """Obtiene paciente por ID"""
    result = await db.execute(
        select(Paciente)
        .options(selectinload(Paciente.contactos_emergencia))
        .where(Paciente.id == paciente_id, Paciente.activo == True)
    )
    paciente = result.scalar_one_or_none()
    
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    return PacienteResponse.model_validate(paciente)

@router.get("/dni/{dni}", response_model=PacienteResponse)
async def get_paciente_by_dni(
    dni: str,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = None
):
    """Obtiene paciente por DNI"""
    result = await db.execute(
        select(Paciente)
        .options(selectinload(Paciente.contactos_emergencia))
        .where(Paciente.dni == dni, Paciente.activo == True)
    )
    paciente = result.scalar_one_or_none()
    
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    return PacienteResponse.model_validate(paciente)

@router.post("/", response_model=PacienteResponse, status_code=status.HTTP_201_CREATED)
async def create_paciente(
    paciente_data: PacienteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: EnfermeraDep = None
):
    """Crea nuevo paciente (solo enfermeras)"""
    # Verificar si ya existe
    result = await db.execute(
        select(Paciente).where(Paciente.dni == paciente_data.dni)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un paciente con ese DNI")
    
    # Crear paciente
    paciente = Paciente(**paciente_data.model_dump(exclude={'contactos_emergencia'}))
    db.add(paciente)
    await db.flush()
    
    # Crear contactos de emergencia
    for contacto_data in paciente_data.contactos_emergencia:
        contacto = ContactoEmergencia(
            paciente_id=paciente.id,
            **contacto_data.model_dump()
        )
        db.add(contacto)
    
    await db.commit()

    # Recargar con relaciones para respuesta (evita MissingGreenlet)
    result = await db.execute(
        select(Paciente)
        .options(selectinload(Paciente.contactos_emergencia))
        .where(Paciente.id == paciente.id)
    )
    paciente = result.scalar_one()
    
    # Auditoría
    await audit_log(
        db, current_user.id, "INSERT", "paciente", paciente.id,
        None, paciente_data.model_dump_json()
    )
    
    return PacienteResponse.model_validate(paciente)

@router.put("/{paciente_id}", response_model=PacienteResponse)
async def update_paciente(
    paciente_id: int,
    paciente_data: PacienteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: EnfermeraDep = None
):
    """Actualiza paciente con bloqueo optimista"""
    # Obtener paciente con versión actual
    result = await db.execute(
        select(Paciente)
        .options(selectinload(Paciente.contactos_emergencia))
        .where(Paciente.id == paciente_id, Paciente.activo == True)
    )
    paciente = result.scalar_one_or_none()
    
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Guardar datos anteriores para auditoría
    datos_anteriores = PacienteResponse.model_validate(paciente).model_dump_json()
    version_actual = paciente.version
    
    # Actualizar campos
    update_data = paciente_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(paciente, field, value)
    
    # Incrementar versión (optimistic locking)
    paciente.version += 1
    
    # Ejecutar update con verificación de versión
    result = await db.execute(
        select(Paciente).where(
            Paciente.id == paciente_id,
            Paciente.version == version_actual
        )
    )
    if result.scalar_one_or_none() is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El registro fue modificado por otro usuario. Por favor recargue."
        )
    
    await db.commit()
    result = await db.execute(
        select(Paciente)
        .options(selectinload(Paciente.contactos_emergencia))
        .where(Paciente.id == paciente.id)
    )
    paciente = result.scalar_one()
    
    # Auditoría
    await audit_log(
        db, current_user.id, "UPDATE", "paciente", paciente.id,
        datos_anteriores, PacienteResponse.model_validate(paciente).model_dump_json()
    )
    
    return PacienteResponse.model_validate(paciente)