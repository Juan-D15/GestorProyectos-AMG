from django import template
from django.db.models import Q

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Obtiene un item de un diccionario usando una clave.
    """
    if dictionary is None:
        return ''
    return dictionary.get(key, '')

@register.filter
def join_ids(ids_value):
    """
    Une una lista de IDs en una cadena separada por comas.
    """
    print(f"DEBUG join_ids: input={ids_value}, type={type(ids_value)}")
    
    if not ids_value:
        return ''
    
    # Si ya es una cadena con IDs separados por comas, devolverla tal cual
    if isinstance(ids_value, str):
        print(f"DEBUG join_ids: devolviendo string directamente: {ids_value}")
        return ids_value
    
    # Si es una lista, unir los IDs
    if isinstance(ids_value, list):
        result = ','.join(str(item) for item in ids_value)
        print(f"DEBUG join_ids: uniendo lista: {result}")
        return result
    
    print(f"DEBUG join_ids: tipo desconocido, devolviendo string vacío")
    return ''
    
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

