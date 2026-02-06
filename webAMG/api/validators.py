"""
Validadores de input usando Pydantic para las APIs del sistema WebAMG.
Proporcionan validación robusta y tipado de datos.
"""
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator, constr
from webAMG.api.exceptions import ValidationError


class BaseRequestModel(BaseModel):
    """
    Modelo base para requests de API.
    Proporciona validación y serialización comunes.
    """
    
    model_config = {
        'extra': 'forbid',
        'str_strip_whitespace': True
    }


class LoginRequest(BaseRequestModel):
    """
    Modelo de request para login.
    Valida credenciales de autenticación.
    """
    username: constr(min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_\-\.@]+$')
    password: constr(min_length=6, max_length=128)


class CreateUserRequest(BaseRequestModel):
    """
    Modelo de request para crear usuario.
    Valida todos los campos requeridos.
    """
    username: constr(
        min_length=3,
        max_length=30,
        pattern=r'^[a-zA-Z0-9_-]+$'
    )
    email: str
    password: constr(min_length=8, max_length=128)
    full_name: constr(min_length=2, max_length=100)
    role: Optional[str] = 'usuario'
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Email inválido')
        return v.lower().strip()
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        allowed_roles = ['administrador', 'usuario']
        if v not in allowed_roles:
            raise ValueError(f'Rol debe ser uno de: {", ".join(allowed_roles)}')
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError('La contraseña debe tener al menos una mayúscula')
        if not any(c.islower() for c in v):
            raise ValueError('La contraseña debe tener al menos una minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('La contraseña debe tener al menos un número')
        return v


class UpdateUserRequest(BaseRequestModel):
    """
    Modelo de request para actualizar usuario.
    Todos los campos son opcionales.
    """
    email: Optional[str] = None
    full_name: Optional[constr(min_length=2, max_length=100)] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Email inválido')
        return v.lower().strip()
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        allowed_roles = ['administrador', 'usuario']
        if v not in allowed_roles:
            raise ValueError(f'Rol debe ser uno de: {", ".join(allowed_roles)}')
        return v


class ProjectCreateRequest(BaseRequestModel):
    """
    Modelo de request para crear proyecto.
    """
    name: constr(min_length=3, max_length=200)
    description: Optional[str] = None
    location: Optional[str] = None
    budget: Optional[float] = Field(default=None, ge=0)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = 'planificado'
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        allowed_statuses = ['planificado', 'en_progreso', 'pausado', 'completado', 'cancelado']
        if v not in allowed_statuses:
            raise ValueError(f'Estado debe ser uno de: {", ".join(allowed_statuses)}')
        return v
    
    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v: Optional[date], info) -> Optional[date]:
        if v:
            values = info.data
            if 'start_date' in values and values['start_date']:
                if v < values['start_date']:
                    raise ValueError('La fecha de fin debe ser posterior a la fecha de inicio')
        return v


class ProjectUpdateRequest(BaseRequestModel):
    """
    Modelo de request para actualizar proyecto.
    """
    name: Optional[constr(min_length=3, max_length=200)] = None
    description: Optional[str] = None
    location: Optional[str] = None
    budget: Optional[float] = Field(default=None, ge=0)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        allowed_statuses = ['planificado', 'en_progreso', 'pausado', 'completado', 'cancelado']
        if v not in allowed_statuses:
            raise ValueError(f'Estado debe ser uno de: {", ".join(allowed_statuses)}')
        return v
    
    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v: Optional[date], info) -> Optional[date]:
        if v:
            values = info.data
            if 'start_date' in values and values['start_date']:
                if v < values['start_date']:
                    raise ValueError('La fecha de fin debe ser posterior a la fecha de inicio')
        return v


