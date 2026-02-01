"""
Modelos de Django para el Sistema de Gestión de Proyectos - Maya Guatemala
Basado en el esquema de base de datos PostgreSQL
"""
from django.db import models
from django.utils import timezone
import bcrypt


# =====================================================
# ENUMERADOS (Choices)
# =====================================================

class UserRole(models.TextChoices):
    ADMINISTRADOR = 'administrador', 'Administrador'
    USUARIO = 'usuario', 'Usuario'


class ProjectStatus(models.TextChoices):
    PLANIFICADO = 'planificado', 'Planificado'
    EN_PROGRESO = 'en_progreso', 'En Progreso'
    PAUSADO = 'pausado', 'Pausado'
    COMPLETADO = 'completado', 'Completado'
    CANCELADO = 'cancelado', 'Cancelado'


class PhaseStatus(models.TextChoices):
    PENDIENTE = 'pendiente', 'Pendiente'
    EN_PROGRESO = 'en_progreso', 'En Progreso'
    COMPLETADA = 'completada', 'Completada'
    CANCELADA = 'cancelada', 'Cancelada'


class ActivityType(models.TextChoices):
    ENTREGA = 'entrega', 'Entrega'
    CAPACITACION = 'capacitacion', 'Capacitación'
    INSTALACION = 'instalacion', 'Instalación'
    VISITA = 'visita', 'Visita'
    REUNION = 'reunion', 'Reunión'
    SEGUIMIENTO = 'seguimiento', 'Seguimiento'
    MANTENIMIENTO = 'mantenimiento', 'Mantenimiento'
    EVALUACION = 'evaluacion', 'Evaluación'
    OTRO = 'otro', 'Otro'


class CivilStatus(models.TextChoices):
    SOLTERO = 'soltero', 'Soltero'
    CASADO = 'casado', 'Casado'
    UNIDO = 'unido', 'Unido'
    SEPARADO = 'separado', 'Separado'
    DIVORCIADO = 'divorciado', 'Divorciado'
    VIUDO = 'viudo', 'Viudo'


class Ethnicity(models.TextChoices):
    MAYA = 'maya', 'Maya'
    GARIFUNA = 'garifuna', 'Garifuna'
    XINCA = 'xinca', 'Xinca'
    AFRODESCENDIENTE = 'afrodescendiente', 'Afrodescendiente'
    MESTIZO = 'mestizo', 'Mestizo'
    EXTRANJERO = 'extranjero', 'Extranjero'


class HouseholdType(models.TextChoices):
    UNIPERSONAL_NUCLEAR = 'unipersonal_nuclear', 'Unipersonal/Nuclear'
    EXTENSA = 'extensa', 'Extensa'
    COMPUESTA = 'compuesta', 'Compuesta'
    CO_RESIDENTES = 'co_residentes', 'Co-residentes'


class EducationLevel(models.TextChoices):
    NINGUNO = 'ninguno', 'Ninguno'
    PRIMARIA = 'primaria', 'Primaria'
    BASICO = 'basico', 'Básico'
    DIVERSIFICADO = 'diversificado', 'Diversificado'
    UNIVERSITARIO = 'universitario', 'Universitario'
    OTRO = 'otro', 'Otro'


class SchoolAttendance(models.TextChoices):
    SI = 'si', 'Sí'
    NO = 'no', 'No'
    A_VECES = 'a_veces', 'A veces'


class EducationLanguage(models.TextChoices):
    ESPANOL = 'espanol', 'Español'
    MATERNO = 'materno', 'Materno'
    AMBOS = 'ambos', 'Ambos'
    OTRO = 'otro', 'Otro'


class HousingTenure(models.TextChoices):
    PROPIA = 'propia', 'Propia'
    ALQUILADA = 'alquilada', 'Alquilada'
    CEDIDA_PRESTADA = 'cedida_prestada', 'Cedida/Prestada'
    PROPIEDAD_COMUNAL = 'propiedad_comunal', 'Propiedad Comunal'
    OTRA = 'otra', 'Otra'


class HousingType(models.TextChoices):
    CASA_FORMAL = 'casa_formal', 'Casa Formal'
    APARTAMENTO = 'apartamento', 'Apartamento'
    CUARTO_VECINDAD = 'cuarto_vecindad', 'Cuarto de Vecindad'
    RANCHO = 'rancho', 'Rancho'
    IMPROVISADA = 'improvisada', 'Improvisada'
    COLECTIVA_TEMPORAL = 'colectiva_temporal', 'Colectiva Temporal'
    OTRA = 'otra', 'Otra'


