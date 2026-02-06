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


class InvoiceType(models.TextChoices):
    FACTURA = 'factura', 'Factura'
    RECIBO = 'recibo', 'Recibo'
    NOTA_DEBITO = 'nota_debito', 'Nota de Débito'
    NOTA_CREDITO = 'nota_credito', 'Nota de Crédito'
    ORDEN_COMPRA = 'orden_compra', 'Orden de Compra'
    COMPROBANTE_PAGO = 'comprobante_pago', 'Comprobante de Pago'
    CHEQUE = 'cheque', 'Cheque'
    TRANSFERENCIA = 'transferencia', 'Transferencia'
    OTRO = 'otro', 'Otro'


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
        if raw_password is None:
            return False
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

# =====================================================
# MODELO DE AUDITORÍA
# =====================================================

class AuditLog(models.Model):
    """
    Registro de auditoría de todas las operaciones en la base de datos.
    """
    table_name = models.CharField(max_length=100, db_index=True)
    operation = models.CharField(max_length=10, db_index=True)
    old_data = models.JSONField(blank=True, null=True)
    new_data = models.JSONField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='user_id')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    performed_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'audit_log'
        verbose_name = 'Log de Auditoría'
        verbose_name_plural = 'Logs de Auditoría'
        indexes = [
            models.Index(fields=['table_name']),
            models.Index(fields=['operation']),
            models.Index(fields=['user']),
            models.Index(fields=['performed_at']),
        ]

    def __str__(self):
        return f"{self.operation} on {self.table_name} at {self.performed_at}"


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
    actual_end_date = models.DateField(blank=True, null=True)
    estimated_budget = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    actual_budget = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    cover_image_url = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    municipality = models.CharField(max_length=100, blank=True, null=True)
    community = models.CharField(max_length=150, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=ProjectStatus.choices,
        default=ProjectStatus.PLANIFICADO
    )
    has_phases = models.BooleanField(default=False)
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    deactivated_at = models.DateTimeField(blank=True, null=True)
    beneficiaries = models.ManyToManyField(
        'Beneficiary',
        blank=True,
        related_name='projects',
        through='ProjectBeneficiary',
        through_fields=('project', 'beneficiary')
    )
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_projects', db_column='created_by')
    responsible_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='responsible_projects', db_column='responsible_user')
    notes = models.TextField(blank=True, null=True)
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
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.project_name
    
    def delete(self, *args, **kwargs):
        """
        Sobreescribir delete para eliminar también las imágenes físicas.
        """
        import os
        from django.conf import settings
        
        # Eliminar imagen de portada
        if self.cover_image_url:
            cover_path = os.path.join(settings.MEDIA_ROOT, self.cover_image_url)
            if os.path.exists(cover_path):
                try:
                    os.remove(cover_path)
                    print(f"Imagen de portada eliminada: {cover_path}")
                except Exception as e:
                    print(f"Error al eliminar imagen de portada {cover_path}: {e}")
        
        # Eliminar todas las fotos de evidencias asociadas
        for evidence in self.evidences.all():
            for photo in evidence.photos.all():
                if photo.photo_url:
                    photo_path = os.path.join(settings.MEDIA_ROOT, photo.photo_url)
                    if os.path.exists(photo_path):
                        try:
                            os.remove(photo_path)
                            print(f"Foto de evidencia eliminada: {photo_path}")
                        except Exception as e:
                            print(f"Error al eliminar foto de evidencia {photo_path}: {e}")
        
        # Llamar al método delete original
        super().delete(*args, **kwargs)

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
    assigned_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='created_by')

    class Meta:
        db_table = 'project_beneficiaries'
        unique_together = ('project', 'beneficiary')
        verbose_name = 'Proyecto-Beneficiario'
        verbose_name_plural = 'Proyectos-Beneficiarios'
        indexes = [
            models.Index(fields=['project']),
            models.Index(fields=['beneficiary']),
            models.Index(fields=['assigned_at']),
            models.Index(fields=['is_active']),
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
    dpi_image_url = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    civil_status = models.CharField(max_length=20, choices=CivilStatus.choices, blank=True, null=True)
    ethnicity = models.CharField(max_length=20, choices=Ethnicity.choices, blank=True, null=True)
    linguistic_community = models.CharField(max_length=100, blank=True, null=True)
    household_type = models.CharField(max_length=20, choices=HouseholdType.choices, blank=True, null=True)
    
    # Habitantes de la vivienda
    total_household_members = models.IntegerField(default=0)
    male_members = models.IntegerField(default=0)
    female_members = models.IntegerField(default=0)
    
    # Contacto
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile_phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    
    # Control
    notes = models.TextField(blank=True, null=True)
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
# MODELO DE SALUD DE BENEFICIARIOS
# =====================================================

class BeneficiaryHealth(models.Model):
    """
    Información de salud de beneficiarios.
    """
    beneficiary = models.OneToOneField(Beneficiary, on_delete=models.CASCADE, db_column='beneficiary_id', primary_key=True, related_name='health')
    
    # Maternidad
    is_pregnant = models.BooleanField(default=False)
    is_breastfeeding = models.BooleanField(default=False)
    
    # Enfermedades crónicas
    has_diabetes = models.BooleanField(default=False)
    has_high_blood_pressure = models.BooleanField(default=False)
    has_low_blood_pressure = models.BooleanField(default=False)
    has_heart_disease = models.BooleanField(default=False)
    has_kidney_disease = models.BooleanField(default=False)
    has_cancer = models.BooleanField(default=False)
    has_respiratory_disease = models.BooleanField(default=False)
    
    # Discapacidades
    has_language_disability = models.BooleanField(default=False)
    has_hearing_disability = models.BooleanField(default=False)
    has_visual_disability = models.BooleanField(default=False)
    has_physical_disability = models.BooleanField(default=False)
    has_intellectual_disability = models.BooleanField(default=False)
    has_psychosocial_disability = models.BooleanField(default=False)
    
    health_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'beneficiary_health'
        verbose_name = 'Salud de Beneficiario'
        verbose_name_plural = 'Salud de Beneficiarios'
        indexes = [
            models.Index(fields=['beneficiary']),
        ]


# =====================================================
# MODELO DE EDUCACIÓN DE BENEFICIARIOS
# =====================================================

class BeneficiaryEducation(models.Model):
    """
    Información educativa de beneficiarios.
    """
    beneficiary = models.OneToOneField(Beneficiary, on_delete=models.CASCADE, db_column='beneficiary_id', primary_key=True, related_name='education')
    
    education_level = models.CharField(max_length=20, choices=EducationLevel.choices, blank=True, null=True)
    school_attendance = models.CharField(max_length=20, choices=SchoolAttendance.choices, blank=True, null=True)
    education_language = models.CharField(max_length=20, choices=EducationLanguage.choices, blank=True, null=True)
    can_read_write = models.BooleanField(blank=True, null=True)
    years_of_study = models.IntegerField(default=0)
    current_grade = models.CharField(max_length=50, blank=True, null=True)
    school_name = models.CharField(max_length=200, blank=True, null=True)
    
    # Tecnología
    has_cellphone = models.BooleanField(default=False)
    has_computer = models.BooleanField(default=False)
    has_internet = models.BooleanField(default=False)
    
    education_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'beneficiary_education'
        verbose_name = 'Educación de Beneficiario'
        verbose_name_plural = 'Educación de Beneficiarios'
        indexes = [
            models.Index(fields=['beneficiary']),
        ]


# =====================================================
# MODELO DE VIVIENDA DE BENEFICIARIOS
# =====================================================

class BeneficiaryHousing(models.Model):
    """
    Información de vivienda de beneficiarios.
    """
    beneficiary = models.OneToOneField(Beneficiary, on_delete=models.CASCADE, db_column='beneficiary_id', primary_key=True, related_name='housing')
    
    housing_tenure = models.CharField(max_length=20, choices=HousingTenure.choices, blank=True, null=True)
    housing_type = models.CharField(max_length=20, choices=HousingType.choices, blank=True, null=True)
    number_of_rooms = models.IntegerField(blank=True, null=True)
    
    # Materiales
    floor_material = models.CharField(max_length=100, blank=True, null=True)
    wall_material = models.CharField(max_length=100, blank=True, null=True)
    roof_material = models.CharField(max_length=100, blank=True, null=True)
    
    # Servicios básicos
    has_electricity = models.BooleanField(default=False)
    has_piped_water = models.BooleanField(default=False)
    has_sewage = models.BooleanField(default=False)
    
    # Agua
    water_source = models.CharField(max_length=100, blank=True, null=True)
    drinking_water_source = models.CharField(max_length=100, blank=True, null=True)
    
    # Saneamiento
    toilet_type = models.CharField(max_length=100, blank=True, null=True)
    waste_disposal = models.CharField(max_length=100, blank=True, null=True)
    
    housing_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'beneficiary_housing'
        verbose_name = 'Vivienda de Beneficiario'
        verbose_name_plural = 'Vivienda de Beneficiarios'
        indexes = [
            models.Index(fields=['beneficiary']),
        ]


# =====================================================
# MODELO DE ECONOMÍA DE BENEFICIARIOS
# =====================================================

class BeneficiaryEconomy(models.Model):
    """
    Información económica de beneficiarios.
    """
    beneficiary = models.OneToOneField(Beneficiary, on_delete=models.CASCADE, db_column='beneficiary_id', primary_key=True, related_name='economy')
    
    # Actividades económicas
    economically_active_employed = models.BooleanField(default=False)
    economically_active_independent = models.BooleanField(default=False)
    economically_active_entrepreneur = models.BooleanField(default=False)
    economically_active_day_laborer = models.BooleanField(default=False)
    homemaker = models.BooleanField(default=False)
    unemployed = models.BooleanField(default=False)
    job_seeker = models.BooleanField(default=False)
    student_only = models.BooleanField(default=False)
    pensioner_rentier = models.BooleanField(default=False)
    retired = models.BooleanField(default=False)
    caregiver = models.BooleanField(default=False)
    community_position = models.BooleanField(default=False)
    
    # Ingresos y ayudas
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    receives_social_aid = models.BooleanField(default=False)
    social_aid_type = models.CharField(max_length=200, blank=True, null=True)
    
    occupation = models.CharField(max_length=150, blank=True, null=True)
    workplace = models.CharField(max_length=200, blank=True, null=True)
    
    economy_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'beneficiary_economy'
        verbose_name = 'Economía de Beneficiario'
        verbose_name_plural = 'Economía de Beneficiarios'
        indexes = [
            models.Index(fields=['beneficiary']),
        ]


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
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    actual_end_date = models.DateField(blank=True, null=True)
    estimated_budget = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    actual_budget = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=PhaseStatus.choices,
        default=PhaseStatus.PENDIENTE
    )
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
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
            models.Index(fields=['is_active']),
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
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
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
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.activity_type} - {self.activity_date}"