class BeneficiaryCreateRequest(BaseRequestModel):
    """
    Modelo de request para crear beneficiario.
    """
    full_name: constr(min_length=2, max_length=200)
    dpi: Optional[constr(min_length=13, max_length=13, pattern=r'^\d{13}$')] = None
    phone: Optional[constr(pattern=r'^\+502\d{8}$|^\d{8}$')] = None
    address: Optional[str] = None
    community: Optional[str] = None
    municipality: Optional[str] = None
    department: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    civil_status: Optional[str] = None
    ethnicity: Optional[str] = None
    education_level: Optional[str] = None
    occupation: Optional[str] = None
    monthly_income: Optional[float] = Field(default=None, ge=0)
    family_members: Optional[int] = Field(default=None, ge=0)
    
    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        allowed_genders = ['masculino', 'femenino']
        if v not in allowed_genders:
            raise ValueError(f'Género debe ser uno de: {", ".join(allowed_genders)}')
        return v


class BaseResponseModel(BaseModel):
    """
    Modelo base para respuestas de API.
    """
    success: bool = True
    message: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now())


class ErrorResponseModel(BaseModel):
    """
    Modelo de respuesta para errores.
    """
    success: bool = False
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now())


class SuccessResponseModel(BaseResponseModel):
    """
    Modelo de respuesta exitosa con datos.
    """
    data: Optional[Dict[str, Any]] = None


class PaginatedResponseModel(BaseResponseModel):
    """
    Modelo de respuesta con paginación.
    """
    items: List[Dict[str, Any]]
    pagination: Dict[str, Any]
    
    @classmethod
    def create(
        cls,
        items: List[Dict[str, Any]],
        page: int,
        page_size: int,
        total: int
    ):
        total_pages = (total + page_size - 1) // page_size
        return cls(
            items=items,
            pagination={
                'page': page,
                'page_size': page_size,
                'total': total,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        )


class APIResponse:
    """
    Clase helper para crear respuestas de API consistentes.
    """
    
    @staticmethod
    def success(
        data: Optional[Dict[str, Any]] = None,
        message: Optional[str] = None,
        status_code: int = 200
    ) -> Dict[str, Any]:
        """
        Crea una respuesta exitosa.
        
        Args:
            data: Datos a incluir en la respuesta
            message: Mensaje de éxito
            status_code: Código HTTP (para documentation purposes)
        
        Returns:
            Diccionario con respuesta exitosa
        """
        response = {
            'success': True,
            'timestamp': datetime.now().isoformat()
        }
        
        if message:
            response['message'] = message
        if data:
            response['data'] = data
        
        return response
    
    @staticmethod
    def error(
        error: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = 400
    ) -> Dict[str, Any]:
        """
        Crea una respuesta de error.
        
        Args:
            error: Código de error
            message: Mensaje de error
            details: Detalles adicionales del error
            status_code: Código HTTP (para documentation purposes)
        
        Returns:
            Diccionario con respuesta de error
        """
        response = {
            'success': False,
            'error': error,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        
        if details:
            response['details'] = details
        
        return response
    
    @staticmethod
    def paginated(
        items: List[Dict[str, Any]],
        page: int,
        page_size: int,
        total: int,
        message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Crea una respuesta paginada.
        
        Args:
            items: Lista de items
            page: Número de página actual
            page_size: Tamaño de página
            total: Total de items
            message: Mensaje opcional
        
        Returns:
            Diccionario con respuesta paginada
        """
        total_pages = (total + page_size - 1) // page_size
        
        response = {
            'success': True,
            'items': items,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total': total,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            },
            'timestamp': datetime.now().isoformat()
        }
        
        if message:
            response['message'] = message
        
        return response


def validate_request_data(
    data: Dict[str, Any],
    model_class: type
) -> BaseModel:
    """
    Valida datos de request usando un modelo Pydantic.
    
    Args:
        data: Diccionario de datos a validar
        model_class: Clase de modelo Pydantic
    
    Returns:
        Instancia del modelo validada
    
    Raises:
        ValidationError: Si la validación falla
    """
    try:
        return model_class(**data)
    except Exception as e:
        from pydantic import ValidationError as PydanticValidationError
        
        if isinstance(e, PydanticValidationError):
            errors = {}
            for error in e.errors():
                field = '.'.join(str(loc) for loc in error['loc'])
                errors[field] = error['msg']
        else:
            errors = {'general': str(e)}
        
        raise ValidationError(
            "Validación de request fallida",
            details={'validation_errors': errors}
        )