class EconomicStatus(models.TextChoices):
    EMPLEADO = 'empleado', 'Empleado'
    INDEPENDIENTE = 'independiente', 'Independiente'
    EMPRENDEDOR = 'emprendedor', 'Emprendedor'
    AMA_CASA = 'ama_casa', 'Ama de Casa'
    JORNALERO = 'jornalero', 'Jornalero'
    DESEMPLEADO = 'desempleado', 'Desempleado'
    ASPIRANTE = 'aspirante', 'Aspirante'
    SOLO_ESTUDIO = 'solo_estudio', 'Solo Estudio'
    RENTISTA = 'rentista', 'Rentista'
    JUBILADO = 'jubilado', 'Jubilado'
    CUIDADO_PERSONAS = 'cuidado_personas', 'Cuidado de Personas'
    CARGO_COMUNITARIO = 'cargo_comunitario', 'Cargo Comunitario'


# =====================================================
# MODELO DE USUARIO PERSONALIZADO
# =====================================================

class User(models.Model):
    """
    Modelo de usuario personalizado para el sistema.
    Coincide exactamente con el esquema PostgreSQL de BasedeDatos.txt.
    Usa autenticación manual con bcrypt.
    """
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, max_length=100)
    password_hash = models.TextField()  # Contraseña encriptada con bcrypt
    full_name = models.CharField(max_length=150)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USUARIO
    )
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    profile_image_url = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Propiedades para compatibilidad con Django
    @property
    def is_authenticated(self):
        """Siempre retorna True para usuarios autenticados."""
        return True

    @property
    def is_anonymous(self):
        """Siempre retorna False para usuarios no anónimos."""
        return False

    @property
    def is_staff(self):
        """Los administradores tienen acceso al admin de Django."""
        return self.role == UserRole.ADMINISTRADOR

    @property
    def is_superuser(self):
        """Los administradores tienen permisos de superusuario."""
        return self.role == UserRole.ADMINISTRADOR

    def set_password(self, raw_password):
        """
        Encripta la contraseña usando bcrypt y la guarda en password_hash.
        """
        salt = bcrypt.gensalt(rounds=10)
        self.password_hash = bcrypt.hashpw(raw_password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, raw_password):
        """
        Verifica si la contraseña proporcionada coincide con el hash almacenado.
        """
        return bcrypt.checkpw(
            raw_password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

    def is_admin(self):
        """Verifica si el usuario es administrador."""
        return self.role == UserRole.ADMINISTRADOR

    def has_perm(self, perm, obj=None):
        """Los administradores tienen todos los permisos."""
        return self.role == UserRole.ADMINISTRADOR

    def has_module_perms(self, app_label):
        """Los administradores tienen acceso a todos los módulos."""
        return self.role == UserRole.ADMINISTRADOR

    # Atributos requeridos por Django para autenticación
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name']

    class Meta:
        db_table = 'users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.username})"


# =====================================================
# MODELO DE LOGIN LOG
# =====================================================

class LoginLog(models.Model):
    """
    Registro de intentos de inicio de sesión.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='user_id')
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    success = models.BooleanField(default=False)
    failure_reason = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'login_log'
        verbose_name = 'Log de Login'
        verbose_name_plural = 'Logs de Login'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['login_time']),
            models.Index(fields=['success']),
        ]

    def __str__(self):
        return f"{self.user} - {self.login_time}"


# =====================================================
# MODELO DE SESIONES DE USUARIO
# =====================================================

class UserSession(models.Model):
    """
    Sesiones activas de usuarios.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    session_token = models.CharField(max_length=255, unique=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_sessions'
        verbose_name = 'Sesión de Usuario'
        verbose_name_plural = 'Sesiones de Usuarios'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['session_token']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.user} - {self.session_token[:20]}..."

    def is_expired(self):
        """Verifica si la sesión ha expirado."""
        return timezone.now() > self.expires_at


# =====================================================
# MODELO DE PROYECTOS
# =====================================================

class Project(models.Model):
    """
    Proyectos principales de la organización.
    """
    project_name = models.CharField(max_length=250)
    project_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    objectives = models.TextField(blank=True, null=True)
    what_is_done = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    estimated_budget = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    actual_budget = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    cover_image_url = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    municipality = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=ProjectStatus.choices,
        default=ProjectStatus.PLANIFICADO
    )
    has_phases = models.BooleanField(default=False)
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    beneficiaries = models.ManyToManyField(
        'Beneficiary',
        blank=True,
        related_name='projects',
        through='ProjectBeneficiary',
        through_fields=('project', 'beneficiary')
    )
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_projects', db_column='created_by')
    responsible_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='responsible_projects', db_column='responsible_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'projects'
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        indexes = [
            models.Index(fields=['project_code']),
            models.Index(fields=['status']),
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['created_by']),
            models.Index(fields=['responsible_user']),
            models.Index(fields=['municipality']),
            models.Index(fields=['department']),
        ]

    def __str__(self):
        return self.project_name

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError({'end_date': 'La fecha de fin debe ser posterior a la fecha de inicio.'})