# =====================================================
# MODELO DE FOTOS DE ACTIVIDADES
# =====================================================

class ActivityPhoto(models.Model):
    """
    Fotos de actividades diarias.
    """
    activity = models.ForeignKey(DailyActivity, on_delete=models.CASCADE, related_name='photos')
    photo_url = models.TextField()
    caption = models.TextField(blank=True, null=True)
    photo_order = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='uploaded_by')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'activity_photos'
        verbose_name = 'Foto de Actividad'
        verbose_name_plural = 'Fotos de Actividades'
        indexes = [
            models.Index(fields=['activity']),
            models.Index(fields=['uploaded_by']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"Foto {self.photo_order} - {self.activity}"


# =====================================================
# MODELO DE EVIDENCIAS DE PROYECTOS
# =====================================================

class ProjectEvidence(models.Model):
    """
    Evidencias de proyectos con rangos de fechas, descripción, fotos y checklist de requerimientos.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='evidences')
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    requirements = models.JSONField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project_evidences'
        verbose_name = 'Evidencia de Proyecto'
        verbose_name_plural = 'Evidencias de Proyectos'
        indexes = [
            models.Index(fields=['project']),
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['created_by']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.project.project_name} - {self.start_date} a {self.end_date}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.end_date < self.start_date:
            raise ValidationError({'end_date': 'La fecha de fin debe ser posterior o igual a la fecha de inicio.'})


class EvidencePhoto(models.Model):
    """
    Fotos asociadas a las evidencias de proyectos.
    """
    evidence = models.ForeignKey(ProjectEvidence, on_delete=models.CASCADE, related_name='photos')
    photo_url = models.TextField()
    caption = models.TextField(blank=True, null=True)
    photo_order = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='uploaded_by')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'evidence_photos'
        verbose_name = 'Foto de Evidencia'
        verbose_name_plural = 'Fotos de Evidencias'
        indexes = [
            models.Index(fields=['evidence']),
            models.Index(fields=['uploaded_by']),
            models.Index(fields=['uploaded_at']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"Foto {self.photo_order} - {self.evidence}"


# =====================================================
# RELACIÓN EVIDENCIA-BENEFICIARIOS
# =====================================================

class EvidenceBeneficiary(models.Model):
    """
    Relación entre evidencias y beneficiarios participantes.
    """
    evidence = models.ForeignKey(ProjectEvidence, on_delete=models.CASCADE, related_name='beneficiaries')
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='evidence_participations')
    assigned_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'evidence_beneficiaries'
        verbose_name = 'Beneficiario de Evidencia'
        verbose_name_plural = 'Beneficiarios de Evidencias'
        indexes = [
            models.Index(fields=['evidence']),
            models.Index(fields=['beneficiary']),
            models.Index(fields=['assigned_at']),
            models.Index(fields=['is_active']),
        ]
        unique_together = ['evidence', 'beneficiary']

    def __str__(self):
        return f"{self.beneficiary.full_name} - {self.evidence}"


# =====================================================
# RELACIÓN FASE-BENEFICIARIOS
# =====================================================

class PhaseBeneficiary(models.Model):
    """
    Relación entre fases y beneficiarios asignados.
    """
    phase = models.ForeignKey(ProjectPhase, on_delete=models.CASCADE, related_name='beneficiaries')
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='phase_participations')
    assigned_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='created_by')

    class Meta:
        db_table = 'phase_beneficiaries'
        verbose_name = 'Beneficiario de Fase'
        verbose_name_plural = 'Beneficiarios de Fases'
        indexes = [
            models.Index(fields=['phase']),
            models.Index(fields=['beneficiary']),
            models.Index(fields=['assigned_at']),
            models.Index(fields=['is_active']),
        ]
        unique_together = ['phase', 'beneficiary']

    def __str__(self):
        return f"{self.beneficiary.full_name} - {self.phase}"


# =====================================================
# MODELO DE EVIDENCIAS DE FASES
# =====================================================

class PhaseEvidence(models.Model):
    """
    Evidencias de fases de proyectos con rangos de fechas, descripción, fotos y checklist de requerimientos.
    """
    phase = models.ForeignKey(ProjectPhase, on_delete=models.CASCADE, related_name='evidences')
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    requirements = models.JSONField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'phase_evidences'
        verbose_name = 'Evidencia de Fase'
        verbose_name_plural = 'Evidencias de Fases'
        indexes = [
            models.Index(fields=['phase']),
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['created_by']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.phase} - {self.start_date} a {self.end_date}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.end_date < self.start_date:
            raise ValidationError({'end_date': 'La fecha de fin debe ser posterior o igual a la fecha de inicio.'})


class PhaseEvidencePhoto(models.Model):
    """
    Fotos asociadas a las evidencias de fases.
    """
    phase_evidence = models.ForeignKey(PhaseEvidence, on_delete=models.CASCADE, related_name='photos')
    photo_url = models.TextField()
    caption = models.TextField(blank=True, null=True)
    photo_order = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='uploaded_by')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'phase_evidence_photos'
        verbose_name = 'Foto de Evidencia de Fase'
        verbose_name_plural = 'Fotos de Evidencias de Fases'
        indexes = [
            models.Index(fields=['phase_evidence']),
            models.Index(fields=['uploaded_by']),
            models.Index(fields=['uploaded_at']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"Foto {self.photo_order} - {self.phase_evidence}"


class PhaseEvidenceBeneficiary(models.Model):
    """
    Relación entre evidencias de fases y beneficiarios participantes.
    """
    phase_evidence = models.ForeignKey(PhaseEvidence, on_delete=models.CASCADE, related_name='beneficiaries')
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='phase_evidence_participations')
    assigned_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'phase_evidence_beneficiaries'
        verbose_name = 'Beneficiario de Evidencia de Fase'
        verbose_name_plural = 'Beneficiarios de Evidencias de Fases'
        indexes = [
            models.Index(fields=['phase_evidence']),
            models.Index(fields=['beneficiary']),
            models.Index(fields=['assigned_at']),
            models.Index(fields=['is_active']),
        ]
        unique_together = ['phase_evidence', 'beneficiary']

    def __str__(self):
        return f"{self.beneficiary.full_name} - {self.phase_evidence}"


# =====================================================
# MODELO DE MATERIALES DE PROYECTOS
# =====================================================

class ProjectMaterial(models.Model):
    """
    Materiales utilizados en proyectos.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='materials')
    material_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50, blank=True, null=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_cost = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    supplier = models.CharField(max_length=200, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project_materials'
        verbose_name = 'Material de Proyecto'
        verbose_name_plural = 'Materiales de Proyectos'
        indexes = [
            models.Index(fields=['project']),
            models.Index(fields=['purchase_date']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.material_name} - {self.project.project_name}"


# =====================================================
# MODELO DE EJECUCIÓN PRESUPUESTARIA
# =====================================================

class BudgetExecution(models.Model):
    """
    Ejecución presupuestaria de proyectos y fases - Registro de gastos y facturas.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='budget_executions', db_column='project_id')
    phase = models.ForeignKey(ProjectPhase, on_delete=models.CASCADE, null=True, blank=True, related_name='budget_executions', db_column='phase_id')
    
    # Información del documento
    invoice_type = models.CharField(max_length=20, choices=InvoiceType.choices)
    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    invoice_date = models.DateField()
    invoice_name = models.CharField(max_length=200)
    
    # Montos
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=15, decimal_places=2)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Descripción y categoría
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True, null=True)
    supplier_name = models.CharField(max_length=200, blank=True, null=True)
    
    # Documentos adjuntos
    invoice_document_url = models.TextField(blank=True, null=True)
    additional_documents_urls = models.JSONField(blank=True, null=True)
    
    # Información de pago
    payment_date = models.DateField(blank=True, null=True)
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    
    # Control y aprobación
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='created_by', related_name='created_budget_executions')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='approved_by', related_name='approved_budget_executions')
    approval_date = models.DateTimeField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'budget_execution'
        verbose_name = 'Ejecución Presupuestaria'
        verbose_name_plural = 'Ejecuciones Presupuestarias'
        indexes = [
            models.Index(fields=['project']),
            models.Index(fields=['phase']),
            models.Index(fields=['invoice_type']),
            models.Index(fields=['invoice_date']),
            models.Index(fields=['invoice_number']),
            models.Index(fields=['category']),
            models.Index(fields=['is_paid']),
            models.Index(fields=['is_approved']),
            models.Index(fields=['is_active']),
            models.Index(fields=['created_by']),
            models.Index(fields=['approved_by']),
        ]

    def __str__(self):
        return f"{self.invoice_name} - {self.invoice_date}"
