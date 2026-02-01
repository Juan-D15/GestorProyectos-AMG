from django import template
from django.db.models import Q

register = template.Library()

@register.filter
def get_project_beneficiaries(project):
    """
    Obtiene los beneficiarios de un proyecto usando el modelo intermedio ProjectBeneficiary.
    """
    from webAMG.models import ProjectBeneficiary, Beneficiary
    
    # Obtener los IDs de los beneficiarios del proyecto
    beneficiary_ids = ProjectBeneficiary.objects.filter(
        project=project
    ).values_list('beneficiary_id', flat=True)
    
    # Obtener los objetos Beneficiary
    beneficiaries = Beneficiary.objects.filter(
        id__in=beneficiary_ids,
        is_active=True
    ).order_by('first_name', 'last_name')
    
    return beneficiaries