# =====================================================
# TABLA INTERMEDIA: PROYECTO-BENEFICIARIOS
# =====================================================

class ProjectBeneficiary(models.Model):
    """
    Relación entre proyectos y beneficiarios.
    Tabla intermedia para la relación ManyToMany.
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, db_column='project_id')
    beneficiary = models.ForeignKey('Beneficiary', on_delete=models.CASCADE, db_column='beneficiary_id')
    assigned_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='created_by')

    class Meta:
        db_table = 'project_beneficiaries'
        unique_together = ('project', 'beneficiary')
        verbose_name = 'Proyecto-Beneficiario'
        verbose_name_plural = 'Proyectos-Beneficiarios'
        indexes = [
            models.Index(fields=['project']),
            models.Index(fields=['beneficiary']),
            models.Index(fields=['assigned_date']),
        ]

    def __str__(self):
        return f"{self.project.project_name} - {self.beneficiary.first_name} {self.beneficiary.last_name}"


# =====================================================
# MODELO DE BENEFICIARIOS
# =====================================================

class Beneficiary(models.Model):
    """
    Información principal de beneficiarios del censo.
    """
    # Ubicación territorial
    department = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    community = models.CharField(max_length=150, blank=True, null=True)
    
    # Información general
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_place = models.CharField(max_length=150, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    cui_dpi = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    civil_status = models.CharField(max_length=20, choices=CivilStatus.choices, blank=True, null=True)
    ethnicity = models.CharField(max_length=20, choices=Ethnicity.choices, blank=True, null=True)
    linguistic_community = models.CharField(max_length=100, blank=True, null=True)
    household_type = models.CharField(max_length=20, choices=HouseholdType.choices, blank=True, null=True)
    
    # Habitantes de la vivienda
    total_household_members = models.IntegerField(default=0)
    male_members = models.IntegerField(default=0)
    female_members = models.IntegerField(default=0)
    
    # Otros datos
    profile_image_url = models.TextField(blank=True, null=True)
    observations = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'beneficiaries'
        verbose_name = 'Beneficiario'
        verbose_name_plural = 'Beneficiarios'
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['cui_dpi']),
            models.Index(fields=['department']),
            models.Index(fields=['municipality']),
            models.Index(fields=['community']),
            models.Index(fields=['birth_date']),
            models.Index(fields=['is_active']),
            models.Index(fields=['created_by']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


# =====================================================
# MODELO DE FASES DE PROYECTOS
# =====================================================

class ProjectPhase(models.Model):
    """
    Fases de los proyectos.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='phases')
    phase_name = models.CharField(max_length=200)
    phase_number = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    objectives = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    budget = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=PhaseStatus.choices,
        default=PhaseStatus.PENDIENTE
    )
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project_phases'
        verbose_name = 'Fase de Proyecto'
        verbose_name_plural = 'Fases de Proyectos'
        indexes = [
            models.Index(fields=['project']),
            models.Index(fields=['status']),
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['project', 'phase_number']),
        ]
        unique_together = ['project', 'phase_number']

    def __str__(self):
        return f"{self.project.project_name} - Fase {self.phase_number}: {self.phase_name}"


# =====================================================
# MODELO DE ACTIVIDADES DIARIAS
# =====================================================

class DailyActivity(models.Model):
    """
    Actividades diarias de los proyectos.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='activities')
    phase = models.ForeignKey(ProjectPhase, on_delete=models.CASCADE, null=True, blank=True, related_name='activities')
    activity_date = models.DateField()
    activity_type = models.CharField(max_length=20, choices=ActivityType.choices)
    description = models.TextField()
    participants_count = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    observations = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'daily_activities'
        verbose_name = 'Actividad Diaria'
        verbose_name_plural = 'Actividades Diarias'
        indexes = [
            models.Index(fields=['project']),
            models.Index(fields=['phase']),
            models.Index(fields=['activity_date']),
            models.Index(fields=['activity_type']),
            models.Index(fields=['created_by']),
        ]

    def __str__(self):
        return f"{self.activity_type} - {self.activity_date}"
